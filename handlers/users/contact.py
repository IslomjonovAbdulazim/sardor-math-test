from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ContentType, Contact
from aiogram.types import ReplyKeyboardRemove

from loader import dp
from states.contact import ContactState
from states.name_state import FullnameState


@dp.message_handler(state=ContactState.waiting, content_types=ContentType.CONTACT)
async def contact_required(message: Message, state: FSMContext):
    await message.reply(f"Telefon raqamingiz qabul qilindi, \nendi esa <b>to'liq ismingizni</b> kiriting, iltimos!",
                        reply_markup=ReplyKeyboardRemove())
    await state.finish()
    await FullnameState.waiting.set()


@dp.message_handler(state=ContactState.waiting)
async def contact_required(message: Message):
    await message.reply("Kontaktingizni jo'nating, iltimos!")
