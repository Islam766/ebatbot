import asyncio, sqlite3, pytz
from config import BOT_TOKEN
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

loop = asyncio.get_event_loop()
bot = Bot(BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot=bot, storage=MemoryStorage(), loop=loop)
conn = sqlite3.connect("BD/db.db")
cursor = conn.cursor()

#BUTTONS >
inline_btn_help_users = InlineKeyboardButton('Для всех👥', callback_data='button_help_users')
button_help_users = InlineKeyboardMarkup().add(inline_btn_help_users)

inline_btn_help_admins = InlineKeyboardButton('Для админов🅰️', callback_data='button_help_admins')
button_help_admins = InlineKeyboardMarkup().add(inline_btn_help_admins)

inline_btn_help_quotes = InlineKeyboardButton('Связь с владельцем💬', callback_data='button_help_quotes')
button_help_quotes = InlineKeyboardMarkup().add(inline_btn_help_quotes)

inline_btn_slots = InlineKeyboardButton('Развлечения🎰', callback_data='button_slots')
button_slots = InlineKeyboardMarkup().add(inline_btn_slots)




inline_btn_remove = InlineKeyboardButton('Удалить🗑', callback_data='button_remove')
button_remove = InlineKeyboardMarkup().add(inline_btn_remove)

inline_btn_return = InlineKeyboardButton('Вернуться🔙', callback_data='button_return')
button_return = InlineKeyboardMarkup().add(inline_btn_return)

inline_btn_roleplay = InlineKeyboardButton('РП команды🔱', callback_data='button_roleplay')
inline_btn_roleplay_return = InlineKeyboardMarkup(row_width=1)
inline_btn_roleplay_return.row(inline_btn_roleplay, inline_btn_return)

inline_btn_help = InlineKeyboardMarkup(row_width=1)
inline_btn_help.row(inline_btn_help_users, inline_btn_help_admins)
inline_btn_help.add(inline_btn_help_quotes, inline_btn_slots)


inline_btn_whm = InlineKeyboardButton('Войти', callback_data='button_join')
button_join = InlineKeyboardMarkup().add(inline_btn_whm)
#слито в @smoke_software
inline_btn_marry_y = InlineKeyboardButton('Да.', callback_data='button_marry_y')
button_marry_y = InlineKeyboardMarkup().add(inline_btn_marry_y)

inline_btn_marry_n = InlineKeyboardButton('Нет.', callback_data='button_marry_n')
button_marry_n = InlineKeyboardMarkup().add(inline_btn_marry_n)

button_marry = InlineKeyboardMarkup(row_width=1)
button_marry.row(inline_btn_marry_y, inline_btn_marry_n)



inline_btn_divorce_y = InlineKeyboardButton('Да.', callback_data='button_divorce_y')
button_divorce_y = InlineKeyboardMarkup().add(inline_btn_divorce_y)

inline_btn_divorce_n = InlineKeyboardButton('Нет.', callback_data='button_divorce_n')
button_divorce_n = InlineKeyboardMarkup().add(inline_btn_divorce_n)

button_divorce = InlineKeyboardMarkup(row_width=1)
button_divorce.row(inline_btn_divorce_y, inline_btn_divorce_n)







inline_btn_roleplay_chat = InlineKeyboardButton('РП команды', callback_data='roleplay_chat')
roleplay_chat = InlineKeyboardMarkup().add(inline_btn_roleplay_chat)
