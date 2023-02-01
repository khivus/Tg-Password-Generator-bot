from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.enums import SettingType
from src.keyboards.callback_data.settings import SettingsCallbackData


def build_settings_keyboard():
    builder = InlineKeyboardBuilder()

    builder.button(text='Complexity', callback_data=SettingsCallbackData(type=SettingType.COMPLEXITY))
    builder.button(text='Length', callback_data=SettingsCallbackData(type=SettingType.LENGTH))
    builder.button(text='Separator', callback_data=SettingsCallbackData(type=SettingType.SEPARATOR))
    builder.button(text='Use number', callback_data=SettingsCallbackData(type=SettingType.USE_NUMBER))
    builder.button(text='Reset all', callback_data=SettingsCallbackData(type=SettingType.RESET))

    builder.adjust(2, 2, 1)

    return builder.as_markup()
