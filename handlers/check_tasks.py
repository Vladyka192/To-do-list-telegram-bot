from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputRichMessage,
    Message,
)

router = Router(name="rich_edit")

CHECKLIST_BEFORE = """\
# Чек-лист релиза

Прогресс: **0 из 3**

- [ ] Прогнать тесты
- [ ] Обновить документацию
- [ ] Задеплоить бота
"""

CHECKLIST_AFTER = """\
# Чек-лист релиза

Прогресс: **3 из 3** 🎉

- [x] Прогнать тесты
- [x] Обновить документацию
- [x] Задеплоить бота
"""


@router.message(Command("sendrichedit"))
async def cmd_send_rich_edit(
        message: Message,
) -> None:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(
            text="Выполнить все пункты",
            callback_data="complete_checklist",
        )
    ]])
    await message.answer_rich(                                    # [1]
        rich_message=InputRichMessage(markdown=CHECKLIST_BEFORE),
        reply_markup=keyboard,
    )


@router.callback_query(F.data == "complete_checklist")
async def on_complete_checklist(
        callback: CallbackQuery,
) -> None:
    await callback.message.edit_text(                             # [2]
        rich_message=InputRichMessage(markdown=CHECKLIST_AFTER),  # [3]
    )
    await callback.answer()