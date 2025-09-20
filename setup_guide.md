
# Gold Price Tracker POC - Setup Guide

## Quick Setup Steps

### 1. Install Dependencies
```bash
pip install requests
```

### 2. Get API Keys (All Free Tiers)

#### A) API-Ninjas (Gold Prices)
- Visit: https://api.api-ninjas.com/register
- Free tier: 50,000 requests/month
- Get your API key from dashboard

#### B) OpenAI API (GPT Analysis) 
- Visit: https://platform.openai.com/signup
- Add $5 minimum credit (GPT-4o-mini costs ~$0.15 per 1M tokens)
- Get API key from: https://platform.openai.com/api-keys

#### C) Telegram Bot
- Message @BotFather on Telegram
- Send: /newbot
- Choose name and username for your bot
- Get bot token
- Add bot to a chat and get your chat ID

### 3. Configure the Script
Replace these lines in the code:
```python
config = {
    'api_ninjas_key': 'YOUR_ACTUAL_API_KEY',
    'openai_api_key': 'sk-your-actual-openai-key', 
    'telegram_bot_token': '123456789:YOUR_BOT_TOKEN',
    'telegram_chat_id': 'YOUR_CHAT_ID_OR_GROUP_ID'
}
```

### 4. Run the POC
```bash
python simple_gold_tracker_poc.py
```

## Expected Costs (Monthly)

| Service | Free Tier | Cost After Free |
|---------|-----------|-----------------|
| API-Ninjas | 50K requests/month | $0.002 per request |
| OpenAI GPT-4o-mini | ~2M tokens free trial | $0.15 per 1M input tokens |
| Telegram Bot | Unlimited | Free |
| **Total Monthly** | **FREE for first month** | **~$1-5 for moderate use** |

## Sample Output

The bot will send messages like this:

```
🥇 GOLD PRICE ANALYSIS
📅 September 19, 2025

💰 CURRENT PRICE
$2,658.50 USD/oz

📈 DAILY CHANGE
+$25.30 (+0.96%)
Yesterday: $2,633.20

📊 30-DAY SUMMARY  
• Average: $2,610.75
• Change: +$47.75 (+1.83%)
• High: $2,690.40
• Low: $2,580.10
• Volatility: 28.45

🟢 AI RECOMMENDATION: BUY
🎯 Confidence: 78%
⚖️ Risk Level: Medium

📝 KEY ANALYSIS POINTS:
1. Gold showing strong upward momentum with daily gain of 0.96%
2. Price is above 30-day average, indicating bullish sentiment  
3. Recent breakout above resistance at $2,650 level

🔮 SHORT-TERM OUTLOOK
Positive - Technical indicators suggest continued upward movement

📍 MARKET POSITION  
Currently trading near 30-day highs, showing strength

⚠️ DISCLAIMER
This is an automated analysis for informational purposes only.
```

## How It Works

1. **Data Collection**: Uses API-Ninjas to get real-time and historical gold prices
2. **Price Analysis**: Calculates daily changes, 30-day trends, volatility
3. **AI Analysis**: Sends price data to GPT-4o-mini for intelligent analysis
4. **Recommendation**: AI provides BUY/SELL/HOLD with reasoning
5. **Telegram Alert**: Formats and sends user-friendly report

## Scheduling (Optional)

To run daily automatically:

### Linux/Mac (Cron):
```bash
# Add to crontab (crontab -e)
0 9 * * * cd /path/to/poc && python simple_gold_tracker_poc.py
```

### Windows (Task Scheduler):
1. Open Task Scheduler  
2. Create Basic Task
3. Set trigger: Daily at 9:00 AM
4. Action: Start python.exe with script path
