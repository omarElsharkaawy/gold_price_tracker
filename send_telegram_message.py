from common import logger, config
import requests


def send_telegram_message(message: str) -> bool:
    """Send formatted message to Telegram with detailed error logging."""
    try:
        url = f"https://api.telegram.org/bot{config['telegram_bot_token']}/sendMessage"
        data = {
            'chat_id': config['telegram_chat_id'],
            'text': message,
            'parse_mode': 'Markdown'
        }

        response = requests.post(url, json=data)

        if response.status_code != 200:
            logger.error(f"Telegram API error: Status code {response.status_code} - Response: {response.text}")
            return False

        return True

    except Exception as e:
        logger.error(f"Exception while sending Telegram message: {e}")
        return False
