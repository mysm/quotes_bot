from typing import Set
import asyncio

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from parse_quotes import get_random_quote


class QuotesStates(StatesGroup):
    gettime = State()
    running = State()


async def quotes_every_half_hour(bot, user_id, time_in_minutes=30):
    while True:
        quotes_data = get_random_quote(True)
        await bot.send_message(
            user_id,
            f'{quotes_data["quotes"]}\nАвтор: {quotes_data["author"]}',
        )
        await asyncio.sleep(time_in_minutes * 60)


async def quotes_cancel(user_id):
    tasks: Set[asyncio.Task] = asyncio.all_tasks()
    [task.cancel() for task in tasks if task.get_name() == str(user_id)]


async def quotes_start(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await state.update_data(user_id=user_id)
    await state.set_state(QuotesStates.gettime)
    await message.reply("Введите время отправки цитаты в минутах (5-1440)")


async def quotes_process(message: types.Message, state: FSMContext):
    try:
        time_in_minutes = int(message.text)
        if time_in_minutes < 5 or time_in_minutes > 1440:
            time_in_minutes = 30
    except ValueError:
        time_in_minutes = 30
    await message.answer(f"Время отправки цитаты: {time_in_minutes} минут")
    user_id = message.from_user.id
    await state.update_data(user_id=user_id)
    loop = asyncio.get_event_loop()
    loop.create_task(
        quotes_every_half_hour(message.bot, user_id, time_in_minutes), name=str(user_id)
    )
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
    dp.register_message_handler(quotes_process, state=QuotesStates.gettime)
    dp.register_message_handler(quotes_now, commands="now", state="*")
