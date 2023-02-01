from aiogram import types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from src.models import Settings
from src.routers import main_router


@main_router.message(Command("defaults"))
async def process_defaults(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is not None:
        await state.clear()

    settings = await Settings.get(user_id=message.from_user.id)
    settings.complexity = 4
    settings.length = 16
    settings.separator = None
    settings.use_number = True
    await settings.save()

    await message.answer('All settings reset to defaults.')
