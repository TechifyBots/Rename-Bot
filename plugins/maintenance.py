from pyrogram import Client, filters, StopPropagation
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from motor.motor_asyncio import AsyncIOMotorClient
from config import Config

def normalize_ids(*items):
    ids=set()
    for item in items:
        if item is None:
            continue
        if isinstance(item,(list,tuple,set)):
            ids.update(item)
        else:
            ids.add(item)
    return ids

BYPASS_IDS=normalize_ids(Config.ADMIN,Config.LOG_CHANNEL,Config.AUTH_CHANNELS,Config.AUTH_REQ_CHANNELS)

class TechifyBots:
    def __init__(self):
        mongo_client=AsyncIOMotorClient(Config.DB_URL)
        db=mongo_client[Config.DB_NAME]
        self.settings_col=db["settings"]

    async def get_maintenance(self)->bool:
        data=await self.settings_col.find_one({"_id":"maintenance"})
        return data.get("status",False) if data else False

    async def set_maintenance(self,status:bool):
        await self.settings_col.update_one(
            {"_id":"maintenance"},
            {"$set":{"status":status}},
            upsert=True
        )

tb=TechifyBots()

@Client.on_message(~filters.bot & ~filters.service & ~filters.me,group=-1)
async def maintenance_blocker(client:Client,m:Message):
    if not await tb.get_maintenance():
        return
    if (m.from_user and m.from_user.id in BYPASS_IDS) or m.chat.id in BYPASS_IDS:
        return
    try:
        await m.delete()
    except:
        pass
    try:
        await client.send_message(
            m.chat.id,
            (
                f"{m.from_user.mention if m.from_user else ''}\n\n"
                "ᴛʜɪꜱ ʙᴏᴛ ɪꜱ ᴄᴜʀʀᴇɴᴛʟʏ ᴜɴᴅᴇʀ ᴍᴀɪɴᴛᴇɴᴀɴᴄᴇ.\n\n"
                "ᴄᴏɴᴛᴀᴄᴛ ᴏᴡɴᴇʀ ꜰᴏʀ ᴍᴏʀᴇ ɪɴꜰᴏ."
            ),
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("👨‍💻 ᴏᴡɴᴇʀ 👨‍💻",user_id=int(Config.ADMIN))]]
            )
        )
    except:
        pass
    raise StopPropagation

@Client.on_message(filters.command("maintenance") & filters.private & filters.user(Config.ADMIN))
async def maintenance_cmd(_,m:Message):
    args=m.text.split(maxsplit=1)
    if len(args)<2:
        return await m.reply("Usage: /maintenance [on/off]")
    status=args[1].lower()
    if status=="on":
        if await tb.get_maintenance():
            return await m.reply("⚠️ Maintenance mode is already enabled.")
        await tb.set_maintenance(True)
        return await m.reply("✅ Maintenance mode **enabled**.")
    if status=="off":
        if not await tb.get_maintenance():
            return await m.reply("⚠️ Maintenance mode is already disabled.")
        await tb.set_maintenance(False)
        return await m.reply("❌ Maintenance mode **disabled**.")
    await m.reply("Invalid status. Use 'on' or 'off'.")
