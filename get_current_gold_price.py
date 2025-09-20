import requests
from datetime import datetime
from typing import Dict, Optional
from common import logger, config

def get_current_gold_price() -> Optional[Dict]:
        """Get current gold price from API-Ninjas (Free tier: 50,000 requests/month)"""
        try:
            url = "https://api.api-ninjas.com/v1/commodityprice?name=gold"
            headers = {'X-Api-Key': config['api_ninjas_key']}

            response = requests.get(url, headers=headers)
            data = response.json()
            
            logger.info(f"Current Gold Price Data: {data}")

            return {
                'price': data['price'],
                'timestamp': data['updated'],
                'date': datetime.fromtimestamp(data['updated']).date(),
                'source': 'api-ninjas'
            }
        except Exception as e:
            logger.error(f"Error fetching current gold price: {e}")
            return None    
    