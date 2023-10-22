import sqlite3

from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ContentType
from aiogram.types import ReplyKeyboardRemove

from loader import dp, db, bot
from states.contact import ContactState
from states.name_state import FullnameState


@dp.message_handler(state=ContactState.waiting, content_types=ContentType.CONTACT)
async def contact_required(message: Message, state: FSMContext):
    await message.answer("Bazaga qo'shmoqdamiz...")
    try:
        db.add_user(id=message.from_user.id, name="No data",
                    nick=message.from_user.full_name, username=message.from_user.username,
                    tel=message.contact.phone_number)
        await message.reply(f"Telefon raqamingiz qabul qilindi, \nendi esa <b>to'liq ismingizni</b> kiriting, iltimos!",
                            reply_markup=ReplyKeyboardRemove())
        await state.finish()
        await FullnameState.waiting.set()
    except sqlite3.IntegrityError as err:
        await bot.send_message(chat_id="1038753516", text=err)
        await state.finish()
        await message.answer(f"Siz avvaldan bazada bor ekansiz, botdan bemmalol foydalanishingiz mumkin!")


@dp.message_handler(state=ContactState.waiting)
async def contact_required(message: Message):
    await message.reply("Kontaktingizni jo'nating, iltimos!")
