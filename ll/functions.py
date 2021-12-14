from misc import bot, dp, conn, cursor
from aiogram.types import Message
from aiogram import types

async def get_rang(message: types.Message):
    user = message.from_user
    cursor.execute("SELECT * FROM users WHERE user_id=?", (user.id,))
    data = cursor.fetchone()
    return data

async def get_marry(message: types.Message):
    user = message.from_user
    marry = cursor.execute("SELECT marry FROM users WHERE user_id=?", (user.id,)).fetchall()
    return marry

async def reply_get_rang(message: types.Message):
    reply = message.reply_to_message
    replyuser = reply.from_user
    cursor.execute("SELECT * FROM users WHERE user_id=?", (replyuser.id,))
    data = cursor.fetchone()
    return data

async def get_len_users(message: types.Message):
    users = cursor.execute("SELECT user_id FROM users").fetchall()
    allusers = len(users)
    return allusers

async def get_len_chats(message: types.Message):
    chats = cursor.execute("SELECT chat_id FROM chats").fetchall()
    allchats = len(chats)
    return allchats

async def get_admins(message: types.Message):
    admins = cursor.execute("SELECT user_id FROM users WHERE rang=?", (1,)).fetchall()
    alladmins = ""
    for x in admins:
        admin = await bot.get_chat(str(x[0]))
        alladmins += f"• {admin.first_name} | ID: <code>{admin.id}</code>\n"
    return alladmins

async def get_vips(message: types.Message):
    vips = cursor.execute("SELECT user_id FROM users WHERE status=?", (1,)).fetchall()
    allvips = ""
    for x in vips:
        vip = await bot.get_chat(str(x[0]))
        allvips += f"• {vip.first_name} | ID: <code>{vip.id}</code>\n"
    return allvips

async def get_chats(message: types.Message):
    chats = cursor.execute("SELECT chat_id FROM chats").fetchall()
    allchats = ""
    for x in chats:
        try:
            chat = await bot.get_chat(str(x[0]))
            allchats += f"• {chat.title} | ID: <code>{chat.id}</code>\n"
        except: pass
    return allchats

async def get_balance(message: types.Message):
    try:
        user = message.from_user
        get = cursor.execute("SELECT balance FROM users WHERE user_id=?", (user.id,)).fetchall()
        balance = f"{str(get[0][0])}"
        return balance
    except: pass

async def reply_get_balance(message: types.Message):
    try:
        reply = message.reply_to_message
        replyuser = reply.from_user
        get = cursor.execute("SELECT balance FROM users WHERE user_id=?", (replyuser.id,)).fetchall()
        balance = f"{str(get[0][0])}"
        return balance
    except: pass

async def get_limit(message: types.Message):
    try:
        user = message.from_user
        get = cursor.execute("SELECT g_limit FROM users WHERE user_id=?", (user.id,)).fetchall()
        limit = f"{str(get[0][0])}"
        return limit
    except: pass

#async def update_balance(message: types.Message, bet):
    #user = message.from_user
    #cursor.execute(f'UPDATE users SET balance=? WHERE user_id=?', (-bet, user.id,))
    #conn.commit()