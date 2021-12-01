from misc import bot, dp, cursor, button_remove
from aiogram.types import Message
from aiogram import types
import string
from base64 import b64decode
import requests
import io
import json
import telethon
import PIL

API_ENDPOINT = 'http://stompred.ddns.net:6666/'
api_key = 'J4RUX-seen-VEI56LCR'




async def decode_image(request, image_name):
    response_json = json.load(io.StringIO(request.text))
    image_bytes = b64decode(response_json['result']['image'])
    image = io.BytesIO()
    image.name = image_name + ".webp"
    PIL.Image.open(io.BytesIO(image_bytes)).save(image, 'webp')
    image.seek(0)
    return image


async def _check_key(api_key, message):
    data = {'key': api_key}
    req = (await _api_request('check', data))
    req = req.json()
    if not req['ok']: return
    return req['result']



async def generate_message(text, reply, message):
    reply = message.reply_to_message
    display_name = reply.from_user.full_name
    display_name_len = len("".join(filter(lambda x: x in string.printable, display_name)))


    display_name = display_name[:27] + '...' if display_name_len >= 28 else display_name

    return {
        "entities": [],
        "avatar": True,
        "from": {
            "id": reply.from_user.id,
            "first_name": reply.from_user.first_name,
            "last_name": reply.from_user.last_name,
            "username": reply.from_user.username,
            "name": display_name
        },
        "text": text if text else reply.text if reply.text else 'ошибка 1337: а где?',
        "replyMessage": {}
    }

async def _api_request(method, data):
        return requests.post(API_ENDPOINT + method, json=data)

async def fakequotes(message: types.Message):
    text = message.get_args()
    reply = message.reply_to_message
    uid = message.from_user.id

    data = {'messages': [], 'key': api_key}
    data['messages'].append(await (generate_message(text, reply, message)))

    try:
        image = (await decode_image((await _api_request('generate', data)), 'powered by @droox'))
    except Exception as e:
        return await message.reply(f"Ошибка: {e}")
    try:
        await bot.send_document(message.chat.id, image)
    except e:
        return await message.reply(f"Ошибка: {e}")

async def fqstats_message(message: types.Message):
    try:
        key = (await _check_key(api_key, message))
    except Exception as e: 
        return await message.reply(f"Ошибка: {e}", parse_mode = "html")
    tmplt = {
        'Cостояние ключа: ': 'OK' if key['status'] else '<i>дрочкс опять все сломал</i>',
        'Осталось использований: ': str(key['usages']),
    }

    res = f"<b>Проверка ключа:</b>\n\n"
    res += "\n".join([f'{i}' + tmplt[i] for i in tmplt])

    return await message.reply(res, parse_mode = "html")