from aiogram import types

from loader import db, dp, bot, test


@dp.message_handler()
async def start(message: types.Message):
    if "*" in message.text:
        l = message.text.split("*")
        if len(l) == 2:
            id = l[0]
            data = test.select_user(id=id)
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
                print(results)
                for num, ans in results.items():
                    if ans[1] == "T":
                        result += f"{num}: ✅{ans[0]}\n"
                        corrects += 1
                    elif ans[1] == "N":
                        result += f"{num}: ℹ️{ans[0]}\n"
                        unselected += 1
                    else:
                        result += f"{num}: ❌{ans[1]}->{ans[0]}✅\n"
                        wrongs += 1
                av = corrects // len(results.items()) + round(corrects / len(results.items()), 1)
                symbol = "✅" if av >= 85 else "ℹ️" if av >= 71 else "❌"
                result += f"✅{corrects}     ❌{wrongs}     ℹ️{unselected}\n{av * 100}%{symbol}"
                await message.reply(result, protect_content=True)
            else:
                await message.reply(f"{id} ga tegishli test topilmadi")
        else:
            await message.reply("Formatni noto'gri kiritdingiz, to'g'risini bilish uchun /help ning ustiga bosing")
    else:
        await message.reply(
            "Test javoblari quyidagi fromatda yuboriladi: \n<b>[tes codi]*[test javoblari]</b> \nmisol uchun <b>5*abc</b>, bilmagan javoblaringizni o'rniga bo'sh joy qoldiring <b>" "</b>")
