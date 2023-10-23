from aiogram import types
from aiogram.types import InputMediaPhoto, ContentType

from loader import db, dp, bot, test
from states.confirm_state import ConfirmState


@dp.message_handler()
async def start(message: types.Message):
    l = message.text.split("*")
    if len(l) == 2 and "*" in message.text:
        id = l[0]
        data = test.select_user(id=id)
        print(data)
        if data is not None:
            results = {}
            answers = data[2]
            print(answers)
            users = " " + l[1]
            t = 0
            for res in answers:
                t += 1
                try:
                    if users[t] == " ":
                        results[t] = f"{res}n".upper()
                    elif res == users[t]:
                        results[t] = f"{res}t".upper()
                    else:
                        results[t] = f"{res}{users[t]}".upper()
                except:
                    results[t] = f"{res}n".upper()
            result = ""
            corrects = 0
            unselected = 0
            wrongs = 0
            sum = 0
            print(results)
            for num, ans in results.items():
                if ans[1] == "T":
                    result += f"{num}: ✅{ans[0]}\n"
                    corrects += 1
                    sum += 500
                elif ans[1] == "N":
                    result += f"{num}: ℹ️{ans[0]}\n"
                    unselected += 1
                    sum -= 100
                else:
                    result += f"{num}: ❌{ans[1]}->{ans[0]}✅\n"
                    wrongs += 1
                    sum -= 1000
            av = corrects / len(results.items())
            av *= 100
            if av >= 85:
                symbol = "✅"
            elif av >= 71:
                symbol = "ℹ️"
            else:
                symbol = "❌"
            a = str(av)[:5]
            s = format(sum, ",").replace(",", " ")
            result += f"<b>✅{corrects}     ❌{wrongs}     ℹ️{unselected}\n\n{s} bal   {a}%{symbol}</b>"
            user = db.select_user(id=message.from_user.id)
            channel = f"{id}=@{user[5]}\n{id}={user[2][3:]}\n{id}={user[3]}\n"
            channel += f"<b>✅{corrects}     ❌{wrongs}     ℹ️{unselected}\n\n{s} bal   {a}%{symbol}</b>"
            print(user)
            await bot.send_message("@sardors_test", channel)
            await message.reply(result, protect_content=True)
        else:
            await message.reply(f"{id} ga tegishli test topilmadi")
    elif len(l) == 1:
        id = l[0]
        data = test.select_user(id=id)
        if data is not None:
            photos = str(data[1]).split(",")[:-1]
            res = []
            for p in photos:
                res.append(InputMediaPhoto(media=p))
            await message.reply_media_group(media=res, protect_content=True)
            await message.reply(
                f"Yechib bo'lganingizdan so'ng test raqami va yulduzcha qo'yib ketidan javoblaringizni yuboring, javobingiz bo'lmasa bo'sh qoldiring \nMisol uchun: <b>{id}*aaaab bc  ceed dd</b>")
        else:
            await message.reply(f"<b>{id}</b> ga tegishli test topilmadi")
    else:
        await message.reply("Formatni noto'gri kiritdingiz, to'g'risini bilish uchun /help ning ustiga bosing")
