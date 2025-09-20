
# AI Gold Price Tracker - POC with Perplexity Pro API
# This version uses Perplexity Pro API instead of OpenAI GPT-4o-mini

from calculate_price_analysis import calculate_price_analysis
from format_report import format_report
from get_current_gold_price import get_current_gold_price
from get_perplexity_analysis import get_perplexity_analysis
from llm_fetch import get_historical_gold_prices_via_llm
from common import logger
from send_telegram_message import send_telegram_message

class SimpleGoldTracker:

    def run_analysis(self):
        """Main function to run the complete analysis"""
        logger.info("Starting Gold Price Analysis with Perplexity Pro...")

        try:
            # Step 1: Get current gold price
            current_data = get_current_gold_price()
            if not current_data:
                logger.error("Failed to get current gold price")
                return
            
            logger.info(f"Current Gold Price: ${current_data['price']} (Source: {current_data['source']})")
            # Step 2: Get 30-day historical data
            historical_data = get_historical_gold_prices_via_llm()
            logger.info(f"Retrieved {len(historical_data)} days of historical data")

            # Step 3: Calculate price analysis
            price_analysis = calculate_price_analysis(current_data['price'], historical_data)
            logger.info(f"Calculated price analysis: {price_analysis}")

            # Step 4: Get Perplexity AI analysis and recommendation
            llm_analysis = get_perplexity_analysis(price_analysis)

            # Step 5: Format and send report
            report = format_report(price_analysis, llm_analysis)

            success = send_telegram_message(report)

            if success:
                logger.info("Analysis completed and sent successfully!")
                logger.info(f"Recommendation: {llm_analysis['recommendation']} (Confidence: {llm_analysis['confidence']}%)")
            else:
                logger.error("Failed to send Telegram message")
                print("REPORT CONTENT:")
                print(report)

        except Exception as e:
            logger.error(f"Error in analysis: {e}")
            # Send error notification
            send_telegram_message(f"❌ Gold Tracker Error: {str(e)}")
# Configuration
if __name__ == "__main__":
    tracker = SimpleGoldTracker()
    tracker.run_analysis()
