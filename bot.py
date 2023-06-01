from aiogram.utils import executor
from create_bot import dp
from handlers import user
import asyncio
from aiogram.contrib.fsm_storage.memory import MemoryStorage


async def on_startup(_):
    print('Бот онлайн')

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

