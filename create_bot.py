import types

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

#memory storage for use states group
storage = MemoryStorage()

bot = Bot(token="TOKEN")

dp = Dispatcher(bot, storage=storage)

