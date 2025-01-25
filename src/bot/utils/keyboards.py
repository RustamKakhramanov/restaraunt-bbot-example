from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class Keyboards:

    @classmethod
    def start_inline_keyboard(cls):
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(
                    text='Badge Company', url='http://badge-digital.com')],
                [InlineKeyboardButton(
                    text='ИИ-чат бот, КП', callback_data='кп')],
            ]
        )
