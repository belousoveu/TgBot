from aiogram.fsm.state import StatesGroup, State


class UserState(StatesGroup):
    name = State()
    age = State()
    height = State()
    weight = State()
    gender = State()

    @staticmethod
    def calculate_calories(data):
        gender = data['gender']
        calories = 10 * float(data['weight']) + 6.25 * float(data['height']) - 5.0 * float(data['age'])
        if gender.startswith('М') or gender.startswith('M'):
            calories += 5
        else:
            calories -= 161
        return int(calories)
