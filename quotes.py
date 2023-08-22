from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


class QuotesStates(StatesGroup):
    running = State()


# Обратите внимание: есть второй аргумент
async def quotes_start(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await message.answer(f"Цитита каждые полчаса на {user_id}")
    await state.update_data(user_id=user_id)
    await state.set_state(QuotesStates.running)


async def quotes_now(message: types.Message, state: FSMContext):
    await message.answer("Цитита сейчас")


def register_handlers_quotes(dp: Dispatcher):
    dp.register_message_handler(quotes_start, commands="quotes", state="*")
    dp.register_message_handler(quotes_now, commands="now", state="*")
