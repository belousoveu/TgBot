from aiogram import html
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, ReplyKeyboardRemove, Message

from keyboard import main_keyboard


class CaloriesState(StatesGroup):
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


async def formulas_handler(callback_query: CallbackQuery) -> None:
    print("formulas")
    await callback_query.message.answer("""
    Упрощенный вариант формулы Миффлина-Сан Жеора:
    👨‍🦰 : 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5;
    👩‍🦰 : 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161.
    """)
    await callback_query.answer()


async def calories_handler(callback_query: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(name=callback_query.from_user.full_name)
    await callback_query.message.answer("Введите свой возраст (полных лет):")
    await callback_query.message.delete_reply_markup()
    await state.set_state(CaloriesState.age)


async def age_handler(message: Message, state: FSMContext) -> None:
    await state.update_data(age=message.text)
    await message.answer("Введите свой рост (см):", reply_markup=ReplyKeyboardRemove())
    await state.set_state(CaloriesState.height)


async def height_handler(message: Message, state: FSMContext) -> None:
    await state.update_data(height=message.text)
    await message.answer("Введите свой вес (кг):", reply_markup=ReplyKeyboardRemove())
    await state.set_state(CaloriesState.weight)


async def weight_handler(message: Message, state: FSMContext) -> None:
    await state.update_data(weight=message.text)
    await message.answer("Введите свой пол (Муж/Жен):", reply_markup=ReplyKeyboardRemove())
    await state.set_state(CaloriesState.gender)


async def gender_handler(message: Message, state: FSMContext) -> None:
    await state.update_data(gender=message.text)
    data = await state.get_data()
    await message.answer(
        f"{html.bold(data['name'])}. Ваша ежедневная норма калорий: "
        f"{html.underline(CaloriesState.calculate_calories(data))}",
        reply_markup=main_keyboard)
    await state.clear()
