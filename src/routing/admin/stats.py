import datetime

from aiogram import types
from aiogram.filters import Command
from tortoise.functions import Sum

from src.constants import bot, version
from src.models import User
from src.routers import admin_router


async def calculate(field: str):
    response = await User.all().annotate(**{field: Sum(field)}).values(field)

    return response[0].get(field, 0)


@admin_router.message(Command("stats"))
async def process_stats(message: types.Message):
    db_file_path = 'resources/db.sqlite'
    tnow = datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=+3.0)))
    new_file_name = f'backup_{tnow.day:02}_{tnow.month:02}_{tnow.year}.sqlite'
    
    file = types.FSInputFile(f'{db_file_path}', f'{new_file_name}')
    users = await User.all().count()
    generations = await calculate('generations')

    msg = f'Bot version: <code>{version}</code>\n' \
        f'Statistics:\n' \
        f'Users: <code>{users}</code>\n' \
        f'Generations: <code>{generations}</code>\n'

    await message.answer_document(caption=msg, document=file)
