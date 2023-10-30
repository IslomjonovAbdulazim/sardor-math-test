from datetime import datetime, timedelta
from unittest import result

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InputMediaPhoto, ContentType, CallbackQuery

from keyboards.inline.sure import sure_inline
from loader import db, dp, bot, test, results
from states.check import CheckState
import asyncio
from states.confirm_state import ConfirmState


@dp.message_handler()
async def start(message: types.Message, state: FSMContext):
    id = message.text
    data = test.select_user(id=id)
    if data is not None:
        result_id = str(message.from_user.id) + id
        result = results.select_user(id=result_id)
        if result is not None:
            percent = str((result[1] / len(str(result[8]).split(','))) * 100)
            await message.reply(
                f"Sizning bu test bo'yicha <b>natijangiz</b>:\n✅{result[1]}    ❌{result[2]}     ℹ️{result[3]}\n{percent[:4]}%")
        else:
            print(data)
            print(data[5])
            now = datetime.now()
            e = now + timedelta(minutes=data[5])
            sstart = datetime.fromtimestamp(data[3])
            eend = datetime.fromtimestamp(data[4])
            sta = sstart.strftime("%H:%M")
            end = eend.strftime("%H:%M")
            _e = e.strftime("%H:%M")
            if eend <= now:
                await message.reply(f"Bu test <b>{end}</b> da <b>yakunlangan</b>!")
            elif sstart >= now:
                await message.reply(f"Bu test <b>{sta}</b> da <b>boshlanadi</b>!")
            else:
                photos = str(data[1]).split(",")[:-1]
                res = []
                for p in photos:
                    res.append(InputMediaPhoto(media=p))
                await message.reply_media_group(media=res, protect_content=True)
                await CheckState.waiting.set()
                await state.update_data({
                    "id": id
                })
                __time: datetime
                if e > eend:
                    __time = eend
                    await message.reply(
                        f"Sizdan testni {end} gacha qabul qilamiz, biroz kech boshladingiz!\nformat: <b>a bc</b>, javoblaringizni ketma ket kiritib keting, belgilamaganingizni bo'sh qoldiring.")
                else:
                    __time = e
                    await message.reply(
                        f"Testni sizdan <b>{_e}</b> <b>gacha</b> qabul qilamiz!\nformat: <b>a bc</b>, javoblaringizni ketma ket kiritib keting, belgilamaganingizni bo'sh qoldiring.")
                _user = message.from_user.id
                __test = int(id)
                __id = f"{_user}{__test}"
                results.add_user(correct=0, wrong=0, not_selected=0, user=message.from_user.id, test=int(id), id=__id,
                                 start=now, end=__time, answers=""
                                 )
    else:
        await message.reply(f"<b>{id}</b> ga tegishli test topilmadi!")


@dp.callback_query_handler(text="yuq.secret", state=CheckState.waiting)
async def yuq(call: CallbackQuery):
    await call.message.delete()
    await call.message.answer("Javoblaringizni <b>boshidan</b> kiriting!")


@dp.callback_query_handler(text="ha.secret", state=CheckState.waiting)
async def ha(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    s = await state.get_data()
    _id = s.get("id")
    _answers = str(s.get("answers")).upper()
    _test = test.select_user(id=_id)
    _correct = str(_test[2]).upper()
    __id = str(call.from_user.id) + _id
    _result = []
    corrects = 0
    wrongs = 0
    un = 0
    for i in range(0, len(_correct)):
        if i >= len(_answers) or _answers[i] == " ":
            _result.append(f"N-{_correct[i]}")
            un += 1
        elif _answers[i] == _correct[i]:
            _result.append(f"T-{_correct[i]}")
            corrects += 1
        else:
            _result.append(f"F-{_correct[i]}")
            wrongs += 1
    res = ','.join(_result)
    results.update_user_answers(id=__id, answers=res)
    results.update_user_end(id=__id, end=datetime.now().timestamp())
    results.update_user_corrects(id=__id, correct=corrects)
    results.update_user_wrongs(id=__id, wrongs=wrongs)
    results.update_user_not_selected(id=__id, not_selected=un)
    percent = str((corrects / len(_correct)) * 100)
    await state.reset_state(with_data=False)
    await call.message.answer(
        f"Sizning bu test bo'yicha <b>natijangiz</b>:\n✅{corrects}    ❌{wrongs}     ℹ️{un}\n{percent[:4]}%")


@dp.message_handler(state=CheckState.waiting)
async def check(message: types.Message, state: FSMContext):
    res = message.text.lower().replace("a", "").replace("b", "").replace("c", "").replace("d", "").replace("e",
                                                                                                           "").replace(
        " ", "")
    n = datetime.now()
    d = await state.get_data()
    result = results.select_user(id=str(message.from_user.id) + d.get("id"))
    end = datetime.fromtimestamp(result[7])
    if end > n:
        if len(res) == 0:
            await message.reply(f"<b>{message.text.upper()}</b>\nUshbu javobni <b>qabul qilay</b>mi?",
                                reply_markup=sure_inline)
            await state.update_data({"answers": message.text.upper()})
        else:
            await message.reply(
                f"Javoblarda faqatgina <b>a,b,c,d,e</b> variantlari bo'ishi mumkin, sida esa <b>{res}</b> belgilari ortiqcha")
    else:
        await message.reply("Bu testni topshirishga ulgurmadingiz!")
        await state.reset_state(with_data=False)