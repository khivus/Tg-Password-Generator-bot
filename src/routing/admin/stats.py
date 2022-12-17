from aiogram import types
from aiogram.filters import Command
from tortoise.functions import Sum

from src.constants import version
from src.models import Statistics, User
from src.routers import admin_router


async def calculate(field: str):
    response = await Statistics.all().annotate(**{field: Sum(field)}).values(field)

    return response[0].get(field, 0)


@admin_router.message(Command("stats"))
async def process_stats(message: types.Message):
    users = await User.all().count()
    human = await calculate('generation_human')
    # non_human = await calculate('generation_non_human')
    # numbers_only = await calculate('generation_numbers_only')

    await message.answer(
        text=
        f'Bot version: <code>{version}</code>\n'
        f'Statistics:\n'
        f'Users: <code>{users}</code>\n'
        f'Generations: <code>{human}</code>\n'
        # f'Non human generations: <code>{non_human}</code>\n'
        # f'Numbers only generations: <code>{numbers_only}</code>\n'
    )
