import operator
from datetime import datetime

import phonenumbers
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentType

from data.config import ADMINS
from loader import dp, test, db, results
from states.answer_state import AnswersState
from states.end import EndState
from states.image import ImageState
from states.start import StartState
from states.time import TimeState
from phonenumbers import format_number


@dp.message_handler(text="/new_test", user_id=ADMINS)
async def new_test(message: types.Message):
    _d = db.select_user(id=message.from_user.id)
    if _d is None:
        await message.reply("Bazadan sizni topa olmadik. Ro'yxatdan o'ting, /start comandasining ustiga bosish orqali!")
        return
    await message.reply("Avvalo test rasmlarini jo'nating, to'xtatish uchun <b>stop</b> so'zini yozing")
    await ImageState.waiting.set()


@dp.message_handler(user_id=ADMINS)
async def admin_test(message: types.Message):
    _d = db.select_user(id=message.from_user.id)
    if _d is None:
        await message.reply("Bazadan sizni topa olmadik. Ro'yxatdan o'ting, /start comandasining ustiga bosish orqali!")
        return
    _end = False
    txt = message.text
    if txt[-1] == ".":
        _end = True
        txt = txt[:-1]
    print(f'txtttttttttttttttttttttttttttttttttttttttttttttttt {txt}a')
    _data = results.select_all_users()
    d = test.select_user(id=txt)
    if _data is not None and d is not None:
        data = []
        for d in _data:
            if str(d[5]) == txt:
                print('in')
                data.append(d)
        print(f'data: {data}')
        _sort = {}
        for res in data:
            _sort[str(res[0])] = res[1]
        _sort = dict(sorted(_sort.items(), reverse=True, key=operator.itemgetter(1)))
        result = ""
        t = 0
        for k, v in _sort.items():
            t += 1
            r = results.select_user(id=k)
            user = db.select_user(id=int(r[4]))
            num = format_number(phonenumbers.parse(user[2], "UZ"), phonenumbers.PhoneNumberFormat.INTERNATIONAL)
            percent = str(100 * r[1] / len(str(r[8]).split(',')))
            # time = ((datetime.fromtimestamp(r[7]))-(datetime.fromtimestamp(r[6]))).seconds
            # __t = datetime.fromtimestamp(time).strftime("%H:%M:%S")
            p1 = f"{t}: 👤{user[1]}\n✅{r[1]}, ❌{r[2]}, ℹ️{r[3]}, {percent[:4]}%"
            p2 = "\n\n" if _end else f"\n<tg-spoiler>🅰️@{user[5]} ☎️{str(num)[5:]}</tg-spoiler>\n\n"
            result += f"<b>{p1}{p2}</b>"
        if len(result) != 0:
            await message.reply(result)
        else:
            await message.reply("Hali bu testni heckkim ishlamagan")
    else:
        await message.reply("Test topilmadi")


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
        count = len(test.select_all_users()) + 1
        d = (await state.get_data("data")).get("data")
        print(f"count {count}\n\n\n\n\n\n\n")
        test.add_user(id=count, media=d, answers="No data", start=datetime.now(), end=datetime.now(), t=90)
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
        count = len(test.select_all_users())
        print(f"count {count}\n\n\n\n\n\n\n")
        test.update_user_answers(answers=message.text, id=count)
        await message.reply(f"Tesni boshlanish vaqtini kiriting, misol uchun: <b>17:35</b>")
        await StartState.waiting.set()
    else:
        await message.answer("Testda faqat <b>'a,b,c,d,e'</b> kalitlarini kiritish mumkin")


@dp.message_handler(state=StartState.waiting, content_types=ContentType.TEXT)
async def start(message: types.Message, state: FSMContext):
    count = len(test.select_all_users())
    print(f"count {count}\n\n\n\n\n\n\n")
    await EndState.waiting.set()
    t = message.text.split(":")
    hour = int(t[0])
    minute = int(t[1])
    st = datetime.today().replace(hour=hour, minute=minute)
    print(st.timestamp())
    test.update_user_start(id=count, time=st.timestamp())
    await message.reply("Tesni tugash vaqtini kiriting, misol uchun: <b>20:00</b>")


def hello():
    print("Salmcha\n\n\n\n\n")


@dp.message_handler(state=EndState.waiting, content_types=ContentType.TEXT)
async def end(message: types.Message, state: FSMContext):
    count = len(test.select_all_users())
    print(f"count {count}\n\n\n\n\n\n\n")
    await TimeState.waiting.set()
    t = message.text.split(":")
    hour = int(t[0])
    minute = int(t[1])
    st = datetime.today().replace(hour=hour, minute=minute)
    test.update_user_end(id=count, time=st.timestamp())
    await message.reply("Tesni davom etish daqiqasini kiriting, misol uchun <b>90</b>")


@dp.message_handler(state=TimeState.waiting, content_types=ContentType.TEXT)
async def duration(message: types.Message, state: FSMContext):
    count = len(test.select_all_users())
    print(f"count {count}\n\n\n\n\n\n\n")
    test.update_user_time(id=count, time=int(message.text))
    t = test.select_user(id=count)
    sta = datetime.fromtimestamp(t[3]).strftime("%H:%M")
    end = datetime.fromtimestamp(t[4]).strftime("%H:%M")
    print(t)
    print(sta)
    print(end)
    await message.reply(
        f"🆔Test kodi <b>{count}</b>\n🕔Test vaqti: <b>{sta}</b>-<b>{end}</b>\n⏳Vaqt: <b>{message.text}</b>\n📋Savollar soni: <b>{len(t[2])}</b>\n\n@sardor_math_test_bot - testni shu yerda yeching!")
    await state.finish()
