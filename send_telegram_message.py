from common import logger, config
import requests

# Define your list of chat IDs here
chat_id_list = [
    '-1002647495037',
]

def send_telegram_message(message: str) -> bool:
    """Send formatted message to Telegram to multiple chat IDs from list."""
    if not chat_id_list:
        logger.warning("send_telegram_message: No chat IDs in the list.")
        return False

    overall_success = True
    for chat_id in chat_id_list:
        try:
            url = f"https://api.telegram.org/bot{config['telegram_bot_token']}/sendMessage"
            data = {
                'chat_id': chat_id,
                'text': message,
                'parse_mode': 'Markdown'
            }

            response = requests.post(url, json=data)
            if response.status_code != 200:
                logger.error(f"Failed to send message to chat_id {chat_id}: Status {response.status_code} - {response.text}")
                overall_success = False
            else:
                logger.info(f"Message sent successfully to chat_id {chat_id}")

        except Exception as e:
            logger.error(f"Exception while sending message to chat_id {chat_id}: {e}")
            overall_success = False

    return overall_success

send_telegram_message("Test message")