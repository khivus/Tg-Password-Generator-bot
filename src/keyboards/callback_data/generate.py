from aiogram.filters.callback_data import CallbackData

from src.enums import GenerationType


class GenerateCallbackData(CallbackData, prefix='generate'):
    type: GenerationType
