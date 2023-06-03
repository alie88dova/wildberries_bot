import datetime
import sqlite3
from create_bot import bot, dp
from aiogram import types, Dispatcher
from aiogram.types import ContentType
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from wb_parse_tools import Card


class CardData(StatesGroup):
    article = State()
    search_input = State()


async def start_msg(msg: types.Message):
    await bot.send_message(msg.from_user.id,
                           "Добро пожаловать в бота для остеживания позиции вашей карточки по запросу\n"
                           "/search - для начала поиска")


async def start_search(msg: types.Message, state: FSMContext ):
    await state.finish()
    await bot.send_message(msg.from_user.id, "Пожалйста пришлите артикул вашего товара")
    await CardData.article.set()


async def get_article(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['article'] = msg.text
        await bot.send_message(msg.from_user.id,
                        f"Ваш артикул = {msg.text}\n"
                        f"пришлите запрос по которому можно найти карточку (Т.к. процесс"
                        f"достаточно долгий убидительная просьба писать запрос по которому можно найт итовар данного типа"
                         )
        await CardData.search_input.set()


async def get_search_input(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['search_input'] = msg.text
        bot.send_message(msg.from_user.id,
                         f"Ваш поисковой = {msg.text}\n"
                         f"Когда поиск будет завершен мы пришлем вам ответ"
                         )
        await CardData.search_input.set()
        card = Card(data['search_input'], data['article'])
        card.check_correct_article()
        card.find_position_by_article()

        position = card.get_possition

        await bot.send_message(
            msg.from_user.id,
            f"Позиция вашей карточки\n"
            f"Столбец {position[0]}\n"
            f"Строка {position[1]}\n"
            f"Страница {position[2]}"
        )


def register_handlers_user(dp: Dispatcher):
    dp.register_message_handler(start_msg, commands=["start"])
    dp.register_message_handler(start_search, commands=["search"], state="*")
    dp.register_message_handler(get_article, state=CardData.article)
    dp.register_message_handler(get_search_input, state=CardData.search_input)


