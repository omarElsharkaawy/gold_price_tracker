from common import logger, config
import requests

def send_telegram_message(message: str) -> bool:
        """Send formatted message to Telegram"""
        try:
            url = f"https://api.telegram.org/bot{config['telegram_bot_token']}/sendMessage"
            data = {
                'chat_id': config['telegram_chat_id'],
                'text': message,
                'parse_mode': 'Markdown'
            }

            response = requests.post(url, json=data)
            return response.status_code == 200

        except Exception as e:
            logger.error(f"Error sending Telegram message: {e}")
            return False
