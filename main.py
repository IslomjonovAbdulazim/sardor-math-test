
from aiogram import executor

from loader import dp, db, test, bot, results
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands
from datetime import time, datetime


async def on_startup(dispatcher):
    await set_default_commands(dispatcher)

    try:
        db.create_table_users()
    except Exception as err:
        print(err)

    try:
        test.create_table_users()
    except Exception as err:
        print(err)
    await on_startup_notify(dispatcher)

    try:
        results.create_table_users()
    except Exception as err:
        print(err)
    print(results.select_all_users())
    await on_startup_notify(dispatcher)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
