import asyncio
from os import getenv

from aiogram import Bot, Dispatcher, html, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

from UserState import UserState
from commands import CommandHelp

token = getenv("BOT_TOKEN")

dp = Dispatcher()

main_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Информация"),
     KeyboardButton(text="Рассчитать калории")]
], resize_keyboard=True)


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Привет, {html.bold(message.from_user.full_name)}! Я бот, помогающий твоему здоровью.",
                         reply_markup=main_keyboard)


@dp.message(CommandHelp())
@dp.message(F.text == "Информация")
async def command_help_handler(message: Message) -> None:
    await message.answer(
        f"Я могу посчитать вашу ежедневную норму калорий. Хотите узнать? Нажмите на кнопку - "
        f"{html.bold('Рассчитать калории')}", reply_markup=main_keyboard)


@dp.message(F.text == "Рассчитать калории")
async def calories_handler(message: Message, state: FSMContext) -> None:
    await state.update_data(name=message.from_user.full_name)
    await message.answer("Введите свой возраст (полных лет):", reply_markup=ReplyKeyboardRemove())
    await state.set_state(UserState.age)


@dp.message(UserState.age)
async def age_handler(message: Message, state: FSMContext) -> None:
    await state.update_data(age=message.text)
    await message.answer("Введите свой рост (см):", reply_markup=ReplyKeyboardRemove())
    await state.set_state(UserState.height)


@dp.message(UserState.height)
async def height_handler(message: Message, state: FSMContext) -> None:
    await state.update_data(height=message.text)
    await message.answer("Введите свой вес (кг):", reply_markup=ReplyKeyboardRemove())
    await state.set_state(UserState.weight)


@dp.message(UserState.weight)
async def weight_handler(message: Message, state: FSMContext) -> None:
    await state.update_data(weight=message.text)
    await message.answer("Введите свой пол (Муж/Жен):", reply_markup=ReplyKeyboardRemove())
    await state.set_state(UserState.gender)


@dp.message(UserState.gender)
async def gender_handler(message: Message, state: FSMContext) -> None:
    await state.update_data(gender=message.text)
    data = await state.get_data()
    await message.answer(
        f"{html.bold(data['name'])}. Ваша ежедневная норма калорий: "
        f"{html.underline(UserState.calculate_calories(data))}",
        reply_markup=ReplyKeyboardRemove())
    await state.clear()


@dp.message()
async def default_message_handler(message: Message) -> None:
    await message.answer("Введите команду /start, чтобы начать общение.")


async def main() -> None:
    bot = Bot(token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
