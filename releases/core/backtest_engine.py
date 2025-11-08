"""
Strategy Backtesting Engine
Simulates trading strategies on historical data
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from utils.logger import setup_logger

logger = setup_logger('backtest_engine')


class Trade:
    """Represents a single trade"""
    def __init__(self, entry_time, entry_price, position_size, direction='long'):
        self.entry_time = entry_time
        self.entry_price = entry_price
        self.position_size = position_size
        self.direction = direction  # 'long' or 'short'
        self.exit_time = None
        self.exit_price = None
        self.profit = 0
        self.profit_percent = 0
        self.duration = None
        self.closed = False
    
    def close(self, exit_time, exit_price):
        """Close the trade"""
        self.exit_time = exit_time
        self.exit_price = exit_price
        self.closed = True
        
        # Calculate profit
        if self.direction == 'long':
            self.profit = (exit_price - self.entry_price) * self.position_size
            self.profit_percent = ((exit_price - self.entry_price) / self.entry_price) * 100
        else:  # short
            self.profit = (self.entry_price - exit_price) * self.position_size
            self.profit_percent = ((self.entry_price - exit_price) / self.entry_price) * 100
        
        # Calculate duration
        if isinstance(self.entry_time, pd.Timestamp) and isinstance(exit_time, pd.Timestamp):
            self.duration = (exit_time - self.entry_time).total_seconds() / 3600  # hours


class BacktestEngine:
    """Backtesting engine for trading strategies"""
    
    def __init__(self, initial_capital: float = 10000):
        self.initial_capital = initial_capital
        self.capital = initial_capital
        self.trades: List[Trade] = []
        self.equity_curve = []
        self.current_position = None
        
    def load_data(self, data: pd.DataFrame) -> bool:
        """
        Load and validate historical data
        
        Expected columns: timestamp, open, high, low, close, volume
        """
        required_columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
        
        # Check for required columns
        missing = [col for col in required_columns if col not in data.columns]
        if missing:
            logger.error(f"Missing required columns: {missing}")
            return False
        
        # Convert timestamp to datetime if needed
        if not pd.api.types.is_datetime64_any_dtype(data['timestamp']):
            data['timestamp'] = pd.to_datetime(data['timestamp'])
        
        # Sort by timestamp
        data = data.sort_values('timestamp').reset_index(drop=True)
        
        self.data = data
        logger.info(f"Loaded {len(data)} candles from {data['timestamp'].min()} to {data['timestamp'].max()}")
        return True
    
    def execute_strategy(self, strategy_rules: Dict) -> Dict:
        """
        Execute a trading strategy on loaded data
        
        strategy_rules format:
        {
            'name': 'Strategy Name',
            'entry_conditions': callable or dict,
            'exit_conditions': callable or dict,
            'position_size_percent': 10,  # % of capital per trade
            'stop_loss_percent': 2,  # % stop loss
            'take_profit_percent': 5,  # % take profit
            'direction': 'long' or 'short' or 'both'
        }
        """
        if self.data is None or len(self.data) == 0:
            logger.error("No data loaded")
            return {'error': 'No data loaded'}
        
        logger.info(f"Backtesting strategy: {strategy_rules.get('name', 'Unknown')}")
        
        # Reset state
        self.capital = self.initial_capital
        self.trades = []
        self.equity_curve = [self.initial_capital]
        self.current_position = None
        
        # Strategy parameters
        position_size_percent = strategy_rules.get('position_size_percent', 10)
        stop_loss_percent = strategy_rules.get('stop_loss_percent', 2)
        take_profit_percent = strategy_rules.get('take_profit_percent', 5)
        direction = strategy_rules.get('direction', 'long')
        
        # Iterate through data
        for i in range(1, len(self.data)):
            current_candle = self.data.iloc[i]
            prev_candles = self.data.iloc[max(0, i-50):i]  # Last 50 candles for indicators
            
            # Check for open position
            if self.current_position:
                # Check stop loss
                if direction == 'long':
                    if current_candle['low'] <= self.current_position.entry_price * (1 - stop_loss_percent/100):
                        self._close_position(current_candle['timestamp'], 
                                            self.current_position.entry_price * (1 - stop_loss_percent/100))
                        continue
                    
                    # Check take profit
                    if current_candle['high'] >= self.current_position.entry_price * (1 + take_profit_percent/100):
                        self._close_position(current_candle['timestamp'],
                                            self.current_position.entry_price * (1 + take_profit_percent/100))
                        continue
                
                # Check exit conditions
                if self._check_exit_conditions(current_candle, prev_candles, strategy_rules):
                    self._close_position(current_candle['timestamp'], current_candle['close'])
                    continue
            
            else:
                # Check entry conditions
                if self._check_entry_conditions(current_candle, prev_candles, strategy_rules):
                    self._open_position(current_candle['timestamp'], current_candle['close'], 
                                       position_size_percent, direction)
            
            # Update equity curve
            current_equity = self.capital
            if self.current_position:
                unrealized_pnl = (current_candle['close'] - self.current_position.entry_price) * self.current_position.position_size
                current_equity += unrealized_pnl
            
            self.equity_curve.append(current_equity)
        
        # Close any open position at end
        if self.current_position:
            last_candle = self.data.iloc[-1]
            self._close_position(last_candle['timestamp'], last_candle['close'])
        
        # Calculate results
        results = self._calculate_results()
        return results
    
    def _check_entry_conditions(self, current, history, rules) -> bool:
        """Check if entry conditions are met"""
        # If callable function provided
        if callable(rules.get('entry_conditions')):
            return rules['entry_conditions'](current, history)
        
        # If dict of conditions provided
        conditions = rules.get('entry_conditions', {})
        
        # Example simple conditions
        if 'rsi_below' in conditions:
            rsi = self._calculate_rsi(history['close'], 14)
            if rsi is None or rsi > conditions['rsi_below']:
                return False
        
        if 'price_above_ma' in conditions:
            ma = history['close'].tail(conditions['price_above_ma']).mean()
            if current['close'] < ma:
                return False
        
        return True
    
    def _check_exit_conditions(self, current, history, rules) -> bool:
        """Check if exit conditions are met"""
        # If callable function provided
        if callable(rules.get('exit_conditions')):
            return rules['exit_conditions'](current, history)
        
        # If dict of conditions provided
        conditions = rules.get('exit_conditions', {})
        
        # Example simple conditions
        if 'rsi_above' in conditions:
            rsi = self._calculate_rsi(history['close'], 14)
            if rsi is not None and rsi > conditions['rsi_above']:
                return True
        
        return False
    
    def _open_position(self, timestamp, price, position_size_percent, direction):
        """Open a new position"""
        position_size = (self.capital * position_size_percent / 100) / price
        self.current_position = Trade(timestamp, price, position_size, direction)
        logger.info(f"Opened {direction} position at {price}, size: {position_size}")
    
    def _close_position(self, timestamp, price):
        """Close current position"""
        if self.current_position:
            self.current_position.close(timestamp, price)
            self.capital += self.current_position.profit
            self.trades.append(self.current_position)
            logger.info(f"Closed position at {price}, profit: {self.current_position.profit:.2f}")
            self.current_position = None
    
    def _calculate_rsi(self, prices, period=14):
        """Calculate RSI indicator"""
        if len(prices) < period + 1:
            return None
        
        deltas = prices.diff()
        gain = (deltas.where(deltas > 0, 0)).rolling(window=period).mean()
        loss = (-deltas.where(deltas < 0, 0)).rolling(window=period).mean()
        
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi.iloc[-1]
    
    def _calculate_results(self) -> Dict:
        """Calculate backtest results and metrics"""
        if len(self.trades) == 0:
            return {
                'total_trades': 0,
                'error': 'No trades executed'
            }
        
        # Basic metrics
        total_trades = len(self.trades)
        winning_trades = [t for t in self.trades if t.profit > 0]
        losing_trades = [t for t in self.trades if t.profit <= 0]
        
        win_rate = (len(winning_trades) / total_trades * 100) if total_trades > 0 else 0
        
        total_profit = sum(t.profit for t in self.trades)
        total_return = ((self.capital - self.initial_capital) / self.initial_capital) * 100
        
        avg_win = np.mean([t.profit for t in winning_trades]) if winning_trades else 0
        avg_loss = np.mean([t.profit for t in losing_trades]) if losing_trades else 0
        
        # Calculate max drawdown
        equity_array = np.array(self.equity_curve)
        running_max = np.maximum.accumulate(equity_array)
        drawdown = (equity_array - running_max) / running_max * 100
        max_drawdown = abs(drawdown.min())
        
        # Calculate Sharpe ratio (simplified)
        returns = pd.Series(self.equity_curve).pct_change().dropna()
        sharpe_ratio = (returns.mean() / returns.std() * np.sqrt(252)) if returns.std() > 0 else 0
        
        # Average trade duration
        durations = [t.duration for t in self.trades if t.duration is not None]
        avg_duration = np.mean(durations) if durations else 0
        
        results = {
            'total_trades': total_trades,
            'winning_trades': len(winning_trades),
            'losing_trades': len(losing_trades),
            'win_rate': win_rate,
            'total_profit': total_profit,
            'total_return_percent': total_return,
            'initial_capital': self.initial_capital,
            'final_capital': self.capital,
            'avg_win': avg_win,
            'avg_loss': avg_loss,
            'profit_factor': abs(avg_win / avg_loss) if avg_loss != 0 else 0,
            'max_drawdown_percent': max_drawdown,
            'sharpe_ratio': sharpe_ratio,
            'avg_trade_duration_hours': avg_duration,
            'equity_curve': self.equity_curve,
            'trades': self.trades,
            'profitable': total_profit > 0
        }
        
        return results


# Create global instance
backtest_engine = BacktestEngine()
