# common.py
import os
import logging
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

config = {
    'api_ninjas_key': os.getenv('API_NINJAS_KEY'),
    'perplexity_api_key': os.getenv('PERPLEXITY_API_KEY'),
    'telegram_bot_token': os.getenv('TELEGRAM_BOT_TOKEN'),
    'telegram_chat_id': os.getenv('TELEGRAM_CHAT_ID')
}
