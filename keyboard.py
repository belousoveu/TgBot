from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

main_keyboard = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text="Информация"),
        KeyboardButton(text="Рассчитать калории")
    ],
    [
        KeyboardButton(text="Купить")
    ],
    [
        KeyboardButton(text="Регистрация")
    ]
], resize_keyboard=True)

caloric_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Рассчитать калории", callback_data="calories"),
        InlineKeyboardButton(text="Формулы расчета", callback_data="formulas")
    ]
])

product_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Product1", callback_data="product_buying"),
        InlineKeyboardButton(text="Product2", callback_data="product_buying"),
        InlineKeyboardButton(text="Product3", callback_data="product_buying"),
        InlineKeyboardButton(text="Product4", callback_data="product_buying")
    ]
])
