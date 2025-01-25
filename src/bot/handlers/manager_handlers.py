from aiogram.enums import ContentType, ParseMode

from src import container

from aiogram import Router, F
from aiogram.types import Message
from aiogram.types import CallbackQuery
from aiogram.types import FSInputFile

from src.bot.bot import bot
from src.services.recognizer import transcrible

router: Router = Router()


@router.callback_query(F.data == 'кп')
async def send_kp(callback_query: CallbackQuery):
    # Отправляем сообщение "КП" при нажатии кнопки
    await send_kp(callback_query.message)


async def send_kp(message: Message):
    document = FSInputFile(
        'src/storage/files/ChatBot_KP.pdf',
        "КП чат-бот.pdf",
    )
    await message.bot.send_document(message.chat.id, document)


@router.message(F.text)
async def text_help(message: Message, con=container):
    # Если текст сообщения содержит одно из ключевых слов
    keywords = ['кп', 'кпп', 'коммерческое']
    if any(keyword in message.text.lower() for keyword in keywords):
        try:
            # Открываем файл в бинарном режиме и передаем его как InputFile

            await send_kp(message)
            await message.delete()
        except Exception as e:
            await message.reply(f"Наш менеджер сформирует КП в ближайшее время и отправит вам его в личные сообщения")
    else:
        # Обработка других текстов
        answer: str = await con.openai_worker.get_product_info(
            query=message.text,
            user=message.from_user.id
        )
        await message.answer(answer, parse_mode=ParseMode.MARKDOWN)


@router.message(F.content_type.in_({'voice'}))
async def voice_help(message: Message, con=container):
    file_id = message.voice.file_id
    file_info = await bot.get_file(file_id)
    file_path = file_info.file_path
    file_url = f"https://api.telegram.org/file/bot{bot.token}/{file_path}"
    query = transcrible(file_url)

    answer: str = await con.openai_worker.get_product_info(
        query=query,
        user=message.from_user.id
    )

    await message.answer(answer, parse_mode=ParseMode.MARKDOWN)
