from misc import *
from aiogram.types import Message
from aiogram import types
from .functions import *
from aiogram.utils.markdown import quote_html
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from asyncio import sleep


@dp.callback_query_handler(lambda c: c.data == "button_remove")
async def callback_remove(callback_query: types.CallbackQuery):
    cursor.execute("SELECT * FROM users WHERE user_id=?", (callback_query.from_user.id,))
    data = cursor.fetchone()
    if data is None:
        await bot.answer_callback_query(callback_query.id, text="🚫 Не найден в базе данных.", show_alert=True)
    elif 1912408598 or data[1] == 1:
        await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    elif data[1] == 0:
        await bot.answer_callback_query(callback_query.id, text="❌ Ты не админ бота", show_alert=True)

@dp.callback_query_handler(lambda c: c.data == "button_return")
async def callback_return(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text(f"Документация бота.", reply_markup=inline_btn_help)

@dp.callback_query_handler(lambda c: c.data == "button_help_users")
async def callback_users(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text(f"<code>Сэм</code> - Отзывалка.\n"
                                           f"<code>/ping</code> - Пинг-Понг ебать!\n"
                                           f"<code>/брак</code> - Предложить брак.\n"
                                           f"<code>/развод</code> - Расторгнуть брак.\n"
                                           f"<code>Сэм где я</code> - Узнать местонахождение.\n"
                                           f"<code>Сэм кто я</code> - Посмотреть свой профиль.\n"
                                           f"<code>Сэм кто это</code> - Посмотреть чужой профиль.\n", reply_markup=inline_btn_roleplay_return)

@dp.callback_query_handler(lambda c: c.data == "button_roleplay")
async def callback_roleplay(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text(f"<b>РП команды бота!</b>\n\n"
                                           f"• Чмок\n• Чпок\n• Кусь\n• Обнять\n• Шлеп\n• Убить\n• Выебать\n• Связать\n"
                                           f"• Ударить\n• Уебать\n• Отсосать\n• Отлизать\n• Задушить\n• Украсть\n"
                                           f"• Погладить\n• Притянуть\n• Изнасиловать\n• Отпороть", reply_markup=button_return)

@dp.callback_query_handler(lambda c: c.data == "button_help_admins")
async def callback_admins(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text(f"<code>Сэм админы</code> - Список админов бота.\n"
                                           f"<code>Сэм чаты</code> - Список чатов с ботом.\n"
                                           f"<code>/botinfo</code> - Информация о базе данных бота.\n"
                                           f"<code>/setwelcome «args»</code> - Установить приветствие новых юзеров.\n"
                                           f"<code>/delwelcome</code> - Удалить приветствие.\n"
                                           f"<code>/mute 30m/h/d</code> - Выдать мут на 30 минут/часов/дней.\n"
                                           f"<code>/unmute</code> - Снять мут.\n"
                                           f"<code>/ban</code> - Выдать бан.\n"
                                           f"<code>/unban</code> - Снять мут.\n", reply_markup=button_return)

@dp.callback_query_handler(lambda c: c.data == "button_help_quotes")
async def callback_quotes(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text(f"<b>Есть вопросы? Тык 👇:</b>\n\n"
                                           f"<a href='tg://user?id=2074396003'>Тык</a>", reply_markup=button_return)

@dp.callback_query_handler(lambda c: c.data == "button_slots")
async def callback_slots(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text(f"<b>Развлечения: | Слоты | Мини-игра</b>\n\n"
                                           f"<code>Б или Баланс</code> - Посмотреть баланс монеток + лимит.\n"
                                           f"<code>Бонус</code> - Взять бонус (1 раз в 3 часа).\n"
                                           f"<code>/buylim «кол-во лимита»</code> - Купить лимит, 5000 лимита = 2500 монет.\n"
                                           f"<code>/give «кол-во монеток»</code> - Передать монеток.\n"
                                           f"<code>/top</code> - Топ 5 богачей всего бота.\n"
                                           f"<code>слот «кол-во монеток»</code> - Сыграть в слоты.\n"
                                           f"<code>казино «кол-во монеток»</code> - Сыграть в казино.\n"
                                           f"<code>/vs «кол-во монеток»</code> - Сыграть в мини-игру.", reply_markup=button_return)