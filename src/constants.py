from aiogram import Bot, Dispatcher

from src.config import Config

config = Config()
bot = Bot(token=config.API_TOKEN, parse_mode='HTML')
dp = Dispatcher()

version = 'v1.41'
admin_id = 897276284

TORTOISE_CONFIG = {
    'connections': {'default': 'sqlite://resources//db.sqlite'},
    'apps': {
        'models': {
            'models': ['src.models'],
            'default_connection': 'default'
        }
    }
}
