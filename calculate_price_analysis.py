from typing import Dict, List

def calculate_price_analysis(current_price: float, historical_data: List[Dict]) -> Dict:
    """Calculate basic price statistics"""
    if not historical_data:
        return {
            'current_price': current_price,
            'yesterday_price': current_price,
            'daily_change': 0,
            'daily_change_pct': 0,
            '30_day_avg': current_price,
            '30_day_change': 0,
            '30_day_change_pct': 0,
            '30_day_high': current_price,
            '30_day_low': current_price,
            'volatility': 0
        }

    # Sort by date to ensure correct order
    sorted_data = sorted(historical_data, key=lambda x: x['time'])
    prices = [item['close'] for item in sorted_data]

    # Yesterday's price (last item in historical data)
    yesterday_price = prices[-1] if prices else current_price

    # Daily change
    daily_change = current_price - yesterday_price
    daily_change_pct = (daily_change / yesterday_price * 100) if yesterday_price > 0 else 0

    # 30-day statistics
    avg_30_day = sum(prices) / len(prices) if prices else current_price
    oldest_price = prices[0] if prices else current_price
    change_30_day = current_price - oldest_price
    change_30_day_pct = (change_30_day / oldest_price * 100) if oldest_price > 0 else 0

    # High/Low
    high_30_day = max(prices + [current_price])
    low_30_day = min(prices + [current_price])

    # Simple volatility (standard deviation)
    if len(prices) > 1:
        mean_price = sum(prices) / len(prices)
        variance = sum((p - mean_price) ** 2 for p in prices) / len(prices)
        volatility = variance ** 0.5
    else:
        volatility = 0

    return {
        'current_price': round(current_price, 2),
        'yesterday_price': round(yesterday_price, 2),
        'daily_change': round(daily_change, 2),
        'daily_change_pct': round(daily_change_pct, 2),
        '30_day_avg': round(avg_30_day, 2),
        '30_day_change': round(change_30_day, 2),
        '30_day_change_pct': round(change_30_day_pct, 2),
        '30_day_high': round(high_30_day, 2),
        '30_day_low': round(low_30_day, 2),
        'volatility': round(volatility, 2)
    }
