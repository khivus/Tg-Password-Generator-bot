from aiogram import types
from aiogram.filters import Command

from src.models import User, Settings, Statistics
from src.routers import main_router


@main_router.message(Command("start"))
async def process_start(message: types.Message) -> None:
    await Statistics.get_or_create(user_id=message.from_user.id, defaults={})
    user, _ = await User.get_or_create(telegram_id=message.from_user.id)
    await Settings.get_or_create(user=user, defaults={})

    await message.answer(
        text=
        f'Hello! I\'m bot that generates passwords for you.\n'
        f'This bot <b>does not</b> save your passwords! '
        f'You can get readable and unreadable passwords by using /gen command. Also you can set up settings for '
        f'your preferences by using /settings command.\n'
        f'Contact @khivus for suggestions and questions.\n'
        f'<b>Thanks for using me!</b>'
    )
