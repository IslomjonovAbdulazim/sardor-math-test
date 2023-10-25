from aiogram.dispatcher.filters.state import StatesGroup, State


class EndState(StatesGroup):
    waiting = State()

