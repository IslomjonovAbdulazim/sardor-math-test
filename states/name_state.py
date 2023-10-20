from aiogram.dispatcher.filters.state import StatesGroup, State


class FullnameState(StatesGroup):
    waiting = State()

