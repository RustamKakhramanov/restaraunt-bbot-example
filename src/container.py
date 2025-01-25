from src.bot.utils.keyboards import Keyboards
from src.config import settings
from src.services.openai_worker import OpenAIWorker
from whatsapp_chatbot_python import (
    BaseStates,
    GreenAPIBot,
    Notification,
    filters,
)

openai_worker: OpenAIWorker = OpenAIWorker(
    'gpt-3.5-turbo',
    'user_history.json',
    settings.OPENAI_API_KEY,
    settings.OPENAI_ORGANIZATION,
    settings.OPENAI_PROJECT
)


wb_bot: GreenAPIBot = GreenAPIBot(settings.WB_BOT_ID,  settings.WB_API_KEY)

keyboards: Keyboards = Keyboards()
