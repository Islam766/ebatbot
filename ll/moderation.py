from misc import bot, dp, cursor, button_remove
from aiogram.types import Message
from aiogram import types
import time
from .functions import *

@dp.message_handler(commands=['mute'])
async def cmd_mute(message: types.Message):
    user = message.from_user
    data = await get_rang(message)
    if data[1] == 1 or 1912408598:
        reply = message.reply_to_message
        if reply:
            replyuser = reply.from_user
            args = message.get_args()
            if args:
                try:
                    n = ''
                    t = ''
                    for _ in args:
                        if _.isdigit():
                            n += _
                        else:
                            t += _
                    yeah = f"{n}"
                    if t == "m":
                        n = int(n) * 60
                        yeah += " минут"
                    elif t == "h":
                        n = int(n) * 3600
                        yeah += " часов"
                    elif t == "d":
                        n = int(n) * 86400
                        yeah += " дней"
                except ValueError: return await message.reply("Нет аргументов.")
                if replyuser.id == (await bot.get_me()).id:
                    return
                cursor.execute("SELECT * FROM users WHERE user_id=?", (replyuser.id,))
                status = cursor.fetchone()
                if status is None:
                    await bot.send_message(message.chat.id, f"<b>{replyuser.first_name}</b> получил мут на {yeah}!\n\n"
                                                            f"💢 Выдал: <b>{user.first_name}</b>")
                    await bot.restrict_chat_member(message.chat.id, replyuser.id,
                                       until_date=time.time() + int(n),
                                       can_send_messages=False)
                elif status[1] == 2 or status[1] == 1:
                    return await message.reply("Я не буду его мутить!")
                elif status[1] == 0:
                    await bot.send_message(message.chat.id, f"<b>{replyuser.first_name}</b> получил мут на {yeah}!\n\n"
                                                            f"💢 Выдал: <b>{user.first_name}</b>")
                    await bot.restrict_chat_member(message.chat.id, replyuser.id,
                                       until_date=time.time() + int(n),
                                       can_send_messages=False)
            else:
                await message.reply("Нет аргументов.")
        else:
            await message.reply("Кому мут то?")

@dp.message_handler(commands=['unmute'])
async def cmd_unmute(message: types.Message):
    user = message.from_user
    data = await get_rang(message)
    if data[1] == 1 or 1912408598:
        reply = message.reply_to_message
        if reply:
            replyuser = reply.from_user
            if replyuser.id == (await bot.get_me()).id:
                return
            await bot.send_message(message.chat.id, f"<b>{replyuser.first_name}</b> теперь не в муте!\n\n"
                                                    f"💢 Снял: <b>{user.first_name}</b>")
            await bot.restrict_chat_member(message.chat.id, replyuser.id,
                                       can_send_messages=True,
                                       can_send_media_messages=True,
                                       can_send_other_messages=True,
                                       can_add_web_page_previews=True)
        else:
            await message.reply("Кому снять мут то?")

@dp.message_handler(commands=['ban'])
async def cmd_ban(message: types.Message):
    user = message.from_user
    data = await get_rang(message)
    if data[1] == 1 or 1912408598:
        reply = message.reply_to_message
        if reply:
            replyuser = reply.from_user
            if replyuser.id == (await bot.get_me()).id:
                return
            cursor.execute("SELECT * FROM users WHERE user_id=?", (replyuser.id,))
            status = cursor.fetchone()
            if status is None:
                await bot.send_message(message.chat.id, f"<b>{replyuser.first_name}</b> получил бан!\n\n"
                                                        f"💢 Выдал: <b>{user.first_name}</b>")
                await bot.kick_chat_member(message.chat.id, replyuser.id)
            elif 1912408598 or status[1] == 1:
                return await message.reply("Я не буду его банить!")
            elif status[1] == 0:
                await bot.send_message(message.chat.id, f"<b>{replyuser.first_name}</b> получил бан!\n\n"
                                                        f"💢 Выдал: <b>{user.first_name}</b>")
                await bot.kick_chat_member(message.chat.id, replyuser.id)
        else:
            await message.reply("Кого банить то?")

@dp.message_handler(commands=['unban'])
async def cmd_unban(message: types.Message):
    user = message.from_user
    data = await get_rang(message)
    if data[1] == 1 or 1912408598:
        reply = message.reply_to_message
        if reply:
            replyuser = reply.from_user
            if replyuser.id == (await bot.get_me()).id:
                return
            await bot.send_message(message.chat.id, f"<b>{replyuser.first_name}</b> теперь не в бане!\n\n"
                                                    f"💢 Снял: <b>{user.first_name}</b>")
            await bot.unban_chat_member(message.chat.id, replyuser.id)
        else:
            await message.reply("Кому снять бан то?")