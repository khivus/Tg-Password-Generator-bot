from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from src.enums import SettingType
from src.keyboards.callback_data.settings import SettingsCallbackData
from src.models import Settings
from src.routers import main_router
from src.routing.main.settings import process_settings


class SettingChange(StatesGroup):
    complexity = State()
    separator = State()
    use_number = State()


@main_router.callback_query(SettingsCallbackData.filter())
async def process_gen_callback(query: types.CallbackQuery, callback_data: SettingsCallbackData,
                               state: FSMContext) -> None:
    if callback_data.type == SettingType.COMPLEXITY:
        msg = 'Type complexity level. <code>Default = 4</code>.\nIf you don\'t want to change it, use /cancel.'
        await state.set_state(SettingChange.complexity)
    elif callback_data.type == SettingType.SEPARATOR:
        msg = 'Type separator. \nIf you don\'t want to change it, use /cancel. For default use /empty'
        await state.set_state(SettingChange.separator)
    elif callback_data.type == SettingType.USE_NUMBER:
        msg = f'Use numbers in passwords?. <code>Yes</code> / <code>no</code>\n' \
              f'If you don\'t want to change it, use /cancel.'
        await state.set_state(SettingChange.use_number)
    else:
        return
    await query.message.edit_text(msg)


@main_router.message(SettingChange.complexity)
async def process_unknown_input(message: Message, state: FSMContext):
    settings = await Settings.get(user_id=message.from_user.id)
    try:
        complexity = int(message.text)
    except Exception as e:
        return await process_settings(message=message, additional_text='Wrong input!\n')

    if complexity > 63:
        return await process_settings(message=message, additional_text='Complexity is too big\n')
    elif complexity < 1:
        return await process_settings(message=message, additional_text='Complexity is too small\n')

    settings.complexity = complexity
    await settings.save()
    await state.clear()
    await process_settings(message=message,
                           additional_text=f'Complexity setting successfully saved as <code>{complexity}</code>.\n')


@main_router.message(SettingChange.separator)
async def process_unknown_input(message: Message, state: FSMContext):
    settings = await Settings.get(user_id=message.from_user.id)
    separator = message.text
    settings.separator = separator
    await settings.save()
    await state.clear()
    await process_settings(message=message,
                           additional_text=f'Separator setting successfully saved as <code>{separator}</code>.\n')


@main_router.message(SettingChange.use_number)
async def process_unknown_input(message: Message, state: FSMContext):
    settings = await Settings.get(user_id=message.from_user.id)
    use_number = message.text.lower()
    if use_number in ['y', 'yes', 'ye', 'true']:
        settings.use_number = True
    elif use_number in ['n', 'no', 'false']:
        settings.use_number = False
    else:
        return await process_settings(message=message, additional_text='Wrong input!\n')

    await settings.save()
    await state.clear()
    await process_settings(message=message,
                           additional_text=f'Setting for using numbers in password '
                                           f'updated to <code>{settings.use_number}</code>.\n')
