from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.enums import GenerationType
from src.keyboards.callback_data.generate import GenerateCallbackData


def build_gen_keyboard():
    builder = InlineKeyboardBuilder()

    builder.button(text='Readable', callback_data=GenerateCallbackData(type=GenerationType.HUMAN))
    builder.button(text='Unreadable', callback_data=GenerateCallbackData(type=GenerationType.NON_HUMAN))

    return builder.as_markup()
