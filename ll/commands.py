from misc import bot, dp, conn, cursor, inline_btn_help
from aiogram.utils.markdown import quote_html
from config import logchat
from aiogram.types import Message, ChatType
from aiogram import types
from meval import meval
from datetime import datetime
import quotes as q
import random
from .functions import *

async def getattrs(message):
    return {"reply": message.reply_to_message,
            "message": message,
            "bot": bot,
            "dp": dp,
            "chat": message.chat}

@dp.message_handler(commands=['who'])
async def who(message: types.Message):
    user = message.from_user
    admin = await bot.get_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)
    if admin.status == "creator" or admin.status == "administrator" or user.id == 480184376:
        await message.reply("Вы администратор в чате.")
    else:
        await message.reply("Вы не администратор в чате(")

@dp.message_handler(lambda t: t.text.startswith("Бот"))
async def fff(message: types.Message):
    h = ["Чаво тебе?","бля, да что?","Я тут, хули надо?","Та блять дай поспать","Ушёл в запой","Гнида, не беспокой пожалуйста:),","М?","Што?","Я тут, как дела?","Я занят, иди гуляй","Я тут, что прикажите?","Дя"]
    g = random.choice(h)
    await message.reply(f"""{g} 🤡""")

@dp.message_handler(commands=['ping'])
@dp.throttled(rate=2)
async def send_ping(message: types.Message):
    a = 5
    r = message.get_args()
    if r and r[0].isdigit():
        a = int(r[0])
    ping_msg = []
    ping_data = []
    for _ in range(a):
        start = datetime.now()
        msg = await bot.send_message(logchat, "ping")
        end = datetime.now()
        duration = (end - start).microseconds / 1000
        ping_data.append(duration)
        ping_msg.append(msg)
    ping = sum(ping_data) / len(ping_data)
    await message.reply(f"Понг ебать! {str(ping)[0:5]} ms.")
    for i in ping_msg:
        await i.delete()

@dp.message_handler(commands=['restart'])
async def restart(message: types.Message):
    user = message.from_user
    data = await get_rang(message)
    if 1912408598:
        chats = cursor.execute("SELECT chat_id FROM chats").fetchall()
        for x in chats:
            chat = await bot.get_chat(str(x[0]))
            await bot.send_message(chat.id, "Перезагрузка бота через 10 секунд!")

@dp.message_handler(commands=['botinfo'])
async def cmd_botinfo(message: types.Message):
    user = message.from_user
    data = await get_rang(message)
    if 1912408598 or data[1] == 1:
        users = await get_len_users(message)
        chats = await get_len_chats(message)
        await message.reply(f"<b>Информация о базе данных бота:</b>\n\n"
                            f"Зарегистрированных пользователей: <code>{users}</code>\n"
                            f"Зарегистрированных чатов: <code>{chats}</code>")

@dp.message_handler(commands=['eval'])
async def eval(message: types.Message):
    user = message.from_user
    data = await get_rang(message)
    if 1912408598:
        try:
            args = message.get_args()
            pizda = await meval(args, globals(), **await getattrs(message))
            await message.reply(f"<b>Выполненное выражение:</b>\n<code>{args}</code>\n\n<b>Возвращено:</b>\n<code>{pizda}</code>")
        except: pass
    else:
        await message.reply("пососешб ок?")

@dp.message_handler(commands=['send'])
async def cmd_send(message: types.Message):
    user = message.from_user
    args = message.get_args()
    data = await get_rang(message)
    if 1912408598:
        if not args:
            await message.reply("Укажи аргументы.")
        else:
            chats = cursor.execute("SELECT chat_id FROM chats").fetchall()
            for x in chats:
                try:
                    chat = await bot.get_chat(str(x[0]))
                    await bot.send_message(chat.id, args)
                except: pass
            await message.reply("Рассылка успешна!")

@dp.message_handler(commands=['sm'])
async def cmd_message(message: types.Message):
    user = message.from_user
    args = message.get_args()
    data = await get_rang(message)
    if 1912408598:
        if not args:
            await message.reply("Укажи аргументы.")
        else:
            await bot.send_message(message.chat.id, args)

@dp.message_handler(commands=['start'], chat_type = ChatType.PRIVATE)
async def cmd_start(message: types.Message):
    user = message.from_user
    data = await get_rang(message)
    if data is None:
        cursor.execute(f"INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (user.id, 0, 0, 0, 0, 5000, 0, 0))
        conn.commit()
        await bot.send_message(message.chat.id, "Привет, ты новенький?\nОкей, ты был добавлен в базу данных бота!")
        await bot.send_message(logchat, f"#new_user\n"
                                        f"<b>Новый пользователь в базе данных!</b>\n\n"
                                        f"• <b>Name:</b> <a href='tg://user?id={user.id}'>{user.first_name}</a>\n"
                                        f"• <b>ID:</b> <code>{user.id}</code>")
    else:
        await message.reply(
        f"""Привет <a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a>, я Сэм . Чтобы узнать что я умею введите команду /help""")

@dp.message_handler(commands=['help'])
async def cmd_help(message: types.Message):
    user = message.from_user
    await message.reply(f"<a href='tg://user?id={user.id}'>{user.first_name}</a>, документация бота.", reply_markup=inline_btn_help)

@dp.message_handler(commands=['donate'])
async def cmd_donate(message: types.Message):
    fname = quote_html(message.from_user.full_name)
    await message.reply(f"<a href='tg://user?id={message.from_user.id}'>{fname}</a>, статья о пожертвовании:\n"
                        f"https://telegra.ph/Pozhertvovanie-proektu-03-25")

@dp.message_handler(commands=['fqstats'])
@dp.throttled(rate=5)
async def fqstats_message(message: types.Message):
    data = await get_rang(message)
    if 1912408598:
        await q.fqstats_message(message)

@dp.message_handler(commands=['fq'])
@dp.throttled(rate=5)
async def fakequotes(message: types.Message):
    user = message.from_user
    data = await get_rang(message)
    reply = message.reply_to_message
    if not reply:
        await message.reply("Нет реплая")
        return
    if data is None:
        return await message.reply(f"🚫 <b>Не найден в базе данных.</b>\n\n"
                                   f"/start в лс у бота!")
    elif 1912408598:
        await q.fakequotes(message)
    elif data[1] == 0 or data[1] == 1:
        return_get_balance = await get_balance(message)
        quot = 5000
        if int(return_get_balance) < int(quot):
            await message.reply("💢 Не хватает средств!")
            return
        snyato = int(return_get_balance) - int(quot)
        cursor.execute(f'UPDATE users SET balance=? WHERE user_id=?', (snyato, user.id,))
        await message.reply(f"{user.first_name}, с вашего баланса было снято 5000 монет.\n"
                            f"для - FakeQuotes")
        await q.fakequotes(message)

@dp.message_handler(content_types=["new_chat_members"])
async def new_chat(message: types.Message):
    for user in message.new_chat_members:
        if user.id == (await bot.get_me()).id:
            cid = message.chat.id
            chat = message.chat
            user = message.from_user
            cursor.execute("SELECT * FROM chats WHERE chat_id=?", (cid,))
            data = cursor.fetchone()
            if data is None:
                cursor.execute(f"INSERT INTO chats VALUES (?, ?, ?)", (cid, 0, 0,))
                conn.commit()
                await bot.send_message(message.chat.id, f"<b>Я в новом чате.</b>\n"
                                                        f"• <b>Чат:</b> {chat.title}\n"
                                                        f"• <b>ID:</b> <code>{chat.id}</code>\n\n"
                                                        f"<b>Для полной работы бота, мне нужны права администратора!</b>")
                await bot.send_message(logchat, f"#new_chat\n"
                                                f"<b>Новый чат в базе данных!</b>\n"
                                                f"<b>Пригласил:</b> {user.first_name} | <code>{user.id}</code>\n\n"
                                                f"• <b>Name:</b> {chat.title}\n"
                                                f"• <b>ID:</b> <code>{chat.id}</code>")
            else:
                await bot.send_message(message.chat.id, f"<b>Я в известном мне чате.</b>\n"
                                                        f"• <b>Чат:</b> {chat.title}\n"
                                                        f"• <b>ID:</b> <code>{chat.id}</code>\n\n"
                                                        f"<b>Для полной работы бота, мне нужны права администратора!</b>")
        else:
            chat = message.chat
            cursor.execute("SELECT * FROM chats WHERE chat_id=?", (chat.id,))
            data = cursor.fetchone()
            try:
                if data[1] == "0":
                    return
                else:
                    text = cursor.execute("SELECT welcome FROM chats WHERE chat_id=?", (chat.id,)).fetchone()[0]
                    await message.reply(f"{quote_html(text)}")
            except: pass


@dp.message_handler(commands=['setadmin'])
async def cmd_setadmin(message: types.Message):
    reply = message.reply_to_message
    data = await get_rang(message)
    if 1912408598:
        if reply:
            replyuser = reply.from_user
            name = quote_html(replyuser.full_name)
            cursor.execute(f'UPDATE users SET rang=? WHERE user_id=?', (1, replyuser.id,))
            conn.commit()
            await message.reply(f"{name} назначен админом бота!")
    if data is None:
        await message.reply(f"🚫 <b>Не найден в базе данных.</b>\n\n"
                            f"/start в лс у бота!")

@dp.message_handler(commands=['deladmin'])
async def cmd_deladmin(message: types.Message):
    reply = message.reply_to_message
    data = await get_rang(message)
    if 1912408598:
        if reply:
            replyuser = reply.from_user
            name = quote_html(replyuser.full_name)
            cursor.execute(f'UPDATE users SET rang=? WHERE user_id=?', (0, replyuser.id,))
            conn.commit()
            await message.reply(f"{name} больше не админ бота!")
    if data is None:
        await message.reply(f"🚫 <b>Не найден в базе данных.</b>\n\n"
                            f"/start в лс у бота!")

@dp.message_handler(commands=['delchatbd'])
async def cmd_delchatbd(message: types.Message):
    chat = message.chat
    data = await get_rang(message)
    if 1912408598:
        cursor.execute("DELETE FROM chats WHERE chat_id=?", (chat.id,))
        conn.commit()
        await message.reply(f"Чат {chat.title} удалён из базы данных!")

@dp.message_handler(commands=['delbd'])
async def cmd_delbd(message: types.Message):
    reply = message.reply_to_message
    data = await get_rang(message)
    if 1912408598:
        if reply:
            replyuser = reply.from_user
            name = quote_html(replyuser.full_name)
            cursor.execute("DELETE FROM users WHERE user_id=?", (replyuser.id,))
            conn.commit()
            await message.reply(f"{name} удалён из базы данных!")

@dp.message_handler(commands=['buyvip'])
async def cmd_buyvip(message: types.Message):
    data = await get_rang(message)
    user = message.from_user
    if data[2] == 0:
        name = quote_html(user.full_name)
        return_get_balance = await get_balance(message)
        vip = 500000
        if int(return_get_balance) < int(vip):
            await message.reply("💢 Не хватает средств!")
            return
        snyato = int(return_get_balance) - int(vip)
        cursor.execute(f'UPDATE users SET balance=? WHERE user_id=?', (snyato, user.id,))
        cursor.execute(f'UPDATE users SET status=? WHERE user_id=?', (1, user.id,))
        return_get_limit = await get_limit(message)
        plim = int(return_get_limit) + int(50000)
        cursor.execute(f'UPDATE users SET g_limit=? WHERE user_id=?', (plim, user.id,))
        conn.commit()
        await message.reply(f"<a href='tg://user?id={user.id}'>{name}</a>, успешно приобрел VIP статус.")
    elif data[2] == 1:
        await message.reply(f"У тебя есть випка :/")
    if data is None:
        await message.reply(f"🚫 <b>Не найден в базе данных.</b>\n\n"
                            f"/start в лс у бота!")

@dp.message_handler(commands=['vladskinsisi'])
async def cmd_buyvip(message: types.Message):
    user = message.from_user
    name = quote_html(user.full_name)
    await message.reply(f"<a href='tg://user?id={user.id}'>{name}</a>, владик не скинет сиси((")
