from aiogram import types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from src.models import Settings
from src.routers import main_router


@main_router.message(Command("empty"))
async def process_empty(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is not None:
        await message.answer(f'Separator is reset to default.')
        settings = await Settings.get(user_id=message.from_user.id)
        settings.separator = None
        await settings.save()
    else:
        await message.answer('What is empty?')
    await state.clear()
