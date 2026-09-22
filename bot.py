import aiohttp, asyncio, datetime, signal
from zoneinfo import ZoneInfo
import logging
import logging.config, logging.handlers
from pyrogram import Client, __version__, errors, enums
from pyrogram.raw.all import layer
from html import escape
from config import Config
from helper.database import digital_botz
from plugins.web_support import web_server
from plugins.file_rename import app

# Structured logging: rotating file (canonical path from config) + console
_fmt = logging.Formatter("%(asctime)s | %(levelname)-8s | %(name)s | %(message)s")
_root = logging.getLogger()
_root.setLevel(logging.INFO)
_file = logging.handlers.RotatingFileHandler(
    Config.LOG_FILE, maxBytes=2_000_000, backupCount=3, encoding="utf-8"
)
_file.setFormatter(_fmt)
_stream = logging.StreamHandler()
_stream.setFormatter(_fmt)
_root.handlers = [_file, _stream]  # replace, keeps setup idempotent
logging.getLogger("pyrogram").setLevel(logging.WARNING)
logging.getLogger("pymongo").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

class TechifyBots(Client):
    def __init__(self):
        super().__init__(
            name="RenameBot",
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            bot_token=Config.BOT_TOKEN,
            parse_mode=enums.ParseMode.HTML,
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

        logger.info("%s Iꜱ Sᴛᴀʀᴛᴇᴅ.....✨️", me.first_name)

        
        if Config.ADMIN:
            if Config.STRING_SESSION:
                try:
                    await self.send_message(Config.ADMIN, f"𝟮𝗚𝗕+ ғɪʟᴇ sᴜᴘᴘᴏʀᴛ ʜᴀs ʙᴇᴇɴ ᴀᴅᴅᴇᴅ ᴛᴏ ʏᴏᴜʀ ʙᴏᴛ.\n\nNote: 𝐓𝐞𝐥𝐞𝐠𝐫𝐚𝐦 𝐩𝐫𝐞𝐦𝐢𝐮𝐦 𝐚𝐜𝐜𝐨𝐮𝐧𝐭 𝐬𝐭𝐫𝐢𝐧𝐠 𝐬𝐞𝐬𝐬𝐢𝐨𝐧 𝐫𝐞𝐪𝐮𝐢𝐫𝐞𝐝 𝐓𝐡𝐞𝐧 𝐬𝐮𝐩𝐩𝐨𝐫𝐭𝐬 𝟐𝐆𝐁+ 𝐟𝐢𝐥𝐞𝐬.\n\n<b><i>{escape(me.first_name)}  Iꜱ Sᴛᴀʀᴛᴇᴅ.....✨️</i></b>")
                except Exception:
                    pass
            else:
                try:
                    await self.send_message(Config.ADMIN, f"𝟮𝗚𝗕- ғɪʟᴇ sᴜᴘᴘᴏʀᴛ ʜᴀs ʙᴇᴇɴ ᴀᴅᴅᴇᴅ ᴛᴏ ʏᴏᴜʀ ʙᴏᴛ.\n\n<b><i>{escape(me.first_name)}  Iꜱ Sᴛᴀʀᴛᴇᴅ.....✨️</i></b>")
                except Exception:
                    pass
                    
        if Config.LOG_CHANNEL:
            try:
                curr = datetime.datetime.now(ZoneInfo("Asia/Kolkata"))
                date = curr.strftime('%d %B, %Y')
                time = curr.strftime('%I:%M:%S %p')
                await self.send_message(Config.LOG_CHANNEL, f"<b><i>{me.mention} Iꜱ Rᴇsᴛᴀʀᴛᴇᴅ !!</i></b>\n\n📅 Dᴀᴛᴇ : <code>{date}</code>\n⏰ Tɪᴍᴇ : <code>{time}</code>\n🌐 Tɪᴍᴇᴢᴏɴᴇ : <code>Asia/Kolkata</code>\n\n🉐 Vᴇʀsɪᴏɴ : <code>v{__version__} (Layer {layer})</code>")
            except Exception:
                logger.error("Pʟᴇᴀꜱᴇ Mᴀᴋᴇ Tʜɪꜱ Iꜱ Aᴅᴍɪɴ Iɴ Yᴏᴜʀ Lᴏɢ Cʜᴀɴɴᴇʟ")

    async def stop(self, *args):
        if Config.ADMIN:
            try:
                await self.send_message(Config.ADMIN, "<b>Bot Stopped....</b>")
            except Exception:
                pass
                
        runner = getattr(self, "_web_runner", None)
        if runner is not None:
            self._web_runner = None
            try:
                await runner.cleanup()
            except Exception:
                logging.getLogger(__name__).exception("web server cleanup failed")
        try:
            await super().stop()
        except Exception:
            pass
        logger.info("Bot Stopped 🙄")


tb = TechifyBots()

def main():
    async def start_services():
        stop_event = asyncio.Event()
        loop = asyncio.get_running_loop()
        for sig in (signal.SIGINT, signal.SIGTERM):
            try:
                loop.add_signal_handler(sig, stop_event.set)
            except (NotImplementedError, RuntimeError):
                pass  # event loop/platform without signal handler support

        started = []
        try:
            if Config.STRING_SESSION:
                started.append(app)
                await app.start()
            started.append(tb)
            await tb.start()
            await stop_event.wait()
        finally:
            logger.info("⏳ Shutting down gracefully...")
            for client in reversed(started):
                try:
                    await client.stop()
                except Exception:
                    logging.getLogger(__name__).exception("failed to stop a client")
            try:
                await digital_botz.close()
            except Exception:
                logging.getLogger(__name__).exception("failed to close database")

    try:
        asyncio.run(start_services())
    except KeyboardInterrupt:
        logger.info("🛑 Bot stopped by user!")

if __name__ == "__main__":
    try:
        main()
    except errors.FloodWait as ft:
        logger.warning(f"⏳ FloodWait: Sleeping for {ft.value} seconds")
        asyncio.run(asyncio.sleep(ft.value))
        logger.info("Now Ready For Deploying!")
        main()
