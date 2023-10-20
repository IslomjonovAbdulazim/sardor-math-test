from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

contact_btn = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📱Kontaktingiz", request_contact=True),
        ],
    ],
    resize_keyboard=True
)
