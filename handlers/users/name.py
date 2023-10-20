from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ContentType, Contact

from loader import dp
from states.name_state import FullnameState


@dp.message_handler(state=FullnameState.waiting, content_types=ContentType.TEXT)
async def contact_required(message: Message, state: FSMContext):
    if 2 <= len(message.text.split(' ')) <= 3:
        l = len(message.text)
        if l < 7 or l > 25:
            await message.reply("Ismingizni to'g'ri kiriting, iltimos!")
        else:
            await message.reply("Rahmat, ma'lumotlaringiz qabul qilindi!\nBotdan bemmalol foydalanishingiz mumkin!")
            await state.finish()
    else:
        await message.reply("Ismingizni to'g'ri kiriting, iltimos!")


@dp.message_handler(state=FullnameState.waiting)
async def contact_required(message: Message):
    await message.reply("To'liq ismingizni jo'nating, iltimos!")
