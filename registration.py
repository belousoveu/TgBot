import re

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove

from database.user import UserRepository
from keyboard import main_keyboard


class RegistrationState(StatesGroup):
    user_id = State()
    username = State()
    email = State()
    age = State()


async def sing_up(message: Message, state: FSMContext):
    user_id = message.from_user.id
    if user_exists(user_id=user_id):
        await message.reply("Вы уже зарегистрированы")
        await message.answer("Регистрация отменена", reply_markup=main_keyboard)
        await state.clear()
        return
    await state.update_data(user_id=user_id)
    await message.answer("Введите ваше имя (разрешены только латинские символы)", reply_markup=ReplyKeyboardRemove())
    await state.set_state(RegistrationState.username)


async def set_username(message: Message, state: FSMContext):
    username = message.text
    if not validate_username(username):
        await message.reply("Некорректное имя. Попробуйте снова")
        await state.set_state(RegistrationState.username)
        return
    if user_exists(username=username):
        await message.reply("Пользователь с таким именем уже существует. Попробуйте снова")
        await state.set_state(RegistrationState.username)
        return
    await state.update_data(username=username)
    await message.answer("Введите ваш email", reply_markup=ReplyKeyboardRemove())
    await state.set_state(RegistrationState.email)


async def set_email(message: Message, state: FSMContext):
    email = message.text
    if not validate_email(email):
        await message.reply("Некорректный email. Попробуйте снова")
        await state.set_state(RegistrationState.email)
        return
    await state.update_data(email=email)
    await message.answer("Введите ваш возраст", reply_markup=ReplyKeyboardRemove())
    await state.set_state(RegistrationState.age)


async def set_age(message: Message, state: FSMContext):
    age = message.text
    if not validate_age(age):
        await message.reply("Некорректный возраст. Попробуйте снова")
        await state.set_state(RegistrationState.age)
        return
    if not adult_user(age):
        await message.reply("Вы не можете зарегистрироваться, так как не достигли 18 лет")
        await message.answer("Регистрация отменена", reply_markup=main_keyboard)
        await state.clear()
        return
    await state.update_data(age=age)
    data = await state.get_data()
    register_user(data)
    await message.answer("Вы успешно зарегистрировались", reply_markup=main_keyboard)
    await state.clear()


def validate_username(username) -> bool:
    pattern = r'^[a-zA-Z]+$'
    return bool(re.match(pattern, username))


def validate_email(email) -> bool:
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return bool(re.match(pattern, email))


def validate_age(age) -> bool:
    if not age.isdigit():
        return False
    if int(age) < 1 or int(age) > 120:
        return False
    return True


def adult_user(age) -> bool:
    return int(age) >= 18


def user_exists(user_id=None, username=None) -> bool:
    repo = UserRepository()
    return repo.user_exists(user_id, username)


def register_user(data) -> None:
    repo = UserRepository()
    repo.add_user(data['user_id'], data['username'], data['email'], data['age'])
    repo.close()
