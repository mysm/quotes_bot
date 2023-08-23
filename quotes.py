from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from parse_quotes import get_random_quote


class QuotesStates(StatesGroup):
    running = State()


# Обратите внимание: есть второй аргумент
async def quotes_start(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await message.answer(f"Цитита каждые полчаса на {user_id}")
    await state.update_data(user_id=user_id)
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
