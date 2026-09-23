from pyrogram import Client, filters, StopPropagation
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pymongo import AsyncMongoClient
from config import Config
import time

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

BYPASS_IDS=normalize_ids(Config.ADMIN,Config.LOG_CHANNEL,Config.BIN_CHANNEL,Config.AUTH_CHANNELS,Config.AUTH_REQ_CHANNELS)

class TechifyBots:
    def __init__(self):
        mongo_client=AsyncMongoClient(Config.DB_URL)
        db=mongo_client[Config.DB_NAME]
        self.settings_col=db["settings"]
        self._maint_cache=None

    # 30s cache: the blocker runs on every message, and one Mongo round-trip per
    # message is disproportionate. /maintenance toggles now take up to 30s to apply.
    _MAINT_TTL = 30

    async def get_maintenance(self) -> bool:
        cached = self._maint_cache
        now = time.monotonic()
        if cached and now - cached[1] < self._MAINT_TTL:
            return cached[0]
        data = await self.settings_col.find_one({"_id": "maintenance"})
        value = data.get("status", False) if data else False
        self._maint_cache = (value, now)
        return value

    async def set_maintenance(self, status: bool):
        await self.settings_col.update_one(
            {"_id": "maintenance"},
            {"$set": {"status": status}},
            upsert=True
        )
        self._maint_cache = (status, time.monotonic())

tb=TechifyBots()

@Client.on_message(~filters.bot & ~filters.service & ~filters.me,group=-1)
async def maintenance_blocker(client:Client,m:Message):
    if not await tb.get_maintenance():
        return
    if (m.from_user and m.from_user.id in BYPASS_IDS) or m.chat.id in BYPASS_IDS:
        return
    try:
        await m.delete()
    except Exception:
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
    except Exception:
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
        return await m.reply("✅ Maintenance mode <b>enabled</b>.")
    if status=="off":
        if not await tb.get_maintenance():
            return await m.reply("⚠️ Maintenance mode is already disabled.")
        await tb.set_maintenance(False)
        return await m.reply("❌ Maintenance mode <b>disabled</b>.")
    await m.reply("Invalid status. Use 'on' or 'off'.")
