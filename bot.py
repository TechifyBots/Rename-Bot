import aiohttp, asyncio, datetime
from zoneinfo import ZoneInfo
import logging
import logging.config
from pyrogram import Client, __version__, errors
from pyrogram.raw.all import layer
from pyrogram import idle
from config import Config
from plugins.web_support import web_server
from plugins.file_rename import app

# Get logging configurations
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler('BotLog.txt'),
             logging.StreamHandler()]
)
#logger = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

class TechifyBots(Client):
    def __init__(self):
        super().__init__(
            name="RenameBot",
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            bot_token=Config.BOT_TOKEN,
            workers=200,
            plugins={"root": "plugins"},
            sleep_threshold=5,
            max_concurrent_transmissions=50
        )
                
         
    async def start(self):
        await super().start()
        me = await self.get_me()
        self.mention = me.mention
        self.username = me.username  
        self.uptime = Config.BOT_UPTIME
        self.premium = Config.PREMIUM_MODE
        self.uploadlimit = Config.UPLOAD_LIMIT_MODE
        Config.BOT = self
        
        self._web_runner = aiohttp.web.AppRunner(await web_server())
        await self._web_runner.setup()
        bind_address = "0.0.0.0"
        await aiohttp.web.TCPSite(self._web_runner, bind_address, Config.PORT).start()

        print(f"{me.first_name} Iꜱ Sᴛᴀʀᴛᴇᴅ.....✨️")

        
        if Config.ADMIN:
            if Config.STRING_SESSION:
                try:
                    await self.send_message(Config.ADMIN, f"𝟮𝗚𝗕+ ғɪʟᴇ sᴜᴘᴘᴏʀᴛ ʜᴀs ʙᴇᴇɴ ᴀᴅᴅᴇᴅ ᴛᴏ ʏᴏᴜʀ ʙᴏᴛ.\n\nNote: 𝐓𝐞𝐥𝐞𝐠𝐫𝐚𝐦 𝐩𝐫𝐞𝐦𝐢𝐮𝐦 𝐚𝐜𝐜𝐨𝐮𝐧𝐭 𝐬𝐭𝐫𝐢𝐧𝐠 𝐬𝐞𝐬𝐬𝐢𝐨𝐧 𝐫𝐞𝐪𝐮𝐢𝐫𝐞𝐝 𝐓𝐡𝐞𝐧 𝐬𝐮𝐩𝐩𝐨𝐫𝐭𝐬 𝟐𝐆𝐁+ 𝐟𝐢𝐥𝐞𝐬.\n\n**__{me.first_name}  Iꜱ Sᴛᴀʀᴛᴇᴅ.....✨️__**")
                except Exception:
                    pass
            else:
                try:
                    await self.send_message(Config.ADMIN, f"𝟮𝗚𝗕- ғɪʟᴇ sᴜᴘᴘᴏʀᴛ ʜᴀs ʙᴇᴇɴ ᴀᴅᴅᴇᴅ ᴛᴏ ʏᴏᴜʀ ʙᴏᴛ.\n\n**__{me.first_name}  Iꜱ Sᴛᴀʀᴛᴇᴅ.....✨️__**")
                except Exception:
                    pass
                    
        if Config.LOG_CHANNEL:
            try:
                curr = datetime.datetime.now(ZoneInfo("Asia/Kolkata"))
                date = curr.strftime('%d %B, %Y')
                time = curr.strftime('%I:%M:%S %p')
                await self.send_message(Config.LOG_CHANNEL, f"**__{me.mention} Iꜱ Rᴇsᴛᴀʀᴛᴇᴅ !!**\n\n📅 Dᴀᴛᴇ : `{date}`\n⏰ Tɪᴍᴇ : `{time}`\n🌐 Tɪᴍᴇᴢᴏɴᴇ : `Asia/Kolkata`\n\n🉐 Vᴇʀsɪᴏɴ : `v{__version__} (Layer {layer})`</b>")
            except Exception:
                print("Pʟᴇᴀꜱᴇ Mᴀᴋᴇ Tʜɪꜱ Iꜱ Aᴅᴍɪɴ Iɴ Yᴏᴜʀ Lᴏɢ Cʜᴀɴɴᴇʟ")

    async def stop(self, *args):
        if Config.ADMIN:
            try:
                await self.send_message(Config.ADMIN, "**Bot Stopped....**")
            except Exception:
                pass
                
        print("Bot Stopped 🙄")
        runner = getattr(self, "_web_runner", None)
        if runner is not None:
            await runner.cleanup()
        await super().stop()


tb = TechifyBots()

def main():
    async def start_services():
        if Config.STRING_SESSION:
            await asyncio.gather(app.start(), tb.start())
        else:
            await asyncio.gather(tb.start())
        
        # Idle mode start karo
        await idle()
        
        # Bot stop karo
        if Config.STRING_SESSION:
            await asyncio.gather(app.stop(), tb.stop())
        else:
            await asyncio.gather(tb.stop())

    try:
        asyncio.run(start_services())
    except KeyboardInterrupt:
        print("\n🛑 Bot stopped by user!")

if __name__ == "__main__":
    try:
        main()
    except errors.FloodWait as ft:
        print(f"⏳ FloodWait: Sleeping for {ft.value} seconds")
        asyncio.run(asyncio.sleep(ft.value))
        print("Now Ready For Deploying!")
        main()
