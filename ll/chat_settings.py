from misc import bot, dp, conn, cursor
from aiogram.types import Message
from aiogram import types
from .functions import *
from aiogram.utils.markdown import quote_html

@dp.message_handler(commands=['setwelcome'])
async def cmd_setwelcome(message: types.Message):
    chat = message.chat
    args = message.get_args()
    data = await get_rang(message)
    admin = await bot.get_chat_member(chat_id=chat.id, user_id=message.from_user.id)
    if admin.status == "creator" or admin.status == "administrator" or data[1] == 1 or 1912408598:
        if args:
            cursor.execute(f'UPDATE chats SET welcome=? WHERE chat_id=?', (args, chat.id,))
            conn.commit()
            await message.reply(f"Новое приветствие в чате установлено!")
    else:
        await message.reply(f"🚫 <b>Вы не администратор.</b>")

@dp.message_handler(commands=['delwelcome'])
async def cmd_delwelcome(message: types.Message):
    chat = message.chat
    data = await get_rang(message)
    admin = await bot.get_chat_member(chat_id=chat.id, user_id=message.from_user.id)
    if admin.status == "creator" or admin.status == "administrator" or data[1] == 1 or 1912408598:
        cursor.execute(f'UPDATE chats SET welcome=? WHERE chat_id=?', ("0", chat.id,))
        conn.commit()
        await message.reply(f"Приветствие в чате очищено!")
    else:
        await message.reply(f"🚫 <b>Вы не администратор.</b>")

@dp.message_handler(commands=['del'])
async def cmd_del(message: types.Message):
    if 1912408598:
        await bot.delete_message(message.chat.id, message.reply_to_message.from_user.id)
        await message.reply(f"Удалено!")
    else:
        await message.reply(f"🚫 <b>Вы не администратор.</b>")

@dp.message_handler(commands=['settings'])
async def cmd_settings(message: types.Message):
    chat = message.chat
    await bot.send_message(chat.id, f"Настройки чата «{chat.title}»\n"
                                    f"╰<code>/toggle_rp_commands</code> - вкл/выкл РП команды в чате")

@dp.message_handler(commands=['toggle_rp_commands'])
async def cmd_toggle_rp_commands(message: types.Message):
    chat = message.chat
    user = message.from_user
    fullname = quote_html(user.full_name)
    cursor.execute("SELECT * FROM users WHERE user_id=?", (user.id,))
    getdata = cursor.fetchone()
    admin = await bot.get_chat_member(chat_id=chat.id, user_id=user.id)
    if admin.status == "creator" or admin.status == "administrator" or getdata[1] == 1 or 1912408598:
        cursor.execute("SELECT * FROM chats WHERE chat_id=?", (chat.id,))
        data = cursor.fetchone()
        await bot.delete_message(message.chat.id, message.message_id)
        if data[2] == 0:
            cursor.execute(f'UPDATE chats SET roleplay=? WHERE chat_id=?', (1, chat.id,))
            await bot.send_message(chat.id, f"{fullname} включил РП команды в этом чате!")
        elif data[2] == 1:
            cursor.execute(f'UPDATE chats SET roleplay=? WHERE chat_id=?', (0, chat.id,))
            await bot.send_message(chat.id, f"{fullname} отключил РП команды в этом чате!")
        conn.commit()
    else:
        await bot.delete_message(message.chat.id, message.message_id)
        await message.reply("Вы не администратор в чате❌")