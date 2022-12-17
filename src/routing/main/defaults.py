from aiogram import types
from aiogram.filters import Command

from src.models import Settings
from src.routers import main_router


@main_router.message(Command("defaults"))
async def process_defaults(message: types.Message) -> None:
    settings = await Settings.get(user_id=message.from_user.id)
    settings.complexity = 4
    settings.separator = None
    settings.use_number = True
    await settings.save()

    await message.answer('All settings reset to defaults.')
