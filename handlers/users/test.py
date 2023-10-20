from aiogram import types
from loader import dp


@dp.message_handler()
async def test(message: types.Message):
    await message.answer("Salom")
