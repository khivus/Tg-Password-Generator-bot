from aiogram import types
from aiogram.filters import Command

from src.keyboards.gen import build_gen_keyboard
from src.routers import main_router


@main_router.message(Command("gen"))
async def process_gen(message: types.Message) -> None:
    keyboard = build_gen_keyboard()
    await message.answer("Choose generation way.", reply_markup=keyboard)
