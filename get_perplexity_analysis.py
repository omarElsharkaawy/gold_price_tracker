import requests
import json
from typing import  Dict
from common import logger, config

def get_perplexity_analysis(price_analysis: Dict) -> Dict:
        """Use Perplexity Pro API to analyze the price data and provide recommendation"""
        try:
            # Construct the prompt for Perplexity
            prompt = f"""
You are a professional gold market analyst. Analyze the following gold price data and provide investment recommendation.

CURRENT GOLD PRICE DATA:
- Current Price: ${price_analysis['current_price']:.2f} USD/oz
- Yesterday Price: ${price_analysis['yesterday_price']:.2f} USD/oz
- Daily Change: ${price_analysis['daily_change']:+.2f} ({price_analysis['daily_change_pct']:+.2f}%)
- 30-Day Average: ${price_analysis['30_day_avg']:.2f} USD/oz
- 30-Day Change: ${price_analysis['30_day_change']:+.2f} ({price_analysis['30_day_change_pct']:+.2f}%)
- 30-Day High: ${price_analysis['30_day_high']:.2f} USD/oz
- 30-Day Low: ${price_analysis['30_day_low']:.2f} USD/oz
- Price Volatility: ${price_analysis['volatility']:.2f}

ANALYSIS REQUIREMENTS:
1. Provide a clear BUY/SELL/HOLD recommendation
2. Give a confidence level (1-100%)
3. List 3 key reasons for your recommendation based on technical analysis
4. Assess the short-term trend (next 1-7 days)
5. Consider current market conditions and gold's position relative to its 30-day range

Please respond in the following JSON format only:
{{
    "recommendation": "BUY/SELL/HOLD",
    "confidence": 85,
    "reasoning": [
        "Technical reason 1",
        "Market condition reason 2", 
        "Price action reason 3"
    ],
    "short_term_outlook": "Brief outlook with explanation",
    "market_position": "Current price position analysis",
    "risk_level": "Low/Medium/High"
}}
"""

            # Call Perplexity API (uses OpenAI-compatible format)
            headers = {
                'Authorization': f'Bearer {config["perplexity_api_key"]}',
                'Content-Type': 'application/json'
            }

            data = {
                'model': 'sonar',  # Perplexity model with web search
                'messages': [
                    {
                        'role': 'system', 
                        'content': 'You are a professional gold market analyst with access to current market data and trends. Provide technical analysis based on the price data provided.'
                    },
                    {
                        'role': 'user', 
                        'content': prompt
                    }
                ],
                'temperature': 0.2,  # Lower temperature for more consistent analysis
                'max_tokens': 500
            }

            # Perplexity API endpoint
            response = requests.post('https://api.perplexity.ai/chat/completions', 
                                   headers=headers, json=data)

            if response.status_code == 200:
                result = response.json()
                analysis_text = result['choices'][0]['message']['content']

                # Try to parse JSON response
                try:
                    # Extract JSON from response if it contains other text
                    start_idx = analysis_text.find('{')
                    end_idx = analysis_text.rfind('}') + 1
                    if start_idx != -1 and end_idx != 0:
                        json_text = analysis_text[start_idx:end_idx]
                        analysis_json = json.loads(json_text)
                        return analysis_json
                    else:
                        # Try parsing the entire response
                        analysis_json = json.loads(analysis_text)
                        return analysis_json

                except json.JSONDecodeError:
                    # Fallback if JSON parsing fails
                    logger.warning("Failed to parse JSON from Perplexity response, using fallback")
                    return {
                        'recommendation': 'HOLD',
                        'confidence': 50,
                        'reasoning': [
                            'Unable to parse structured analysis',
                            'Raw analysis available in logs',
                            'Using fallback recommendation system'
                        ],
                        'short_term_outlook': 'Analysis parsing failed, using conservative approach',
                        'market_position': 'Unable to determine from response',
                        'risk_level': 'Medium'
                    }
            else:
                logger.error(f"Perplexity API error: {response.status_code} - {response.text}")
                return self._fallback_analysis(price_analysis)

        except Exception as e:
            logger.error(f"Error in Perplexity analysis: {e}")
            return self._fallback_analysis(price_analysis)
