from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from src.enums import SettingType
from src.keyboards.callback_data.settings import SettingsCallbackData
from src.keyboards.settings import build_settings_keyboard
from src.models import Settings
from src.routers import main_router
from src.routing.main.settings import get_text


class SettingChange(StatesGroup):
    complexity = State()
    separator = State()


@main_router.callback_query(SettingsCallbackData.filter())
async def process_gen_callback(query: types.CallbackQuery, callback_data: SettingsCallbackData,
                               state: FSMContext):
    reply_markup = None

    settings = await Settings.get(user_id=query.from_user.id)

    if callback_data.type == SettingType.COMPLEXITY:
        msg = 'Type complexity level. <code>Default = 4</code>.\n' \
              'Maximum complexity is 48 and minimum is 1.\n' \
              'If you don\'t want to change it, use /cancel.'
        await state.set_state(SettingChange.complexity)
    elif callback_data.type == SettingType.SEPARATOR:
        msg = 'Type separator. \n' \
              'If you don\'t want to change it, use /cancel. For default use /empty.'
        await state.set_state(SettingChange.separator)
    elif callback_data.type == SettingType.USE_NUMBER:
        settings.use_number = not settings.use_number

        reply_markup = build_settings_keyboard()
        msg = get_text(additional_text=f'Use number changed to {settings.use_number}.\n', settings=settings)
    else:
        return

    await settings.save()

    await query.message.edit_text(msg, reply_markup=reply_markup)


@main_router.message(SettingChange.complexity)
async def process_unknown_input(message: Message, state: FSMContext):
    await state.clear()
    keyboard = build_settings_keyboard()
    settings = await Settings.get(user_id=message.from_user.id)
    try:
        complexity = int(message.text)
    except:
        text = get_text(settings=settings, additional_text='Wrong input!\n')
        return await message.answer(text=text, reply_markup=keyboard)

    if complexity > 48:
        text = get_text(settings=settings, additional_text='Complexity is too big!\n')
        return await message.answer(text=text, reply_markup=keyboard)
    elif complexity < 1:
        text = get_text(settings=settings, additional_text='Complexity is too small!\n')
        return await message.answer(text=text, reply_markup=keyboard)

    settings.complexity = complexity
    await settings.save()
    text = get_text(settings=settings,
                    additional_text=f'Complexity setting successfully saved as <code>{complexity}</code>.\n')
    await message.answer(text=text, reply_markup=keyboard)


@main_router.message(SettingChange.separator)
async def process_unknown_input(message: Message, state: FSMContext):
    await state.clear()
    keyboard = build_settings_keyboard()
    settings = await Settings.get(user_id=message.from_user.id)
    separator = message.text
    settings.separator = separator
    await settings.save()
    text = get_text(settings=settings,
                    additional_text=f'Separator setting successfully saved as <code>{separator}</code>.\n')
    await message.answer(text=text, reply_markup=keyboard)
