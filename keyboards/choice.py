from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def choice_menu_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Название")],
            [KeyboardButton(text="Описание")],
            [KeyboardButton(text="Приоритет"),
             KeyboardButton(text="Дата")],
            [KeyboardButton(text="Время"),
            KeyboardButton(text="Статус")]
        ]
    )