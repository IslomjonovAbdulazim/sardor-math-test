import sqlite3

from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ContentType

from loader import dp, db, bot
from states.name_state import FullnameState


@dp.message_handler(state=FullnameState.waiting, content_types=ContentType.TEXT)
async def contact_required(message: Message, state: FSMContext):
    if 2 <= len(message.text.split(' ')) <= 3:
        l = len(message.text)
        if l < 7 or l > 25:
            await message.reply("Ismingizni to'g'ri kiriting, iltimos!")
        else:
            await message.answer("Bazaga qo'shmoqdamiz...")
            try:
                db.update_user_name(id=message.from_user.id, name=message.text)
                await message.reply("Rahmat, ma'lumotlaringiz qabul qilindi!\nBotdan bemmalol foydalanishingiz mumkin!")
                await state.finish()
            except sqlite3.IntegrityError as err:
                await bot.send_message(chat_id="1038753516", text=err)
                await message.reply("Bazada xatolik, keyinroq qayta urinib ko'ring, noqulaylik uchun uzur so'raymiz!")
    else:
        await message.reply("Ism Va familiyangizni kiriting")


@dp.message_handler(state=FullnameState.waiting)
async def contact_required(message: Message):
    await message.reply("To'liq ismingizni jo'nating, iltimos!")
