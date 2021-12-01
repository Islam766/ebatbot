from misc import bot, dp, cursor, button_remove
from aiogram.types import Message
from aiogram.utils.markdown import quote_html
from aiogram import types
import random, time
from .functions import *
from time import gmtime
from time import strftime
from aiogram.dispatcher.filters import Text

Admin = 1912408598
@dp.message_handler(content_types=["text"])
async def main(message: types.Message):
    flowers = ["🌸", "🌼", "🍁", "🌿", "🌹", "🌷", "🌺"]
    phrases = ["Приветик солнце❤️", "Че с ебалом?", "Добро пожаловать", "Ну привет 👉👈", "Салам", "Брат", "ИУУУУУУУУУУУ", "Допустим"]
    user = message.from_user
    chat = message.chat
    if message.text.lower() == "сэм":
        data = await get_rang(message)
        if data is None:
            return await message.reply(f"🚫 <b>Не найден в базе данных.</b>\n\n"
                                       f"/start в лс у бота!")
        else:
            await message.reply(f"{random.choice(phrases)}\n"
                                f"Ты в чате: <b>{message.chat.title}</b>")
    elif message.text.lower() in ["сэм кто я", "профиль", "сэм профиль"]:
        data = await get_rang(message)
        if data is None:
            return await message.reply(f"🚫 <b>Не найден в базе данных.</b>\n\n"
                                       f"/start в лс у бота!")
        elif data[1] == 1:
            status = "\n«<b>Админ бота</b>» ʕ•ᴥ•ʔ"
        elif data[1] == 0:
            status = "юзер"
        if data[2] == 0:
            cvip = "Игрок"
        elif data[2] == 1:
            cvip = "VIP"
        if user.username is None:
            username = "Нет"
        else:
            username = f"@{user.username}"
        return_get_balance = await get_balance(message)
        if data[6] == 0:
            brak = "Без брака💔"
        else:
            marry = cursor.execute("SELECT marry FROM users WHERE user_id=?", (user.id,)).fetchall()
            marred = await bot.get_chat(str(marry[0][0]))
            mname = quote_html(marred.full_name)
            get = cursor.execute("SELECT marry_time FROM users WHERE user_id=?", (user.id,)).fetchall()
            mtime = f"{int(get[0][0])}"
            marry_time = time.time() - float(mtime)
            vremya = strftime("%j дней %H часов %M минут", gmtime(marry_time))
            brak = f"Брак с - {mname}\n   ╰В браке уже - {vremya}"
        await bot.send_message(message.chat.id, f"{random.choice(flowers)} Имя - {quote_html(user.full_name)}\n"
                                                f"╰Юзер - {username}\n"
                                                f"╰Айди - <code>{user.id}</code>\n"
                                                f"╰Монеток - <code>{return_get_balance}</code>\n"
                                                f"╰Статус - {cvip}\n"
                                                f"╰{brak}\n"
                                                f"{status}", reply_markup=button_remove)

    elif message.text.lower() in [" сэм кто это", "кто это", "кто ты", "ты кто"]:
        reply = message.reply_to_message
        if reply:
            replyuser = reply.from_user
            replydata = await reply_get_rang(message)
            if replyuser.id == (await bot.get_me()).id:
                return await message.reply("Я бот, идиот.")
            if replydata is None:
                return await message.reply(f"🚫 <b>Не найден в базе данных.</b>\n\n"
                                           f"/start в лс у бота!")
            elif replydata[1] == 1:
                status = "\n«<b>Админ бота</b>» ʕ•ᴥ•ʔ"
            elif replydata[1] == 0:
                status = "юзер"
            if replydata[2] == 0:
                cvip = "Игрок"
            elif replydata[2] == 1:
                cvip = "VIP"
            if replyuser.username is None:
                username = "Нет"
            else:
                username = f"@{replyuser.username}"
            return_get_balance = await reply_get_balance(message)
            if replydata[6] == 0:
                brak = "Без брака💔"
            else:
                marry = cursor.execute("SELECT marry FROM users WHERE user_id=?", (replyuser.id,)).fetchall()
                marred = await bot.get_chat(str(marry[0][0]))
                mname = quote_html(marred.full_name)
                get = cursor.execute("SELECT marry_time FROM users WHERE user_id=?", (replyuser.id,)).fetchall()
                mtime = f"{int(get[0][0])}"
                marry_time = time.time() - float(mtime)
                vremya = strftime("%j дней %H часов %M минут", gmtime(marry_time))
                brak = f"Брак с - {mname}\n   ╰В браке уже - {vremya}"
            await bot.send_message(message.chat.id, f"{random.choice(flowers)} Имя - {quote_html(replyuser.full_name)}\n"
                                                    f"╰Юзер - {username}\n"
                                                    f"╰Айди - <code>{replyuser.id}</code>\n"
                                                    f"╰Монеток - <code>{return_get_balance}</code>\n"
                                                    f"╰Статус - {cvip}\n"
                                                    f"╰{brak}\n"
                                                    f"{status}", reply_markup=button_remove)
    elif message.text.lower() in ["сэм где я", "где я"]:
        getwelcome = cursor.execute("SELECT welcome FROM chats WHERE chat_id=?", (chat.id,)).fetchall()
        if getwelcome is None:
            return await message.reply(f"🚫 <b>Чат не найден в базе данных.</b>")
        else:
            get = f"{str(getwelcome[0][0])}"
            if get == "0":
                welcome = "Нет"
            else:
                welcome = quote_html(str(get))
            await message.reply(f"{quote_html(message.from_user.full_name)} ты в чате <b>{message.chat.title}</b>\nID: <code>{message.chat.id}</code>\n"
                                f"Приветствие в чате: <b>{welcome}</b>", reply_markup=button_remove)
    elif message.text.lower() in ["б", "баланс"]:
        data = await get_rang(message)
        if data is None:
            return await message.reply(f"🚫 <b>Не найден в базе данных.</b>\n\n"
                                       f"/start в лс у бота!")
        else:
            return_get_balance = await get_balance(message)
            return_get_limit = await get_limit(message)
            if return_get_balance == "0":
                await message.reply(f"{user.first_name}, ваш баланс: <code>{return_get_balance}</code> монет.\n"
                                    f"Ты можешь взять бонус, написав «бонус»!\n\n"
                                    f"Лимит: <code>{return_get_limit}</code> монет.")
            else:
                await message.reply(f"{user.first_name}, ваш баланс: <code>{return_get_balance}</code> монет.\n\n")

    elif message.text.lower() == "бонус":
        data = await get_rang(message)
        if data is None:
            return await message.reply(f"🚫 <b>Не найден в базе данных.</b>\n\n"
                                       f"/start в лс у бота!")
        return_get_balance = await get_balance(message)
        period = 1 * 1
        get = cursor.execute("SELECT last_bonus FROM users WHERE user_id=?", (user.id,)).fetchall()
        last_bonus = f"{int(get[0][0])}"
        bonustime = time.time() - float(last_bonus)
        if int(return_get_balance) < 5000:
            if bonustime > period:
                if data[2] == 1:
                    bonus = random.randint(9000, 3000)
                elif data[2] == 0:
                    bonus = random.randint(3000, 9000)
                cursor.execute(f'UPDATE users SET balance=? WHERE user_id=?', (bonus, user.id,))
                cursor.execute(f'UPDATE users SET last_bonus=? WHERE user_id=?', (time.time(), user.id,))
                await message.reply(f"<a href='tg://user?id={user.id}'>{user.first_name}</a>, ты получил свой бонус в размере <code>{str(bonus)}</code> монет!")
            else:
                return await message.reply(f"<a href='tg://user?id={user.id}'>{user.first_name}</a>, 3 часа с начала взятия бонуса ещё не прошли!\n")
        else:
            return await message.reply(f"<a href='tg://user?id={user.id}'>{user.first_name}</a>, твой баланс не ниже 50 монет!")
    elif message.text.lower() == "сэм админы":
        data = await get_rang(message)
        if data[1] == 1 or data[1] == 2:
            creator = await bot.get_chat(1912408598)
            return_get_admins = await get_admins(message)
            await message.reply(f"<b>Админы бота:</b>\n\n{return_get_admins}\n<b>Создатель:</b>\n"
                                f"• {creator.first_name} | ID: <code>{creator.id}</code>", reply_markup=button_remove)
    elif message.text.lower() == "сэм випы":
        data = await get_rang(message)
        if data[1] == 1 or data[1] == 2 or data[2] == 1:
            return_get_vips = await get_vips(message)
            await message.reply(f"<b>Все вип пользователи:</b>\n\n{return_get_vips}", reply_markup=button_remove)
    elif message.text.lower() == "сэм чаты":
        data = await get_rang(message)
        if data[1] == 1 or data[1] == 2:
            return_get_chats = await get_chats(message)
            await message.reply(f"<b>Чаты в базе данных:</b>\n\n{return_get_chats}", reply_markup=button_remove)
    ######################################РП КОМАНДЫ#################################################
    cursor.execute("SELECT * FROM chats WHERE chat_id=?", (chat.id,))
    chat_data = cursor.fetchone()
    if chat_data[2] == 1:
        if message.text.lower() == "чмок":
            reply = message.reply_to_message
            if reply:
                replyuser = reply.from_user
                await bot.send_message(message.chat.id, f"<a href='tg://user?id={user.id}'>{user.first_name}</a> чмокнул(-а) <a href='tg://user?id={replyuser.id}'>{replyuser.first_name}</a>")
        if message.text.lower() == "чпок":
            reply = message.reply_to_message
            if reply:
                replyuser = reply.from_user
                await bot.send_message(message.chat.id, f"<a href='tg://user?id={user.id}'>{user.first_name}</a> чпокнул(-а) <a href='tg://user?id={replyuser.id}'>{replyuser.first_name}</a>")
        if message.text.lower() == "кусь":
            reply = message.reply_to_message
            if reply:
                replyuser = reply.from_user
                await bot.send_message(message.chat.id, f"<a href='tg://user?id={user.id}'>{user.first_name}</a> кусьнул(-а) <a href='tg://user?id={replyuser.id}'>{replyuser.first_name}</a>")
        if message.text.lower() == "обнять":
            reply = message.reply_to_message
            if reply:
                replyuser = reply.from_user
                await bot.send_message(message.chat.id, f"<a href='tg://user?id={user.id}'>{user.first_name}</a> обнял(-а) <a href='tg://user?id={replyuser.id}'>{replyuser.first_name}</a>")
        if message.text.lower() == "шлеп":
            reply = message.reply_to_message
            if reply:
                replyuser = reply.from_user
                await bot.send_message(message.chat.id, f"<a href='tg://user?id={user.id}'>{user.first_name}</a> шлепнул(-а) <a href='tg://user?id={replyuser.id}'>{replyuser.first_name}</a>")
        if message.text.lower() == "убить":
            reply = message.reply_to_message
            if reply:
                replyuser = reply.from_user
                await bot.send_message(message.chat.id, f"<a href='tg://user?id={user.id}'>{user.first_name}</a> убил(-а) <a href='tg://user?id={replyuser.id}'>{replyuser.first_name}</a>")
        if message.text.lower() == "выебать":
            reply = message.reply_to_message
            if reply:
                replyuser = reply.from_user
                await bot.send_message(message.chat.id, f"<a href='tg://user?id={user.id}'>{user.first_name}</a> выебал(-а) <a href='tg://user?id={replyuser.id}'>{replyuser.first_name}</a>")
        if message.text.lower() == "связать":
            reply = message.reply_to_message
            if reply:
                replyuser = reply.from_user
                await bot.send_message(message.chat.id, f"<a href='tg://user?id={user.id}'>{user.first_name}</a> связал(-а) <a href='tg://user?id={replyuser.id}'>{replyuser.first_name}</a>")
        if message.text.lower() == "ударить":
            reply = message.reply_to_message
            if reply:
                replyuser = reply.from_user
                await bot.send_message(message.chat.id, f"<a href='tg://user?id={user.id}'>{user.first_name}</a> ударил(-а) <a href='tg://user?id={replyuser.id}'>{replyuser.first_name}</a>")
        if message.text.lower() == "уебать":
            reply = message.reply_to_message
            if reply:
                replyuser = reply.from_user
                await bot.send_message(message.chat.id, f"<a href='tg://user?id={user.id}'>{user.first_name}</a> уебал(-а) <a href='tg://user?id={replyuser.id}'>{replyuser.first_name}</a>")
        if message.text.lower() == "отсосать":
            reply = message.reply_to_message
            if reply:
                replyuser = reply.from_user
                await bot.send_message(message.chat.id, f"<a href='tg://user?id={user.id}'>{user.first_name}</a> отсосал(-а) у <a href='tg://user?id={replyuser.id}'>{replyuser.first_name}</a>")
        if message.text.lower() == "отлизать":
            reply = message.reply_to_message
            if reply:
                replyuser = reply.from_user
                await bot.send_message(message.chat.id, f"<a href='tg://user?id={user.id}'>{user.first_name}</a> отлизал(-а) у <a href='tg://user?id={replyuser.id}'>{replyuser.first_name}</a>")
        if message.text.lower() == "задушить":
            reply = message.reply_to_message
            if reply:
                replyuser = reply.from_user
                await bot.send_message(message.chat.id, f"<a href='tg://user?id={user.id}'>{user.first_name}</a> задушил(-а) <a href='tg://user?id={replyuser.id}'>{replyuser.first_name}</a>")
        if message.text.lower() == "украсть":
            reply = message.reply_to_message
            if reply:
                replyuser = reply.from_user
                await bot.send_message(message.chat.id, f"<a href='tg://user?id={user.id}'>{user.first_name}</a> украл(-а) <a href='tg://user?id={replyuser.id}'>{replyuser.first_name}</a>")
        if message.text.lower() == "погладить":
            reply = message.reply_to_message
            if reply:
                replyuser = reply.from_user
                await bot.send_message(message.chat.id, f"<a href='tg://user?id={user.id}'>{user.first_name}</a> погладил(-а) <a href='tg://user?id={replyuser.id}'>{replyuser.first_name}</a>")
        if message.text.lower() == "притянуть":
            reply = message.reply_to_message
            if reply:
                replyuser = reply.from_user
                await bot.send_message(message.chat.id, f"<a href='tg://user?id={user.id}'>{user.first_name}</a> притянул(-а) <a href='tg://user?id={replyuser.id}'>{replyuser.first_name}</a>")
        if message.text.lower() == "изнасиловать":
            reply = message.reply_to_message
            if reply:
                replyuser = reply.from_user
                await bot.send_message(message.chat.id, f"<a href='tg://user?id={user.id}'>{user.first_name}</a> изнасиловал(-а) <a href='tg://user?id={replyuser.id}'>{replyuser.first_name}</a>")
        if message.text.lower() == "отпороть":
            reply = message.reply_to_message
            if reply:
                replyuser = reply.from_user
                await bot.send_message(message.chat.id, f"<a href='tg://user?id={user.id}'>{user.first_name}</a> отпорол(-а) <a href='tg://user?id={replyuser.id}'>{replyuser.first_name}</a>")
    elif chat_data[2] == 0:
        return

@dp.message_handler(content_types=["pinned_message"])
async def pinned(message: types.Message):
    pinned = random.choice(["Дерьмо!", "ахахахах", "хуйня полная!", "ахуеть круто!", "сука нахуя я это прочитал?", "ты идиот?"])
    await message.reply(f"{pinned}")

@dp.message_handler(Text("снять штаны", ignore_case=True))
async def take_off_pants_message(message: types.Message):
    if not message.reply_to_message:
        await message.reply("Эта команда должна быть ответом на сообщение !")
        return

    await message.answer(
        f"""<a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a> снял штаны 🩳🔞  у <a href="tg://user?id={message.reply_to_message.from_user.id}">{message.reply_to_message.from_user.first_name}</a>""")

@dp.message_handler(Text("gay", ignore_case=True))
async def gay_message(message: types.Message):
    if not message.reply_to_message:
        await message.reply("Эта команда должна быть ответом на сообщение !")
        return

    await message.answer(
        f"""<a href="tg://user?id={message.reply_to_message.from_user.id}">{message.reply_to_message.from_user.first_name}</a> гей 🏳️‍🌈 👬  на {random.randint(0, 100)}%""")

@dp.message_handler(Text("поцеловать", ignore_case=True))
async def kiss_message(message: types.Message):
    if not message.reply_to_message:
        await message.reply("Эта команда должна быть ответом на сообщение !")
        return

    y = ["😚", "😙", "😗", "😘"]
    o = random.choice(y)
    await message.answer(
        f"""<a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a> поцеловал {o}  <a href="tg://user?id={message.reply_to_message.from_user.id}">{message.reply_to_message.from_user.first_name}</a>""")


@dp.message_handler(Text("выебать", ignore_case=True))
async def fuck_message(message: types.Message):
    if not message.reply_to_message:
        await message.reply("Эта команда должна быть ответом на сообщение !")
        return

    await message.answer(
        f"""<a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a> выебал(а) 💪👉👌  <a href="tg://user?id={message.reply_to_message.from_user.id}">{message.reply_to_message.from_user.first_name}</a>""")


@dp.message_handler(Text("обнять", ignore_case=True))
async def hug_message(message: types.Message):
    if not message.reply_to_message:
        await message.reply("Эта команда должна быть ответом на сообщение !")
        return

    await message.answer(
        f"""<a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a> обнял(а) 🤗  <a href="tg://user?id={message.reply_to_message.from_user.id}">{message.reply_to_message.from_user.first_name}</a>""")


@dp.message_handler(Text("послать нахуй", ignore_case=True))
async def hug_message(message: types.Message):
    if not message.reply_to_message:
        await message.reply("Эта команда должна быть ответом на сообщение !")
        return

    await message.answer(
        f"""<a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a> послал(а) 🤗  <a href="tg://user?id={message.reply_to_message.from_user.id}">{message.reply_to_message.from_user.first_name}</a> нахуй 🖕😬""")


@dp.message_handler(Text("пнуть", ignore_case=True))
async def kick_message(message: types.Message):
    if not message.reply_to_message:
        await message.reply("Эта команда должна быть ответом на сообщение !")
        return

    await message.answer(
        f"""<a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a> пнул(а) 👞 <a href="tg://user?id={message.reply_to_message.from_user.id}">{message.reply_to_message.from_user.first_name}</a>""")


@dp.message_handler(Text("пожать руку", ignore_case=True))
async def shake_hands_message(message: types.Message):
    if not message.reply_to_message:
        await message.reply("Эта команда должна быть ответом на сообщение !")
        return

    await message.answer(
        f"""<a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a> пожал(а) руку 🤝 <a href="tg://user?id={message.reply_to_message.from_user.id}">{message.reply_to_message.from_user.first_name}</a>""")


@dp.message_handler(Text("ущипнуть попку", ignore_case=True))
async def pinch_ass_message(message: types.Message):
    if not message.reply_to_message:
        await message.reply("Эта команда должна быть ответом на сообщение !")
        return

    await message.answer(
        f"""<a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a> ущипнул(а) попку 🍑🤏 <a href="tg://user?id={message.reply_to_message.from_user.id}">{message.reply_to_message.from_user.first_name}</a>""")


@dp.message_handler(Text("потрогать член", ignore_case=True))
async def touch_penis(message: types.Message):
    if not message.reply_to_message:
        await message.reply("Эта команда должна быть ответом на сообщение !")
        return

    await message.answer(
        f"""<a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a> потрогал(а) член 🍌🤏 <a href="tg://user?id={message.reply_to_message.from_user.id}">{message.reply_to_message.from_user.first_name}</a>""")


@dp.message_handler(Text("трахнуть", ignore_case=True))
async def fuck2_message(message: types.Message):
    if not message.reply_to_message:
        await message.reply("Эта команда должна быть ответом на сообщение !")
        return

    await message.answer(
        f"""<a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a> трахнул(а) 👉👌  <a href="tg://user?id={message.reply_to_message.from_user.id}">{message.reply_to_message.from_user.first_name}</a>""")


@dp.message_handler(Text("отсосать", ignore_case=True))
async def suck_off_message(message: types.Message):
    if not message.reply_to_message:
        await message.reply("Эта команда должна быть ответом на сообщение !")
        return

    await message.answer(
        f"""<a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a> отсосал(а) 👄🍌 у <a href="tg://user?id={message.reply_to_message.from_user.id}">{message.reply_to_message.from_user.first_name}</a>""")


@dp.message_handler(Text("подрочить", ignore_case=True))
async def jerk_off_message(message: types.Message):
    await message.answer(
        f"""<a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a> успешно подрочил 🍆 и получил удовольствие 💦.""")


@dp.message_handler(Text("подрочить на", ignore_case=True))
async def jerk2_off_message(message: types.Message):
    if not message.reply_to_message:
        await message.reply("Эта команда должна быть ответом на сообщение !")
        return

    await message.answer(
        f"""<a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a> подрочил(а) 🍆  на <a href="tg://user?id={message.reply_to_message.from_user.id}">{message.reply_to_message.from_user.first_name}</a>""")

@dp.message_handler(Text("ударить", ignore_case=True))
async def hit_message(message: types.Message):
    if not message.reply_to_message:
        await message.reply("Эта команда должна быть ответом на сообщение !")
        return

    await message.answer(
        f"""<a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a> ударил(а) 👊 <a href="tg://user?id={message.reply_to_message.from_user.id}">{message.reply_to_message.from_user.first_name}</a>""")

@dp.message_handler(Text("ударить сковородкой", ignore_case=True))
async def hit2_message(message: types.Message):
    if not message.reply_to_message:
        await message.reply("Эта команда должна быть ответом на сообщение !")
        return

    await message.answer(
        f"""<a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a> ударил(а) сковородкой 💥👊 <a href="tg://user?id={message.reply_to_message.from_user.id}">{message.reply_to_message.from_user.first_name}</a>""")

