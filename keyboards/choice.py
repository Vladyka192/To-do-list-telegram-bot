from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

def choice_menu_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Название")],
            [KeyboardButton(text="Описание")],
            [KeyboardButton(text="Приоритет"),
             KeyboardButton(text="Дата")],
            [KeyboardButton(text="Время"),
            KeyboardButton(text="Статус")],
            [KeyboardButton(text="Назад")]
        ],
        resize_keyboard = True
    )

def edit_task_kb(task_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Редактировать", callback_data=f"edit_task:{task_id}"), 
            InlineKeyboardButton(text="Удалить", callback_data=f"delete_task:{task_id}")]
        ])