from misc import bot, dp, conn, cursor, button_marry, button_marry_y, button_marry_n, button_divorce, button_divorce_y, button_divorce_n
from aiogram.types import Message
from aiogram import types
from .functions import *
from aiogram.utils.markdown import quote_html
import time
from time import gmtime
from time import strftime

marry_me = []
marry_rep = []
divorce_me = []
divorce_rep = []

@dp.callback_query_handler(lambda c: c.data == "button_marry_y")
async def callback_marry_y(callback_query: types.CallbackQuery):
    user = await bot.get_chat(str(marry_me[0]))
    replyuser = await bot.get_chat(str(marry_rep[0]))
    name = quote_html(user.full_name)
    rname = quote_html(replyuser.full_name)
    if callback_query.from_user.id == replyuser.id:
        cursor.execute(f'UPDATE users SET marry=? WHERE user_id=?', (replyuser.id, user.id,))
        cursor.execute(f'UPDATE users SET marry_time=? WHERE user_id=?', (time.time(), user.id,))

        cursor.execute(f'UPDATE users SET marry=? WHERE user_id=?', (user.id, replyuser.id,))
        cursor.execute(f'UPDATE users SET marry_time=? WHERE user_id=?', (time.time(), replyuser.id,))
        conn.commit()

        marry_me.clear()
        marry_rep.clear()
        await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
        await bot.send_message(callback_query.message.chat.id, f"<a href='tg://user?id={user.id}'>{name}</a> и <a href='tg://user?id={replyuser.id}'>{rname}</a> теперь в браке❤️")
    else:
        await bot.answer_callback_query(callback_query.id, text="Не трогай!", show_alert=True)

@dp.callback_query_handler(lambda c: c.data == "button_marry_n")
async def callback_marry_n(callback_query: types.CallbackQuery):
    user = await bot.get_chat(str(marry_me[0]))
    replyuser = await bot.get_chat(str(marry_rep[0]))
    if callback_query.from_user.id == replyuser.id:
        name = quote_html(user.full_name)
        marry_me.clear()
        marry_rep.clear()
        await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
        await bot.send_message(callback_query.message.chat.id, f"<a href='tg://user?id={user.id}'>{name}</a>, сожалеем но вам отказали")
    else:
        await bot.answer_callback_query(callback_query.id, text="Не трогай!", show_alert=True)

@dp.callback_query_handler(lambda c: c.data == "button_divorce_y")
async def callback_divorce_y(callback_query: types.CallbackQuery):
    user = await bot.get_chat(str(divorce_me[0]))
    if callback_query.from_user.id == user.id:
        replyuser = await bot.get_chat(str(divorce_rep[0]))
        name = quote_html(user.full_name)
        get = cursor.execute("SELECT marry_time FROM users WHERE user_id=?", (user.id,)).fetchall()
        mtime = f"{int(get[0][0])}"
        marry_time = time.time() - float(mtime)
        vremya = strftime("%j дней %H часов %M минут", gmtime(marry_time))
        cursor.execute(f'UPDATE users SET marry=? WHERE user_id=?', (0, user.id,))
        cursor.execute(f'UPDATE users SET marry_time=? WHERE user_id=?', (0, user.id,))

        cursor.execute(f'UPDATE users SET marry=? WHERE user_id=?', (0, replyuser.id,))
        cursor.execute(f'UPDATE users SET marry_time=? WHERE user_id=?', (0, replyuser.id,))
        conn.commit()
        divorce_me.clear()
        divorce_rep.clear()
        await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
        await bot.send_message(callback_query.message.chat.id, f"<a href='tg://user?id={user.id}'>{name}</a>, ваш брак расторгнут.\n"
                                                               f"Он просуществовал {vremya}")
    else:
        await bot.answer_callback_query(callback_query.id, text="Не трогай!", show_alert=True)

@dp.callback_query_handler(lambda c: c.data == "button_divorce_n")
async def callback_divorce_n(callback_query: types.CallbackQuery):
    user = await bot.get_chat(str(divorce_me[0]))
    if callback_query.from_user.id == user.id:
        divorce_me.clear()
        divorce_rep.clear()
        await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    else:
        await bot.answer_callback_query(callback_query.id, text="Не трогай!", show_alert=True) #слито в @smoke_software


@dp.message_handler(commands=['брак'])
async def cmd_marry(message: types.Message):
    data = await get_rang(message)
    if data is None:
        return await message.reply(f"🚫 <b>Не найден в базе данных.</b>\n\n"
                                   f"/start в лс у бота!")
    user = message.from_user
    name = quote_html(user.full_name)
    reply = message.reply_to_message
    if reply:
        replyuser = reply.from_user
        rname = quote_html(replyuser.full_name)
        if data[6] == 0:
            if replyuser.id == user.id:
                return await message.reply(f"Вы не можете сделать брак с самим собой.")
            replydata = await reply_get_rang(message)
            if replydata[6] == 0:
                marry_me.append(user.id)
                marry_rep.append(replyuser.id)
                await bot.send_message(message.chat.id, f"<a href='tg://user?id={replyuser.id}'>{rname}</a>, вы готовы заключить брак с <a href='tg://user?id={user.id}'>{name}</a> ?", reply_markup=button_marry)
            else:
                marry = cursor.execute("SELECT marry FROM users WHERE user_id=?", (replyuser.id,)).fetchall()
                marred = await bot.get_chat(str(marry[0][0]))
                mname = quote_html(marred.full_name)
                return await message.reply(f"{rname}, уже в браке с {mname}")
        else:
            marry = cursor.execute("SELECT marry FROM users WHERE user_id=?", (user.id,)).fetchall()
            marred = await bot.get_chat(str(marry[0][0]))
            mname = quote_html(marred.full_name)
            return await message.reply(f"Вы уже в браке с {mname}❤️")

@dp.message_handler(commands=['развод'])
async def cmd_divorce(message: types.Message):
    data = await get_rang(message)
    if data is None:
        return await message.reply(f"🚫 <b>Не найден в базе данных.</b>\n\n"
                                   f"/start в лс у бота!")
    user = message.from_user
    name = quote_html(user.full_name)
    if data[6] == 0:
        return await message.reply(f"У вас нет брака💔")
    else:
        marry = cursor.execute("SELECT marry FROM users WHERE user_id=?", (user.id,)).fetchall()
        marred = await bot.get_chat(str(marry[0][0]))
        mname = quote_html(marred.full_name)
        divorce_me.append(user.id)
        divorce_rep.append(marred.id)
        await bot.send_message(message.chat.id, f"<a href='tg://user?id={user.id}'>{name}</a>, вы уверены что хотите рассторгнуть брак с <a href='tg://user?id={marred.id}'>{mname}</a> ?💔", reply_markup=button_divorce)