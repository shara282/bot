from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu_start = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Погода"), KeyboardButton(text="Тест")
        ],
        [
            KeyboardButton(text="Загрязнение воздуха")
        ],
    ],
    resize_keyboard=True
)
menu_selection_method = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="По названию города")
        ],
        [
            KeyboardButton(text="По координатам")
        ],
    ],
    resize_keyboard=True
)
menu_selection_test_1 = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="A")
        ],
        [
            KeyboardButton(text="B")
        ],
        [
            KeyboardButton(text="C")
        ],
    ],
    resize_keyboard=True
)
menu_selection_test_2 = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="A")
        ],
        [
            KeyboardButton(text="B")
        ],
        [
            KeyboardButton(text="C")
        ],
        [
            KeyboardButton(text="D")
        ],
    ],
    resize_keyboard=True
)
menu_selection_test_3 = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="A")
        ],
        [
            KeyboardButton(text="B")
        ],
        [
            KeyboardButton(text="C")
        ],
        [
            KeyboardButton(text="D")
        ],
        [
            KeyboardButton(text="E")
        ],
        [
            KeyboardButton(text="F")
        ],
    ],
    resize_keyboard=True
)
