from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    await message.answer("Testni jo'natish formati: \n<b>[tes codi]*[test javoblari]</b> \nmisol uchun <b>5*abc</b>",
                         protect_content=True)
