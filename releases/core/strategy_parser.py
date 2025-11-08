"""
Strategy Parser - Extracts trading rules from documents using Claude
"""
import os
import json
from pathlib import Path
from typing import Dict, Optional
import anthropic
from docx import Document
import PyPDF2
import pandas as pd
from config.settings import settings
from utils.logger import setup_logger

logger = setup_logger('strategy_parser')


class StrategyParser:
    """Parse trading strategy documents and extract rules"""
    
    def __init__(self):
        self.claude_api_key = None
        self._load_claude_key()
    
    def _load_claude_key(self):
        """Load Claude API key"""
        api_keys = settings.get_api_key('claude')
        self.claude_api_key = api_keys.get('key')
    
    def parse_file(self, file_path: str) -> Optional[Dict]:
        """
        Parse strategy file and extract trading rules
        
        Supported formats: PDF, DOCX, TXT, XLSX, Pine Script
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            logger.error(f"File not found: {file_path}")
            return None
        
        # Extract text based on file type
        extension = file_path.suffix.lower()
        
        try:
            if extension == '.pdf':
                text = self._extract_from_pdf(file_path)
            elif extension in ['.docx', '.doc']:
                text = self._extract_from_docx(file_path)
            elif extension in ['.txt', '.pine']:
                text = self._extract_from_txt(file_path)
            elif extension in ['.xlsx', '.xls']:
                text = self._extract_from_excel(file_path)
            else:
                logger.error(f"Unsupported file format: {extension}")
                return None
            
            if not text:
                logger.error("Failed to extract text from file")
                return None
            
            # Use Claude to parse strategy
            strategy_rules = self._parse_with_claude(text, file_path.name)
            return strategy_rules
            
        except Exception as e:
            logger.error(f"Error parsing file: {e}")
            return None
    
    def _extract_from_pdf(self, file_path: Path) -> str:
        """Extract text from PDF"""
        try:
            text = ""
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
            return text
        except Exception as e:
            logger.error(f"Error reading PDF: {e}")
            return ""
    
    def _extract_from_docx(self, file_path: Path) -> str:
        """Extract text from DOCX"""
        try:
            doc = Document(file_path)
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            return text
        except Exception as e:
            logger.error(f"Error reading DOCX: {e}")
            return ""
    
    def _extract_from_txt(self, file_path: Path) -> str:
        """Extract text from TXT"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            logger.error(f"Error reading TXT: {e}")
            return ""
    
    def _extract_from_excel(self, file_path: Path) -> str:
        """Extract text from Excel"""
        try:
            df = pd.read_excel(file_path)
            # Convert dataframe to text representation
            text = f"Excel file with {len(df)} rows and {len(df.columns)} columns\n"
            text += f"Columns: {', '.join(df.columns)}\n\n"
            text += df.to_string()
            return text
        except Exception as e:
            logger.error(f"Error reading Excel: {e}")
            return ""
    
    def _parse_with_claude(self, strategy_text: str, filename: str) -> Optional[Dict]:
        """Use Claude to extract trading rules from strategy text"""
        if not self.claude_api_key:
            logger.warning("Claude API key not configured, using simple parser")
            return self._simple_parse(strategy_text)
        
        try:
            client = anthropic.Anthropic(api_key=self.claude_api_key)
            
            prompt = f"""You are a trading strategy analyzer. Extract the trading rules from this strategy document.

Strategy Document ({filename}):
{strategy_text}

Extract and return a JSON object with the following structure:
{{
    "strategy_name": "Name of the strategy",
    "description": "Brief description of what the strategy does",
    "timeframe": "Preferred timeframe (e.g., 1h, 4h, 1d)",
    "indicators": ["List of technical indicators used"],
    "entry_rules": {{
        "long": ["List of conditions for long entry"],
        "short": ["List of conditions for short entry"]
    }},
    "exit_rules": {{
        "take_profit": "Take profit condition",
        "stop_loss": "Stop loss condition",
        "trailing_stop": "Trailing stop condition if any",
        "other": ["Any other exit conditions"]
    }},
    "position_sizing": "How to size positions (percentage, fixed, etc)",
    "risk_management": ["Risk management rules"],
    "notes": ["Any additional important notes"]
}}

If specific values are mentioned (like "RSI below 30" or "stop loss at 2%"), include those exact values.
If the document is a Pine Script, extract the logic from the code.
Return ONLY the JSON object, no other text."""

            message = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=2000,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )
            
            # Parse Claude's response
            response_text = message.content[0].text.strip()
            
            # Remove markdown code blocks if present
            if response_text.startswith('```'):
                response_text = response_text.split('```')[1]
                if response_text.startswith('json'):
                    response_text = response_text[4:]
                response_text = response_text.strip()
            
            strategy_dict = json.loads(response_text)
            logger.info(f"Successfully parsed strategy: {strategy_dict.get('strategy_name', 'Unknown')}")
            
            return strategy_dict
            
        except Exception as e:
            logger.error(f"Error using Claude to parse strategy: {e}")
            return self._simple_parse(strategy_text)
    
    def _simple_parse(self, text: str) -> Dict:
        """Simple keyword-based parsing as fallback"""
        strategy = {
            'strategy_name': 'Parsed Strategy',
            'description': 'Strategy parsed from document',
            'timeframe': '1h',
            'indicators': [],
            'entry_rules': {'long': [], 'short': []},
            'exit_rules': {},
            'position_sizing': '10% of capital',
            'risk_management': [],
            'notes': ['Strategy parsed using simple parser - configure Claude API for better results']
        }
        
        text_lower = text.lower()
        
        # Detect indicators
        indicators = ['rsi', 'macd', 'ema', 'sma', 'bollinger', 'stochastic', 'atr']
        for indicator in indicators:
            if indicator in text_lower:
                strategy['indicators'].append(indicator.upper())
        
        # Detect entry conditions
        if 'rsi' in text_lower and 'below' in text_lower:
            strategy['entry_rules']['long'].append('RSI below threshold')
        if 'rsi' in text_lower and 'above' in text_lower:
            strategy['entry_rules']['short'].append('RSI above threshold')
        
        # Detect stop loss
        if 'stop loss' in text_lower or 'stop-loss' in text_lower:
            strategy['exit_rules']['stop_loss'] = '2% default'
        
        # Detect take profit
        if 'take profit' in text_lower or 'take-profit' in text_lower:
            strategy['exit_rules']['take_profit'] = '5% default'
        
        return strategy
    
    def convert_to_executable(self, strategy_dict: Dict) -> Dict:
        """
        Convert parsed strategy to executable backtest rules
        
        Returns dict with functions that can be used by backtest engine
        """
        # This creates a simplified executable version
        # In practice, this would need more sophisticated conversion
        
        rules = {
            'name': strategy_dict.get('strategy_name', 'Strategy'),
            'position_size_percent': 10,  # Default
            'stop_loss_percent': 2,  # Default
            'take_profit_percent': 5,  # Default
            'direction': 'long',  # Default
            'entry_conditions': {},
            'exit_conditions': {}
        }
        
        # Extract specific values from rules if present
        entry_rules = strategy_dict.get('entry_rules', {})
        exit_rules = strategy_dict.get('exit_rules', {})
        
        # Parse stop loss percentage
        if 'stop_loss' in exit_rules:
            sl_text = str(exit_rules['stop_loss']).lower()
            if '%' in sl_text:
                try:
                    rules['stop_loss_percent'] = float(sl_text.split('%')[0].split()[-1])
                except:
                    pass
        
        # Parse take profit percentage
        if 'take_profit' in exit_rules:
            tp_text = str(exit_rules['take_profit']).lower()
            if '%' in tp_text:
                try:
                    rules['take_profit_percent'] = float(tp_text.split('%')[0].split()[-1])
                except:
                    pass
        
        # Set entry conditions based on indicators
        indicators = strategy_dict.get('indicators', [])
        if 'RSI' in indicators:
            rules['entry_conditions']['rsi_below'] = 30  # Default RSI oversold
            rules['exit_conditions']['rsi_above'] = 70  # Default RSI overbought
        
        return rules


# Global instance
strategy_parser = StrategyParser()
