from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from quotes import quotes_cancel

async def cmd_start(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(
        "Привет, я бот-цитатник: /quotes - цитата через заданное время, /now - цитата сейчас.",
        reply_markup=types.ReplyKeyboardRemove(),
    )


async def cmd_cancel(message: types.Message, state: FSMContext):
    await quotes_cancel(message.from_user.id)
    await state.finish()
    await message.answer(
        "Действие отменено", reply_markup=types.ReplyKeyboardRemove()
    )


def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands="start", state="*")
    dp.register_message_handler(cmd_cancel, commands="cancel", state="*")
    dp.register_message_handler(
        cmd_cancel, Text(equals="отмена", ignore_case=True), state="*"
    )
