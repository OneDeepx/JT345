"""
CryptoPanic API Integration
Fetches cryptocurrency news and sentiment data
"""
import requests
from typing import List, Dict, Optional
from datetime import datetime
from config.settings import settings
from utils.logger import setup_logger

logger = setup_logger('cryptopanic_api')

# API Configuration
CRYPTOPANIC_BASE_URL = "https://cryptopanic.com/api/v1"


class CryptoPanicAPI:
    """Interface for CryptoPanic news API"""
    
    def __init__(self):
        self.base_url = CRYPTOPANIC_BASE_URL
        self.api_key = None
        self._load_api_key()
    
    def _load_api_key(self):
        """Load API key from settings"""
        api_keys = settings.get_api_key('cryptopanic')
        self.api_key = api_keys.get('key')
        
        if self.api_key:
            logger.info("CryptoPanic API key loaded")
        else:
            logger.warning("CryptoPanic API key not configured")
    
    def is_configured(self) -> bool:
        """Check if API is configured with valid key"""
        return self.api_key is not None and len(self.api_key) > 0
    
    def get_posts(
        self,
        currencies: Optional[str] = None,
        kind: str = "news",
        filter_type: str = "rising",
        limit: int = 50
    ) -> List[Dict]:
        """
        Get news posts from CryptoPanic
        
        Args:
            currencies: Comma-separated currency codes (e.g., "BTC,ETH")
            kind: Type of posts - "news" or "media" or "all"
            filter_type: Filter - "rising", "hot", "bullish", "bearish", "important", "saved", "lol"
            limit: Number of posts to fetch (max 50)
            
        Returns:
            List of news posts
        """
        if not self.is_configured():
            logger.error("CryptoPanic API not configured")
            return []
        
        try:
            # Build request parameters
            params = {
                'auth_token': self.api_key,
                'kind': kind,
                'filter': filter_type,
            }
            
            if currencies:
                params['currencies'] = currencies
            
            # Make request
            url = f"{self.base_url}/posts/"
            logger.info(f"Fetching posts from CryptoPanic: {filter_type}")
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Extract posts
            posts = data.get('results', [])[:limit]
            logger.info(f"Fetched {len(posts)} posts")
            
            # Parse posts
            parsed_posts = []
            for post in posts:
                parsed_post = self._parse_post(post)
                parsed_posts.append(parsed_post)
            
            return parsed_posts
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching posts: {e}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return []
    
    def _parse_post(self, post: Dict) -> Dict:
        """
        Parse a post from API response
        
        Args:
            post: Raw post data from API
            
        Returns:
            Parsed post dictionary
        """
        try:
            # Extract votes (for sentiment)
            votes = post.get('votes', {})
            positive = votes.get('positive', 0)
            negative = votes.get('negative', 0)
            important = votes.get('important', 0)
            liked = votes.get('liked', 0)
            disliked = votes.get('disliked', 0)
            lol = votes.get('lol', 0)
            toxic = votes.get('toxic', 0)
            saved = votes.get('saved', 0)
            
            # Calculate sentiment score (-1 to 1)
            total_votes = positive + negative
            if total_votes > 0:
                sentiment_score = (positive - negative) / total_votes
            else:
                sentiment_score = 0
            
            # Determine sentiment label
            if sentiment_score > 0.3:
                sentiment = "Bullish"
            elif sentiment_score < -0.3:
                sentiment = "Bearish"
            else:
                sentiment = "Neutral"
            
            # Parse timestamp
            published_at = post.get('published_at', '')
            try:
                timestamp = datetime.fromisoformat(published_at.replace('Z', '+00:00'))
                time_str = timestamp.strftime('%Y-%m-%d %H:%M')
            except:
                time_str = published_at
            
            # Extract currencies
            currencies = post.get('currencies', [])
            currency_codes = [c.get('code', '') for c in currencies]
            
            return {
                'id': post.get('id'),
                'title': post.get('title', 'No title'),
                'url': post.get('url', ''),
                'source': post.get('source', {}).get('title', 'Unknown'),
                'published_at': time_str,
                'sentiment': sentiment,
                'sentiment_score': sentiment_score,
                'votes': {
                    'positive': positive,
                    'negative': negative,
                    'important': important,
                    'liked': liked,
                    'disliked': disliked,
                    'lol': lol,
                    'toxic': toxic,
                    'saved': saved
                },
                'currencies': currency_codes,
                'kind': post.get('kind', 'news')
            }
        except Exception as e:
            logger.error(f"Error parsing post: {e}")
            return {
                'id': post.get('id', 'unknown'),
                'title': post.get('title', 'Error parsing post'),
                'url': '',
                'source': 'Unknown',
                'published_at': '',
                'sentiment': 'Neutral',
                'sentiment_score': 0,
                'votes': {},
                'currencies': [],
                'kind': 'news'
            }
    
    def get_bullish_news(self, currencies: Optional[str] = None, limit: int = 20) -> List[Dict]:
        """Get bullish news posts"""
        return self.get_posts(currencies=currencies, filter_type='bullish', limit=limit)
    
    def get_bearish_news(self, currencies: Optional[str] = None, limit: int = 20) -> List[Dict]:
        """Get bearish news posts"""
        return self.get_posts(currencies=currencies, filter_type='bearish', limit=limit)
    
    def get_important_news(self, currencies: Optional[str] = None, limit: int = 20) -> List[Dict]:
        """Get important news posts"""
        return self.get_posts(currencies=currencies, filter_type='important', limit=limit)
    
    def get_rising_news(self, currencies: Optional[str] = None, limit: int = 20) -> List[Dict]:
        """Get rising/trending news posts"""
        return self.get_posts(currencies=currencies, filter_type='rising', limit=limit)
    
    def get_hot_news(self, currencies: Optional[str] = None, limit: int = 20) -> List[Dict]:
        """Get hot news posts"""
        return self.get_posts(currencies=currencies, filter_type='hot', limit=limit)
    
    def test_connection(self) -> tuple[bool, str]:
        """
        Test API connection
        
        Returns:
            (success, message) tuple
        """
        if not self.is_configured():
            return False, "API key not configured"
        
        try:
            # Try to fetch one post
            params = {
                'auth_token': self.api_key,
                'filter': 'rising',
            }
            
            url = f"{self.base_url}/posts/"
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                count = len(data.get('results', []))
                return True, f"Connected successfully! Found {count} posts."
            elif response.status_code == 401:
                return False, "Invalid API key"
            elif response.status_code == 403:
                return False, "Access forbidden - check API key permissions"
            else:
                return False, f"HTTP {response.status_code}"
                
        except requests.exceptions.Timeout:
            return False, "Connection timeout"
        except requests.exceptions.ConnectionError:
            return False, "Cannot connect to CryptoPanic"
        except Exception as e:
            return False, f"Error: {str(e)}"


# Global API instance
cryptopanic_api = CryptoPanicAPI()
