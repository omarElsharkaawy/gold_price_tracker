from datetime import datetime
from typing import Dict

def format_report(price_analysis: Dict, llm_analysis: Dict) -> str:
        """Format the analysis into a user-friendly Telegram message"""

        # Emojis for visual appeal
        if price_analysis['daily_change'] > 0:
            daily_emoji = "📈"
        elif price_analysis['daily_change'] < 0:
            daily_emoji = "📉"
        else:
            daily_emoji = "➡️"

        rec_emoji = {
            'BUY': '🟢',
            'SELL': '🔴', 
            'HOLD': '🟡'
        }.get(llm_analysis['recommendation'], '🟡')

        message = f"""
🥇 **GOLD PRICE ANALYSIS** 
📅 {datetime.now().strftime('%B %d, %Y')}

💰 **CURRENT PRICE**
${price_analysis['current_price']:.2f} USD/oz

{daily_emoji} **DAILY CHANGE**
${price_analysis['daily_change']:+.2f} ({price_analysis['daily_change_pct']:+.2f}%)
Yesterday: ${price_analysis['yesterday_price']:.2f}

📊 **30-DAY SUMMARY**
• Average: ${price_analysis['30_day_avg']:.2f}
• Change: ${price_analysis['30_day_change']:+.2f} ({price_analysis['30_day_change_pct']:+.2f}%)
• High: ${price_analysis['30_day_high']:.2f}
• Low: ${price_analysis['30_day_low']:.2f}
• Volatility: ${price_analysis['volatility']:.2f}

{rec_emoji} **AI RECOMMENDATION: {llm_analysis['recommendation']}**
🎯 Confidence: {llm_analysis['confidence']}%
⚖️ Risk Level: {llm_analysis['risk_level']}

📝 **KEY ANALYSIS POINTS:**
"""

        for i, reason in enumerate(llm_analysis['reasoning'][:3], 1):
            message += f"\n{i}. {reason}"

        message += f"""

🔮 **SHORT-TERM OUTLOOK**
{llm_analysis['short_term_outlook']}

📍 **MARKET POSITION**
{llm_analysis['market_position']}

⚠️ **DISCLAIMER**
This analysis uses AI with real-time market data for informational purposes only. Not financial advice.

---
*Powered by AI Gold Tracker + Perplexity Pro 🤖*
"""

        return message.strip()
