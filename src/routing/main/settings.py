from aiogram import types
from aiogram.filters import Command

from src.keyboards.settings import build_settings_keyboard
from src.models import Settings
from src.routers import main_router


def get_text(settings: Settings, additional_text: str = ''):
    text = f'{additional_text}' \
           f'Your current settings:\n' \
           f'<code>Complexity</code> = {settings.complexity}\n' \
           f'<code>Separator</code> = {settings.separator or "Default"}\n' \
           f'<code>Use number</code> = {settings.use_number}\n' \
           f'Choose setting to change.'
    return text


@main_router.message(Command("settings"))
async def process_settings(message: types.Message) -> None:
    settings = await Settings.get(user_id=message.from_user.id)
    
    keyboard = build_settings_keyboard()
    text = get_text(settings=settings)

    await message.answer(text=text, reply_markup=keyboard)
