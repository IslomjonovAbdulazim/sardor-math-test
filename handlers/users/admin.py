from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentType

from data.config import ADMINS
from loader import dp, test
from states.answer_state import AnswersState
from states.image import ImageState


@dp.message_handler(text="/new_test", user_id=ADMINS)
async def new_test(message: types.Message):
    await message.reply("Avvalo test rasmlarini jo'nating, to'xtatish uchun <b>stop</b> so'zini yozing")
    await ImageState.waiting.set()


@dp.message_handler(state=ImageState.waiting, content_types=ContentType.PHOTO)
async def set_mages(message: types.Message, state: FSMContext):
    data = await state.get_data()
    id = f"{message.photo[-1].file_id},"
    if data.get('data') is not None:
        print(data.get('data'))
        res = data.get('data') + id
    else:
        res = id
    await state.set_data({
        "data": res
    })


@dp.message_handler(state=ImageState.waiting, content_types=ContentType.TEXT)
async def close(message: types.Message, state: FSMContext):
    if message.text.lower() == "stop":
        c = test.count_users()
        count = len(c) + 1 if c is not None else 1
        d = (await state.get_data("data")).get("data")
        print(d)
        print(count)
        print(f"count {count}, data: {d} {d is str}")
        test.add_user(id=count, media=d, answers="No data")
        await AnswersState.waiting.set()
        await message.reply(
            "Endi esa javoblarni kiritib chiqamiz, ketma ketlikda kalitlarni kiritib keta verasiz. <b>abdcebcd</b> tariqasida.")
    else:
        await message.answer("To'xtatish uchun <b>stop</b> so'zini yozing")


@dp.message_handler(state=ImageState.waiting)
async def type_error(message: types.Message):
    await message.reply("Rasmdan boshqa file turi qabul qilinmaydi")


@dp.message_handler(state=AnswersState.waiting, content_types=ContentType.TEXT)
async def answers(message: types.Message, state: FSMContext):
    res = message.text.lower().replace("a", "").replace("b", "").replace("c", "").replace("d", "").replace("e", "")
    print(f"res: {res}")
    if len(res) == 0:
        c = test.count_users()
        id = len(c) + 1 if c is not None else 1
        test.update_user_answers(answers=message.text, id=id)
        await message.reply(f"Test <b>codi: {id}</b>\n\n@sardor_math_test_bot-testni ushbu botda yeching!")
        await state.finish()
    else:
        await message.answer("Testda faqat <b>'a,b,c,d,e'</b> kalitlarini kiritish mumkin")