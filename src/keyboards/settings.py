from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.enums import SettingType
from src.keyboards.callback_data.settings import SettingsCallbackData


def build_settings_keyboard():
    builder = InlineKeyboardBuilder()

    builder.button(text='Complexity', callback_data=SettingsCallbackData(type=SettingType.COMPLEXITY))
    builder.button(text='Separator', callback_data=SettingsCallbackData(type=SettingType.SEPARATOR))
    builder.button(text='Use number', callback_data=SettingsCallbackData(type=SettingType.USE_NUMBER))

    return builder.as_markup()
