import asyncio
from os import getenv

from aiogram import Bot, Dispatcher, html, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from UserState import UserState
from commands import CommandHelp

token = getenv("BOT_TOKEN")

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Привет, {html.bold(message.from_user.full_name)}! Я бот помогающий твоему здоровью.")


@dp.message(CommandHelp())
async def command_help_handler(message: Message) -> None:
    await message.answer(
        f"Я могу посчитать вашу ежедневную норму калорий. Хотите узнать? Введите слово -  {html.bold('Calories')}")


@dp.message(F.text == "Calories")
async def calories_handler(message: Message, state: FSMContext) -> None:
    await state.update_data(name=message.from_user.full_name)
    await message.answer("Введите свой возраст (полных лет):")
    await state.set_state(UserState.age)


@dp.message(UserState.age)
async def age_handler(message: Message, state: FSMContext) -> None:
    await state.update_data(age=message.text)
    await message.answer("Введите свой рост (см):")
    await state.set_state(UserState.height)


@dp.message(UserState.height)
async def height_handler(message: Message, state: FSMContext) -> None:
    await state.update_data(height=message.text)
    await message.answer("Введите свой вес (кг):")
    await state.set_state(UserState.weight)


@dp.message(UserState.weight)
async def weight_handler(message: Message, state: FSMContext) -> None:
    await state.update_data(weight=message.text)
    await message.answer("Введите свой пол (Муж/Жен):")
    await state.set_state(UserState.gender)


@dp.message(UserState.gender)
async def gender_handler(message: Message, state: FSMContext) -> None:
    await state.update_data(gender=message.text)
    data = await state.get_data()
    print(UserState.calculate_calories(data))
    await message.answer(
        f"{html.bold(data['name'])}. Ваша ежедневная норма калорий: {html.underline(UserState.calculate_calories(data))}")
    await state.clear()


@dp.message()
async def default_message_handler(message: Message) -> None:
    await message.answer("Введите команду /start, чтобы начать общение.")


async def main() -> None:
    bot = Bot(token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
