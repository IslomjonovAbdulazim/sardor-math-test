from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from keyboards.default.contact import contact_btn
from loader import dp
from states.contact import ContactState


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(
        f"Salom, <b>{message.from_user.full_name}</b>!\nBazaga qo'shishimiz uchun avvalo sizning telefon raqamingiz kerak bo'ladi. \n<b>Pastdagi tugmani bosib</b> <b>kontaktingizni</b> jo'nating, iltimos!",
        protect_content=True, reply_markup=contact_btn)
    await ContactState.waiting.set()
