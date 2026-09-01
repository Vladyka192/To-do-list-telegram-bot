from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def settings_menu_kb():
    return ReplyKeyboardMarkup(
        keyboard = [
            [KeyboardButton(text="Синхронизация с Google Calendar")],
            [KeyboardButton(text="Напоминания")],
    ],
    resize_keyboard=True)