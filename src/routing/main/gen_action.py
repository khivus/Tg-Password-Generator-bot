from aiogram import types

from src import generate
from src.enums import GenerationType
from src.keyboards.callback_data.generate import GenerateCallbackData
from src.keyboards.gen import build_gen_keyboard
from src.models import Settings, Statistics
from src.routers import main_router


@main_router.callback_query(GenerateCallbackData.filter())
async def process_gen_callback(query: types.CallbackQuery,
                               callback_data: GenerateCallbackData) -> None:
    keyboard = build_gen_keyboard()
    settings = await Settings.get(user_id=query.from_user.id)
    stats = await Statistics.get(user_id=query.from_user.id)
    if callback_data.type is GenerationType.HUMAN:
        password = generate.generate_pass_human(complexity=settings.complexity, separator=settings.separator,
                                                use_number=settings.use_number)
    elif callback_data.type is GenerationType.NON_HUMAN:
        password = generate.generate_pass_non_human(complexity=settings.complexity, use_number=settings.use_number)
    elif callback_data.type is GenerationType.NUMBERS_ONLY:
        password = generate.generate_pass_numbers_only(complexity=settings.complexity)
    else:
        return
    stats.generation_human += 1
    await stats.save()
    await query.message.edit_text(text=f'Generated password: <code>{password}</code>', reply_markup=keyboard)
