from aiogram import types

from src import generate
from src.enums import GenerationType
from src.keyboards.callback_data.generate import GenerateCallbackData
from src.keyboards.gen import build_gen_keyboard
from src.models import Settings, User
from src.routers import main_router


@main_router.callback_query(GenerateCallbackData.filter())
async def process_gen_callback(query: types.CallbackQuery,
                               callback_data: GenerateCallbackData) -> None:
    keyboard = build_gen_keyboard()
    user = await User.get(telegram_id=query.from_user.id)
    settings = await Settings.get(user_id=query.from_user.id)

    if callback_data.type is GenerationType.HUMAN:
        password = generate.generate_pass_human(complexity=settings.complexity, separator=settings.separator, use_number=settings.use_number)
    elif callback_data.type is GenerationType.NON_HUMAN:
        password = generate.generate_pass_non_human(length=settings.length, use_number=settings.use_number, separator=settings.separator, use_upper=settings.use_upper, use_lower=settings.use_lower)
    else:
        return
    
    user.generations += 1
    await user.save()
    await query.message.edit_text(text=f'<code>{password}</code>', reply_markup=keyboard)
