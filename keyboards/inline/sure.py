from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

sure_inline = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="HA", callback_data="ha.secret"),
            InlineKeyboardButton(text="YO'Q", callback_data="yuq.secret"),
        ],
    ]
)
