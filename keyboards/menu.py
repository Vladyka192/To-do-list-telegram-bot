from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_menu_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Создать задачу"),
             KeyboardButton(text="Просмотреть задачи")],
        ], 
        resize_keyboard=True
    )