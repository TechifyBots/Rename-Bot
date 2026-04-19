__name__ = "Rename-Bot"
__version__ = "3.1.0"
__license__ = " Apache License, Version 2.0"
__copyright__ = "Copyright (C) 2022-present Digital Botz <https://github.com/DigitalBotz>"
__programer__ = "<a href=https://github.com/TechifyBots/Rename-Bot>Techify Bots</a>"
__library__ = "<a href=https://github.com/pyrogram>Pyʀᴏɢʀᴀᴍ</a>"
__language__ = "<a href=https://www.python.org/>Pyᴛʜᴏɴ 3</a>"
__database__ = "<a href=https://cloud.mongodb.com/>Mᴏɴɢᴏ DB</a>"
__developer__ = "<a href=https://t.me/TechifyBots>Techify Bots</a>"
__maindeveloper__ = "<a href=https://t.me/Digital_Botz>Digital Botz</a>"


from pyrogram import Client, filters
import datetime
from helper.database import digital_botz

@Client.on_message(filters.private)
async def _(bot, message):
    await digital_botz.add_user(bot, message) 
    user_id = message.from_user.id
    ban_status = await digital_botz.get_ban_status(user_id)
    if ban_status.get("is_banned", False):
        if ( datetime.date.today() - datetime.date.fromisoformat(ban_status["banned_on"])
        ).days > ban_status["ban_duration"]:
            await digital_botz.remove_ban(user_id)
        else:
            return await message.reply_text("Sorry Sir, 😔 You are Banned!.. Please Contact - @TechifyBots") 
    await message.continue_propagation()
