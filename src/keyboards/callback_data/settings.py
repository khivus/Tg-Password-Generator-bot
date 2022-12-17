from aiogram.filters.callback_data import CallbackData

from src.enums import SettingType


class SettingsCallbackData(CallbackData, prefix='generate'):
    type: SettingType
