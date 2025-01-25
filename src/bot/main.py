from re import IGNORECASE
from whatsapp_chatbot_python import (
    BaseStates,
    GreenAPIBot,
    Notification,
    filters,
)
from ..services.openai_worker import OpenAIWorker
from ..services.recognizer import transcrible
from ..container import openai_worker as ai_worker, wb_bot as bot


class States(BaseStates):
    ACTIVE = 'active'
    LANGUAGE_SET = 'lang_set'


@bot.router.message(type_message=filters.TEXT_TYPES,
                    state=None)
def message_handler(notification: Notification) -> None:
    notification.state_manager.update_state(notification.sender,
                                            States.ACTIVE.value)

    if (notification.event["messageData"]['typeMessage'] == 'extendedTextMessage'):
        text = notification.event["messageData"]['extendedTextMessageData']['text']
    else:
        text = notification.event["messageData"]['textMessageData']['textMessage']

    answer = ai_worker.get_product_info(text, notification.chat)
    notification.answer(answer)


@bot.router.message(type_message='audioMessage', state=None)
def message_handler(notification: Notification) -> None:
    text = transcrible(
        notification.event["messageData"]['fileMessageData']['downloadUrl']
    )
    # print(text)
    answer = ai_worker.get_product_info(text, notification.chat)
    notification.answer(answer)


try:
    bot.run_forever()
except ():
    pass


# print(ai_worker.get_product_info('213121', '77711698945@c.us'))
