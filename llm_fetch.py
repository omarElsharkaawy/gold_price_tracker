
# Complete LLM Integration for Historical Gold Price Data
# This function returns data in the exact format expected by your processing code

import requests
import json
from datetime import datetime
from typing import List, Dict
from common import logger, config

def get_historical_gold_prices_via_llm(days: int = 30) -> List[Dict]:
    logger.info(f"Fetching {days} days of historical gold prices via LLM")

    prompt = f"""
Please provide exactly {days} days of historical gold price data (XAU/USD) starting from today (September 20, 2025) going backwards.

Return ONLY a JSON array in this EXACT format (no additional text):

[
    {{
        "time": 1726790400,
        "close": 2658.50,
        "high": 2665.20,
        "low": 2645.80,
        "volume": 125000
    }},
    {{
        "time": 1726704000,
        "close": 2642.30,
        "high": 2655.40,
        "low": 2638.90,
        "volume": 118000
    }}
]

CRITICAL Requirements:
1. "time": Unix timestamp (integer) representing market close each day
2. "close": Daily closing gold price in USD per ounce (float)
3. "high": Daily high price (float)
4. "low": Daily low price (float) 
5. "volume": Trading volume (integer, estimate if needed)
6. Use real market data from financial sources
7. Return exactly {days} entries
8. Start from September 20, 2025 and go backwards
9. NO explanatory text - ONLY the JSON array

Search current financial data sources for accurate historical gold prices.
"""

    headers = {
        'Authorization': f'Bearer {config["perplexity_api_key"]}',
        'Content-Type': 'application/json'
    }

    data = {
        'model': 'sonar',
        'messages': [
            {
                'role': 'system', 
                'content': 'You are a financial data provider. Return accurate historical gold price data in the exact JSON format requested. No explanations, only the JSON array.'
            },
            {'role': 'user', 'content': prompt}
        ],
        'temperature': 0.05,  # Very low for consistent formatting
        'max_tokens': 3000
    }

    try:
        response = requests.post('https://api.perplexity.ai/chat/completions', 
                               headers=headers, json=data, timeout=45)

        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content'].strip()

            # Extract JSON array from response
            start_idx = content.find('[')
            end_idx = content.rfind(']') + 1

            if start_idx != -1 and end_idx != 0:
                json_str = content[start_idx:end_idx]
                historical_data = json.loads(json_str)

                # Validate structure
                if isinstance(historical_data, list) and len(historical_data) > 0:
                    required_fields = ['time', 'close', 'high', 'low', 'volume']

                    # Check first item has all required fields
                    if all(field in historical_data[0] for field in required_fields):
                        # Ensure proper data types
                        for item in historical_data:
                            item['time'] = int(item['time'])
                            item['close'] = float(item['close'])
                            item['high'] = float(item['high'])
                            item['low'] = float(item['low'])
                            item['volume'] = int(item['volume'])

                        return historical_data
                    else:
                        print(f"Missing required fields. Got: {list(historical_data[0].keys())}")
                        return []
                else:
                    print("Invalid data structure from LLM")
                    return []
            else:
                print(f"Could not extract JSON from LLM response: {content[:200]}...")
                return []
        else:
            print(f"LLM API error: {response.status_code} - {response.text}")
            return []

    except json.JSONDecodeError as e:
        print(f"JSON parsing error: {e}")
        return []
    except Exception as e:
        print(f"Error in LLM historical data collection: {e}")
        return []

# Test function to verify the format works with your processing code
def test_data_processing(historical_data: List[Dict]):
    """Test that the data works with your processing code"""
    try:
        processed_data = []
        for item in historical_data:
            processed_data.append({
                'date': datetime.fromtimestamp(item['time']).date(),
                'price': item['close'],
                'high': item['high'],
                'low': item['low'],
                'volume': item['volume']
            })

        print(f"✅ Successfully processed {len(processed_data)} entries")

        # Show sample
        for i, entry in enumerate(processed_data[:3]):
            print(f"Entry {i+1}: Date={entry['date']}, Price=${entry['price']:.2f}, High=${entry['high']:.2f}, Low=${entry['low']:.2f}, Volume={entry['volume']:,}")

        return True

    except Exception as e:
        print(f"❌ Processing failed: {e}")
        return False

