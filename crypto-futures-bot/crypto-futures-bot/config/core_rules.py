"""
Core Trading Rules - IMMUTABLE
These rules cannot be overridden by any uploaded strategy
"""

# Sentiment Rules
SENTIMENT_MIN_THRESHOLD = 3  # Minimum absolute sentiment score to trade
SENTIMENT_RANGE = (-4, 4)  # Sentiment score range
TRADE_LONG_SENTIMENT = 3  # Trade long when sentiment >= this
TRADE_SHORT_SENTIMENT = -3  # Trade short when sentiment <= this

# Risk Management Rules
MAX_RISK_PERCENT = 0.01  # 1% of capital per trade - HARD LIMIT
MIN_POSITION_SIZE = 10  # Minimum position size in USD

# Stop Loss Rules
STOP_LOSS_MAX_RATIO = 0.5  # Stop loss must be <= 50% of take profit

# Trading Constraints
MIN_TAKE_PROFIT_PERCENT = 0.005  # Minimum 0.5% take profit
MAX_POSITION_COUNT = 5  # Maximum concurrent positions
MIN_TIME_BETWEEN_TRADES = 60  # Seconds between trades

# Validation Rules
REQUIRE_TECHNICAL_CONFIRMATION = True
REQUIRE_VOLUME_CONFIRMATION = True
REQUIRE_SENTIMENT_CONFIRMATION = True

def validate_core_rules(trade_params: dict) -> tuple[bool, str]:
    """
    Validate that a trade meets all core rules
    
    Args:
        trade_params: Dictionary containing trade parameters
        
    Returns:
        (is_valid, error_message)
    """
    # Sentiment check
    sentiment = trade_params.get('sentiment', 0)
    if abs(sentiment) < SENTIMENT_MIN_THRESHOLD:
        return False, f"Sentiment {sentiment} does not meet threshold of ±{SENTIMENT_MIN_THRESHOLD}"
    
    # Risk check
    risk_percent = trade_params.get('risk_percent', 0)
    if risk_percent > MAX_RISK_PERCENT:
        return False, f"Risk {risk_percent:.2%} exceeds maximum of {MAX_RISK_PERCENT:.2%}"
    
    # Stop loss check
    take_profit = trade_params.get('take_profit_percent', 0)
    stop_loss = trade_params.get('stop_loss_percent', 0)
    
    if stop_loss > take_profit * STOP_LOSS_MAX_RATIO:
        return False, f"Stop loss {stop_loss:.2%} exceeds {STOP_LOSS_MAX_RATIO:.0%} of take profit {take_profit:.2%}"
    
    if take_profit < MIN_TAKE_PROFIT_PERCENT:
        return False, f"Take profit {take_profit:.2%} below minimum {MIN_TAKE_PROFIT_PERCENT:.2%}"
    
    # Direction vs sentiment check
    direction = trade_params.get('direction', '')
    if direction == 'LONG' and sentiment < TRADE_LONG_SENTIMENT:
        return False, f"Cannot trade LONG with sentiment {sentiment} (requires >= {TRADE_LONG_SENTIMENT})"
    if direction == 'SHORT' and sentiment > TRADE_SHORT_SENTIMENT:
        return False, f"Cannot trade SHORT with sentiment {sentiment} (requires <= {TRADE_SHORT_SENTIMENT})"
    
    return True, "All core rules satisfied"


def calculate_position_size(capital: float, risk_percent: float = None) -> float:
    """
    Calculate position size based on capital and risk
    
    Args:
        capital: Total account capital
        risk_percent: Risk percentage (defaults to MAX_RISK_PERCENT)
        
    Returns:
        Position size in USD
    """
    if risk_percent is None:
        risk_percent = MAX_RISK_PERCENT
    
    # Enforce maximum risk
    risk_percent = min(risk_percent, MAX_RISK_PERCENT)
    
    position_size = capital * risk_percent
    
    # Enforce minimum position size
    return max(position_size, MIN_POSITION_SIZE)


def calculate_stop_loss(entry_price: float, take_profit_price: float, direction: str) -> float:
    """
    Calculate stop loss price based on take profit
    
    Args:
        entry_price: Entry price
        take_profit_price: Take profit price
        direction: 'LONG' or 'SHORT'
        
    Returns:
        Stop loss price
    """
    if direction == 'LONG':
        tp_distance = take_profit_price - entry_price
        max_sl_distance = tp_distance * STOP_LOSS_MAX_RATIO
        stop_loss_price = entry_price - max_sl_distance
    else:  # SHORT
        tp_distance = entry_price - take_profit_price
        max_sl_distance = tp_distance * STOP_LOSS_MAX_RATIO
        stop_loss_price = entry_price + max_sl_distance
    
    return stop_loss_price


class CoreRulesViolationError(Exception):
    """Raised when a trade violates core rules"""
    pass
