import asyncio
from os import getenv

from aiogram import Bot, Dispatcher, html, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, BufferedInputFile

from calories import CaloriesState, formulas_handler, calories_handler
from calories import age_handler, height_handler, weight_handler, gender_handler
from commands import CommandHelp
from database.product import ProductRepository
from keyboard import main_keyboard, caloric_keyboard, product_keyboard
from registration import RegistrationState, sing_up, set_username, set_email, set_age

token = getenv("BOT_TOKEN")

dp = Dispatcher()


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
async def change_option(message: Message) -> None:
    await message.answer("Выберите опцию:", reply_markup=caloric_keyboard)


@dp.message(F.text == "Купить")
async def get_product_list(message: Message) -> None:
    repo = ProductRepository()
    products = repo.get_all()
    repo.close()
    for product in products:
        await message.answer_photo(BufferedInputFile(product[3], product[1]),
                                   f"{product[1]} | {product[2]} | Цена: {product[4]}")
    await message.answer("Выберите продукт для покупки:", reply_markup=product_keyboard)


dp.message(F.text == "Регистрация" or RegistrationState.user_id)(sing_up)
dp.message(RegistrationState.username)(set_username)
dp.message(RegistrationState.email)(set_email)
dp.message(RegistrationState.age)(set_age)


@dp.callback_query(F.data == "product_buying")
async def send_confirm_message(callback_query: CallbackQuery) -> None:
    await callback_query.message.answer("Вы успешно приобрели продукт!")
    await callback_query.answer()


dp.callback_query(F.data == "formulas")(formulas_handler)
dp.callback_query(F.data == "calories")(calories_handler)
dp.message(CaloriesState.age)(age_handler)
dp.message(CaloriesState.height)(height_handler)
dp.message(CaloriesState.weight)(weight_handler)
dp.message(CaloriesState.gender)(gender_handler)


@dp.message()
async def default_message_handler(message: Message) -> None:
    await message.answer("Введите команду /start, чтобы начать общение.")


async def main() -> None:
    bot = Bot(token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
