from aiogram.dispatcher.filters.state import StatesGroup, State


class ImageState(StatesGroup):
    waiting = State()

