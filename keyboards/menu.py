from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_menu_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Задачи")],
            [KeyboardButton(text="Настройки"), 
             KeyboardButton(text="Google calendar")],
        ], 
        resize_keyboard=True
    )