from aiogram import types
from aiogram.filters import Command
from tortoise.functions import Sum

from src.constants import version
from src.models import User
from src.routers import admin_router


async def calculate(field: str):
    response = await User.all().annotate(**{field: Sum(field)}).values(field)

    return response[0].get(field, 0)


@admin_router.message(Command("stats"))
async def process_stats(message: types.Message):
    users = await User.all().count()
    generations = await calculate('generations')

    await message.answer(
        text=
        f'Bot version: <code>{version}</code>\n'
        f'Statistics:\n'
        f'Users: <code>{users}</code>\n'
        f'Generations: <code>{generations}</code>\n'
    )
