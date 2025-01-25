from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from src import container

router: Router = Router()


@router.message(CommandStart())
async def start(message: Message, con=container):
    msg = await message.answer(
        'Добро пожаловать в Badge Digital!'
        'Пожалуйста расскажите, что вас интересует.'
        '\n\n Для этого просто напишите или отправьте аудио'
        '\n\nБольше о нас на нашем сайте:',
        reply_markup=con.keyboards.start_inline_keyboard()
    )

    await message.bot.pin_chat_message(chat_id=message.chat.id, message_id=msg.message_id)
