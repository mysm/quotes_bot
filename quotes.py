from typing import Set
import asyncio

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from parse_quotes import get_random_quote


class QuotesStates(StatesGroup):
    running = State()


async def quotes_every_half_hour(bot, user_id):
    while True:
        quotes_data = get_random_quote(True)
        await bot.send_message(
            user_id,
            f'{quotes_data["quotes"]}\nАвтор: {quotes_data["author"]}',
        )
        await asyncio.sleep(1800)


async def quotes_cancel():
    tasks: Set[asyncio.Task] = asyncio.all_tasks()
    [task.cancel() for task in tasks]


async def quotes_start(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await state.update_data(user_id=user_id)
    loop = asyncio.get_event_loop()
    loop.create_task(quotes_every_half_hour(message.bot, user_id))
    await state.set_state(QuotesStates.running)


async def quotes_now(message: types.Message, state: FSMContext):
    # data = await state.get_data()
    quotes_data = get_random_quote(True)

    await message.answer(
        f"{quotes_data['quotes']}\nАвтор: {quotes_data['author']}",
        parse_mode=types.ParseMode.HTML,
    )


def register_handlers_quotes(dp: Dispatcher):
    dp.register_message_handler(quotes_start, commands="quotes", state="*")
    dp.register_message_handler(quotes_now, commands="now", state="*")
