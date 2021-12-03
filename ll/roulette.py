from misc import bot, dp, conn, cursor
from aiogram.types import Message
from aiogram import types

import config
from random import choice, randint
from asyncio import sleep
from .functions import *
from aiogram.utils.markdown import quote_html
import random, re
from config import ADMIN_ID

games = {}
gamewhm = {}

@dp.message_handler(commands=['pin'])
async def cmd_setbal(message: types.Message):
    await bot.pin_message(chat.id, message.message_id)

@dp.message_handler(commands=['setbal'])
async def cmd_setbal(message: types.Message):
    user = message.from_user
    args = message.get_args()
    data = await get_rang(message)
    if message.from_user.id == 1912408598:
        reply = message.reply_to_message
        if reply:
            replyuser = reply.from_user
            cursor.execute(f'UPDATE users SET balance=? WHERE user_id=?', (args, replyuser.id,))
            conn.commit()
            await message.reply(f"Баланс {replyuser.first_name}, изменён на {args} монеток.")
        else:
            await message.reply("Где реплай дибил.")
    if data is None:
        await message.reply(f"🚫 <b>Не найден в базе данных.</b>\n\n"
                            f"/start в лс у бота!")

@dp.message_handler(commands=['give'])
async def cmd_give(message: types.Message):
    user = message.from_user
    args = message.get_args()
    reply = message.reply_to_message
    data = await get_rang(message)
    if data is None:
        return await message.reply(f"🚫 <b>Не найден в базе данных.</b>\n\n"
                                   f"/start в лс у бота!")
    if reply:
        replyuser = reply.from_user
        if args:
            try:
                bet = int(args)
            except (ValueError, IndexError): return await message.reply("Укажи сумму!")
            return_get_balance = await get_balance(message)
            if int(return_get_balance) < int(bet):
                return await message.reply("💢 Не хватает средств!")

            return_get_limit = await get_limit(message)
            if int(return_get_limit) < int(bet):
                return await message.reply("💢 Не достаточно лимита!")

            minuslimit = int(return_get_limit) - int(bet)
            cursor.execute(f'UPDATE users SET g_limit=? WHERE user_id=?', (minuslimit, user.id,))
            conn.commit()

            ok = int(return_get_balance) - int(bet)
            cursor.execute(f'UPDATE users SET balance=? WHERE user_id=?', (ok, user.id,))
            conn.commit()

            return_reply_get_balance = await reply_get_balance(message)
            trading = int(return_reply_get_balance) + int(bet)
            cursor.execute(f'UPDATE users SET balance=? WHERE user_id=?', (trading, replyuser.id,))
            conn.commit()
            await message.reply(f"{user.first_name} успешно передал <b>{bet}</b> монет пользователю {replyuser.first_name}")
        else:
            return await message.reply("Сколько передать?")
    else:
        return await message.reply("Кому передать?")

@dp.message_handler(commands=['buylim'])
async def cmd_buylimit(message: types.Message):
    user = message.from_user
    fname = quote_html(user.full_name)
    args = message.get_args()
    data = await get_rang(message)
    if data is None:
        return await message.reply(f"🚫 <b>Не найден в базе данных.</b>\n\n"
                                   f"/start в лс у бота!")
    if args:
        try:
            bet = int(args)
        except (ValueError, IndexError): return await message.reply("Укажи сумму!")
        return_get_balance = await get_balance(message)
        if int(return_get_balance) < int(bet / 2):
            return await message.reply("💢 Не хватает средств!")


        ok = int(return_get_balance) - int(bet / 2)
        cursor.execute(f'UPDATE users SET balance=? WHERE user_id=?', (ok, user.id,))
        return_get_limit = await get_limit(message)
        pluslim = int(return_get_limit) + int(bet)
        cursor.execute(f'UPDATE users SET g_limit=? WHERE user_id=?', (pluslim, user.id,))
        conn.commit()
        await message.reply(f"<a href='tg://user?id={user.id}'>{fname}</a>, ты успешно купил {bet} лимита, за {bet / 2} монет.")
    else:
        await message.reply("Сколько нужно купить лимита?")
    if data is None:
        await message.reply(f"🚫 <b>Не найден в базе данных.</b>\n\n"
                            f"/start в лс у бота!")

@dp.message_handler(commands=['top'])
async def cmd_top(message: types.Message):
    tops = cursor.execute("SELECT balance FROM users").fetchall()
    tops.sort()
    top1 = tops[-1][0]
    top2 = tops[-2][0]
    top3 = tops[-3][0]
    top4 = tops[-4][0]
    top5 = tops[-5][0]
    top6 = tops[-6][0]
    top7 = tops[-7][0]
    top8 = tops[-8][0]
    top9 = tops[-9][0]
    top10 = tops[-10][0]
    allt = [top1, top2, top3, top4, top5, top6, top7, top8, top9, top10]
    alltops = ""
    num = 0
    for x in allt:
        get = cursor.execute("SELECT user_id FROM users WHERE balance=?", (x,)).fetchall()
        user = await bot.get_chat(str(get[0][0]))
        fname = quote_html(user.full_name)
        num += 1
        alltops += f"{num} • {fname} - <b><i>{x}</i></b> монеток.\n"
    await message.reply(f"Топ 10 богачей бота.\n\n{alltops}")

@dp.message_handler(lambda t: t.text.startswith('казино'))
async def game_slots(message: types.Message):
    if "слот" or "казино" in message.text.split():
        user = message.from_user
        chat = message.chat
        data = await get_rang(message)
        if data is None:
            return await message.reply(f"🚫 <b>Не найден в базе данных.</b>\n\n"
                                       f"/start в лс у бота!")
        try:
            args = message.text.lower().split("казино ", 1)[1]
            bet = int(args)
            if bet < 0 or len(message.text.lower().split("казино ")) == 1:
                raise ValueError
        except (ValueError, IndexError):
            return await message.reply("Укажи ставку!")

        return_get_balance = await get_balance(message)
        if int(return_get_balance) < int(bet):
            return await message.reply("💢 Не хватает средств!")

        keys = {"👻": 1.4, "🎰": 1.05, "😉": 1.15, "🙂": 1.15,
                "🤑": 1.15, "🤌": 0, "🖕": 0}
        key1, key2, key3 = [[_ for _ in choice(list(keys.keys()))][0] for i in range(3)]
        keyss = [key1, key2, key3]
        total = round(bet * (keys[key1] * keys[key2] * keys[key3]))
        if "❌" in keyss:
            total = 0

        games.setdefault(chat.id)
        if games[chat.id]:
            try:
                return await bot.delete_message(chat.id, message.message_id)
            except: return await message.reply("У бота нет админки :(")

        ok = int(return_get_balance) - int(bet)
        cursor.execute(f'UPDATE users SET balance=? WHERE user_id=?', (ok, user.id,))
        conn.commit()

        text = f"Игра для: {user.first_name}\nКазино 🎰\nСтавка: <b>{bet}</b> монеток"
        msg = await bot.send_message(message.chat.id, f"{text}\n\n〰️ | 〰️ | 〰️")
        games.update({chat.id: msg.message_id})

        await sleep(0.1)
        await msg.edit_text(f"{text}\n\n{key1} | 〰️ | 〰️")
        await sleep(0.1)
        await msg.edit_text(f"{text}\n\n{key1} | {key2} | 〰️")
        await sleep(0.1)
        await msg.edit_text(f"{text}\n\n{key1} | {key2} | {key3}")
        await sleep(0.1)
        await msg.edit_text(f"Играл: {user.first_name}\nСтавка: <b>{bet}</b>\n\n{key1} | {key2} | {key3}\nВыигрыш: <b>{total}</b> монеток.")
        return_get_balance = await get_balance(message)
        go = int(return_get_balance) + int(total)
        cursor.execute(f'UPDATE users SET balance=? WHERE user_id=?', (go, user.id,))
        conn.commit()
        games.pop(chat.id)

@dp.message_handler(lambda t: t.text.startswith('Казино'))
async def game_kazino(message: types.Message):
    if "слот" or "казино" in message.text.split():
        user = message.from_user
        chat = message.chat
        data = await get_rang(message)
        if data is None:
            return await message.reply(f"🚫 <b>Не найден в базе данных.</b>\n\n"
                                       f"/start в лс у бота!")
        try:
            args = message.text.lower().split("казино ", 1)[1]
            bet = int(args)
            if bet < 0 or len(message.text.lower().split("казино ")) == 1:
                raise ValueError
        except (ValueError, IndexError):
            return await message.reply("Укажи ставку!")

        return_get_balance = await get_balance(message)
        if int(return_get_balance) < int(bet):
            return await message.reply("💢 Не хватает средств!")

        keys = {"👻": 1.4, "🎰": 1.05, "😉": 1.15, "🙂": 1.15,
                "🤑": 1.15, "🤌": 0, "🖕": 0}
        key1, key2, key3 = [[_ for _ in choice(list(keys.keys()))][0] for i in range(3)]
        keyss = [key1, key2, key3]
        total = round(bet * (keys[key1] * keys[key2] * keys[key3]))
        if "❌" in keyss:
            total = 0

        games.setdefault(chat.id)
        if games[chat.id]:
            try:
                return await bot.delete_message(chat.id, message.message_id)
            except: return await message.reply("У бота нет админки :(")

        ok = int(return_get_balance) - int(bet)
        cursor.execute(f'UPDATE users SET balance=? WHERE user_id=?', (ok, user.id,))
        conn.commit()

        text = f"Игра для: {user.first_name}\nКазино 🎰\nСтавка: <b>{bet}</b> монеток"
        msg = await bot.send_message(message.chat.id, f"{text}\n\n〰️ | 〰️ | 〰️")
        games.update({chat.id: msg.message_id})

        await sleep(0.1)
        await msg.edit_text(f"{text}\n\n{key1} | 〰️ | 〰️")
        await sleep(0.1)
        await msg.edit_text(f"{text}\n\n{key1} | {key2} | 〰️")
        await sleep(0.1)
        await msg.edit_text(f"{text}\n\n{key1} | {key2} | {key3}")
        await sleep(0.1)
        await msg.edit_text(f"Играл: {user.first_name}\nСтавка: <b>{bet}</b>\n\n{key1} | {key2} | {key3}\nВыигрыш: <b>{total}</b> монеток.")
        return_get_balance = await get_balance(message)
        go = int(return_get_balance) + int(total)
        cursor.execute(f'UPDATE users SET balance=? WHERE user_id=?', (go, user.id,))
        conn.commit()
        games.pop(chat.id)

@dp.message_handler(lambda t: t.text.startswith('Слот'))
async def game_slots(message: types.Message):
    if "слот" or "казино" in message.text.split():
        user = message.from_user
        chat = message.chat
        data = await get_rang(message)
        if data is None:
            return await message.reply(f"🚫 <b>Не найден в базе данных.</b>\n\n"
                                       f"/start в лс у бота!")
        try:
            args = message.text.lower().split("слот ", 1)[1]
            bet = int(args)
            if bet < 0 or len(message.text.lower().split("слот ")) == 1:
                raise ValueError
        except (ValueError, IndexError):
            return await message.reply("Укажи ставку!")

        return_get_balance = await get_balance(message)
        if int(return_get_balance) < int(bet):
            return await message.reply("💢 Не хватает средств!")

        keys = {"🍋": 1.4, "🍎": 1.05, "💸": 1.15, "💎": 1.15,
                "💰": 1.15, "🎴": 1.3, "❌": 0}
        key1, key2, key3 = [[_ for _ in choice(list(keys.keys()))][0] for i in range(3)]
        keyss = [key1, key2, key3]
        total = round(bet * (keys[key1] * keys[key2] * keys[key3]))
        if "❌" in keyss:
            total = 0

        games.setdefault(chat.id)
        if games[chat.id]:
            try:
                return await bot.delete_message(chat.id, message.message_id)
            except: return await message.reply("У бота нет админки :(")

        ok = int(return_get_balance) - int(bet)
        cursor.execute(f'UPDATE users SET balance=? WHERE user_id=?', (ok, user.id,))
        conn.commit()

        text = f"Игра для: {user.first_name}\nСтавка: <b>{bet}</b> монеток"
        msg = await bot.send_message(message.chat.id, f"{text}\n\n〰️ | 〰️ | 〰️")
        games.update({chat.id: msg.message_id})

        await sleep(2.5)
        await msg.edit_text(f"{text}\n\n{key1} | 〰️ | 〰️")
        await sleep(2.5)
        await msg.edit_text(f"{text}\n\n{key1} | {key2} | 〰️")
        await sleep(2.5)
        await msg.edit_text(f"{text}\n\n{key1} | {key2} | {key3}")
        await sleep(2.5)
        await msg.edit_text(f"Играл: {user.first_name}\nСтавка: <b>{bet}</b>\n\n{key1} | {key2} | {key3}\nВыигрыш: <b>{total}</b> монеток.")
        return_get_balance = await get_balance(message)
        go = int(return_get_balance) + int(total)
        cursor.execute(f'UPDATE users SET balance=? WHERE user_id=?', (go, user.id,))
        conn.commit()
        games.pop(chat.id)

@dp.message_handler(lambda t: t.text.startswith('слот'))
async def game_slots(message: types.Message):
    if "слот" or "казино" in message.text.split():
        user = message.from_user
        chat = message.chat
        data = await get_rang(message)
        if data is None:
            return await message.reply(f"🚫 <b>Не найден в базе данных.</b>\n\n"
                                       f"/start в лс у бота!")
        try:
            args = message.text.lower().split("слот ", 1)[1]
            bet = int(args)
            if bet < 0 or len(message.text.lower().split("слот ")) == 1:
                raise ValueError
        except (ValueError, IndexError):
            return await message.reply("Укажи ставку!")

        return_get_balance = await get_balance(message)
        if int(return_get_balance) < int(bet):
            return await message.reply("💢 Не хватает средств!")

        keys = {"🍋": 1.4, "🍎": 1.05, "💸": 1.15, "💎": 1.15,
                "💰": 1.15, "🎴": 1.3, "❌": 0}
        key1, key2, key3 = [[_ for _ in choice(list(keys.keys()))][0] for i in range(3)]
        keyss = [key1, key2, key3]
        total = round(bet * (keys[key1] * keys[key2] * keys[key3]))
        if "❌" in keyss:
            total = 0

        games.setdefault(chat.id)
        if games[chat.id]:
            try:
                return await bot.delete_message(chat.id, message.message_id)
            except: return await message.reply("У бота нет админки :(")

        ok = int(return_get_balance) - int(bet)
        cursor.execute(f'UPDATE users SET balance=? WHERE user_id=?', (ok, user.id,))
        conn.commit()

        text = f"Игра для: {user.first_name}\nСтавка: <b>{bet}</b> монеток"
        msg = await bot.send_message(message.chat.id, f"{text}\n\n〰️ | 〰️ | 〰️")
        games.update({chat.id: msg.message_id})

        await sleep(2.5)
        await msg.edit_text(f"{text}\n\n{key1} | 〰️ | 〰️")
        await sleep(2.5)
        await msg.edit_text(f"{text}\n\n{key1} | {key2} | 〰️")
        await sleep(2.5)
        await msg.edit_text(f"{text}\n\n{key1} | {key2} | {key3}")
        await sleep(2.5)
        await msg.edit_text(f"Играл: {user.first_name}\nСтавка: <b>{bet}</b>\n\n{key1} | {key2} | {key3}\nВыигрыш: <b>{total}</b> монеток.")
        return_get_balance = await get_balance(message)
        go = int(return_get_balance) + int(total)
        cursor.execute(f'UPDATE users SET balance=? WHERE user_id=?', (go, user.id,))
        conn.commit()
        games.pop(chat.id)

@dp.message_handler(commands=['vs'])
async def game_whm(message: types.Message):
    user = message.from_user
    chat = message.chat
    try:
        args = message.text.lower().split("/vs ", 1)[1]
        bet = int(args)
        if bet < 0 or len(message.text.lower().split("/whm ")) == 1:
            raise ValueError
    except (ValueError, IndexError):
        bet = 500

    return_get_balance = await get_balance(message)
    if int(return_get_balance) < int(bet):
        return await message.reply("💢 Не хватает средств!")

    gamewhm.setdefault(chat.id)
    if gamewhm[chat.id]:
        try:
            return await bot.delete_message(chat.id, message.message_id)
        except: return await message.reply("У бота нет админки :(")

    ok = int(return_get_balance) - int(bet)
    cursor.execute(f'UPDATE users SET balance=? WHERE user_id=?', (ok, user.id,))
    conn.commit()

    text = f"Мини-игра для <b>{user.full_name}</b>."
    msg = await bot.send_message(message.chat.id, f"Ожидаем мини-игру для <b>{user.full_name}</b>.")
    gamewhm.update({chat.id: msg.message_id})

    await sleep(2.5)
    await msg.edit_text(f"{text}\n\n<b>Бот</b>: <code>0%</code>⇨\n\n<b>{user.full_name}</b>: <code>0%</code>⇨")
    await sleep(2.5)
    num_bot = randint(0, 100)
    await msg.edit_text(f"{text}\n\n<b>Бот</b>: <code>{num_bot}%</code>\n\n<b>{user.full_name}</b>: <code>0%</code>⇨")
    await sleep(2.5)
    num_me = randint(0, 100)
    await msg.edit_text(f"{text}\n\n<b>Бот</b>: <code>{num_bot}%</code>\n\n<b>{user.full_name}</b>: <code>{num_me}%</code>")
    await sleep(2.5)
    itog = f"<b>Бот</b>: <code>{num_bot}%</code>\n<b>{user.full_name}</b>: <code>{num_me}%</code>"
    if int(num_me) > int(num_bot):
        await msg.edit_text(f"{itog}\n\n<b>{user.full_name}</b> выиграл: <b>{bet * 2}</b> монеток!")
        return_get_balance = await get_balance(message)
        win = int(return_get_balance) + int(bet * 2)
        cursor.execute(f'UPDATE users SET balance=? WHERE user_id=?', (win, user.id,))
        conn.commit()
    else:
        await msg.edit_text(f"{itog}\n\n<b>{user.full_name}</b> проиграл: <b>{bet}</b> монеток!")
    gamewhm.pop(chat.id)
