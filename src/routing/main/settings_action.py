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
    length = State()


@main_router.callback_query(SettingsCallbackData.filter())
async def process_gen_callback(query: types.CallbackQuery, callback_data: SettingsCallbackData,
                               state: FSMContext):
    reply_markup = None

    settings = await Settings.get(user_id=query.from_user.id)

    if callback_data.type == SettingType.COMPLEXITY:
        msg = 'Type complexity level. <code>Default = 4</code>.\n' \
              'Maximum complexity is 32 and minimum is 1.\n' \
              'If you don\'t want to change it, use /cancel.' \
              'Complexity is used only for "readable" method.'
        await state.set_state(SettingChange.complexity)
        
    elif callback_data.type == SettingType.LENGTH:
        msg = 'Type length for password. <code>Default = 16</code>.\n' \
              'Maximum complexity is 128 and minimum is 1.\n' \
              'If you don\'t want to change it, use /cancel.\n' \
              'Length is used only for "numbers" and "non-readable" methods.'
        await state.set_state(SettingChange.length)

    elif callback_data.type == SettingType.SEPARATOR:
        msg = 'Type separator. \n' \
              'If you don\'t want to change it, use /cancel. For default use /empty.'
        await state.set_state(SettingChange.separator)

    elif callback_data.type == SettingType.USE_NUMBER:
        settings.use_number = not settings.use_number
        reply_markup = build_settings_keyboard()
        msg = get_text(additional_text=f'Use number changed to {settings.use_number}.\n', settings=settings)

    elif callback_data.type == SettingType.RESET:
        settings.complexity = 4
        settings.length = 16
        settings.separator = None
        settings.use_number = True

        reply_markup = build_settings_keyboard()
        msg = get_text(additional_text=f'All settings reset to defaults.\n', settings=settings)
    else:
        return

    await settings.save()

    try:
        await query.message.edit_text(msg, reply_markup=reply_markup)
    except:
        await query.answer(text='Data has been updated')


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

    if complexity > 32:
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


@main_router.message(SettingChange.length)
async def process_unknown_input(message: Message, state: FSMContext):
    await state.clear()
    keyboard = build_settings_keyboard()
    settings = await Settings.get(user_id=message.from_user.id)
    try:
        length = int(message.text)
    except:
        text = get_text(settings=settings, additional_text='Wrong input!\n')
        return await message.answer(text=text, reply_markup=keyboard)

    if length > 128:
        text = get_text(settings=settings, additional_text='Length is too big!\n')
        return await message.answer(text=text, reply_markup=keyboard)
    elif length < 1:
        text = get_text(settings=settings, additional_text='Length is too small!\n')
        return await message.answer(text=text, reply_markup=keyboard)

    settings.length = length
    await settings.save()
    text = get_text(settings=settings,
                    additional_text=f'Length setting successfully saved as <code>{length}</code>.\n')
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
