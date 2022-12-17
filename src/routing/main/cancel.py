from aiogram import types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from src.routers import main_router


@main_router.message(Command("cancel"))
async def process_cancel(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is not None:
        await state.clear()
        await message.answer('All states cleared.')
    else:
        await message.answer('Nothing to cancel...')
