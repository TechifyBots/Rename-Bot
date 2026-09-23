import os, time
from dotenv import load_dotenv

load_dotenv()


def _int_env(name, default=0):
    try:
        return int(os.environ.get(name, "") or default)
    except (TypeError, ValueError):
        return default


class Config(object):

    API_ID = os.environ.get("API_ID", "")
    API_HASH = os.environ.get("API_HASH", "")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

    # premium account string session required 😢 
    STRING_SESSION = os.environ.get("STRING_SESSION", "")
    
    # database config
    DB_NAME = os.environ.get("DB_NAME", "Rename_Bot")     
    DB_URL = os.environ.get("DB_URL", "")

    # logging - canonical log path for setup and the /logs command
    LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "BotLog.txt")
 
    # other configs
    PIC = os.environ.get("PIC", "https://i.ibb.co/YTk9gzhY/IMG-20250906-144306-804.jpg")
    ADMIN = _int_env("ADMIN", 0)
    LOG_CHANNEL = _int_env("LOG_CHANNEL", 0)
    BIN_CHANNEL = _int_env("BIN_CHANNEL", 0)

    # free upload limit 
    FREE_UPLOAD_LIMIT = 6442450944 # calculation 6*1024*1024*1024=results

    # premium mode feature ✅
    UPLOAD_LIMIT_MODE = True 
    PREMIUM_MODE = True 
    
    #force subs
    IS_FSUB = os.environ.get("IS_FSUB", "False").lower() == "true"  # Set "True" For Enable Force Subscribe
    AUTH_CHANNELS = list(map(int, os.environ.get("AUTH_CHANNELS", "").split())) # Add Multiple channel ids
    AUTH_REQ_CHANNELS = list(map(int, os.environ.get("AUTH_REQ_CHANNELS", "").split())) # Add Multiple channel ids
    FSUB_EXPIRE = int(os.environ.get("FSUB_EXPIRE", 2))  # minutes, 0 = no expiry
        
    # wes response configuration     
    PORT = int(os.environ.get("PORT", "8080"))
    BOT_UPTIME = time.time()

class rkn(object):
    # part of text configuration
    START_TXT = """<b>{},</b>

𝖨 𝖠𝗆 𝖱𝖾𝗇𝖺𝗆𝖾 𝖡𝗈𝗍 — 𝖠 𝖲𝗆𝖺𝗋𝗍 𝖠𝗇𝖽 𝖯𝗈𝗐𝖾𝗋𝖿𝗎𝗅 𝖳𝗈𝗈𝗅 𝖡𝗎𝗂𝗅𝗍 𝖳𝗈 𝖬𝖺𝗄𝖾 𝖥𝗂𝗅𝖾 𝖬𝖺𝗇𝖺𝗀𝖾𝗆𝖾𝗇𝗍 𝖲𝗂𝗆𝗉𝗅𝖾.

𝖱𝖾𝗇𝖺𝗆𝖾 𝖸𝗈𝗎𝗋 𝖥𝗂𝗅𝖾𝗌, 𝖢𝗁𝖺𝗇𝗀𝖾 𝖳𝗁𝗎𝗆𝖻𝗇𝖺𝗂𝗅𝗌, 𝖢𝗎𝗌𝗍𝗈𝗆𝗂𝗓𝖾 𝖢𝖺𝗉𝗍𝗂𝗈𝗇𝗌, 𝖠𝗇𝖽 𝖢𝗈𝗇𝗏𝖾𝗋𝗍 𝖵𝗂𝖽𝖾𝗈𝗌 𝖳𝗈 𝖥𝗂𝗅𝖾𝗌 𝖮𝗋 𝖥𝗂𝗅𝖾𝗌 𝖳𝗈 𝖵𝗂𝖽𝖾𝗈𝗌.

𝖳𝖺𝗉 𝖧𝖾𝗅𝗉 𝖳𝗈 𝖤𝗑𝗉𝗅𝗈𝗋𝖾 𝖠𝗅𝗅 𝖥𝖾𝖺𝗍𝗎𝗋𝖾𝗌

<blockquote><b>‣ 𝖬𝖺𝗂𝗇𝗍𝖺𝗂𝗇𝖾𝖽 𝖡𝗒: <a href='https://techifybots.vercel.app'>𝖳𝖾𝖼𝗁𝗂𝖿𝗒 𝖡𝗈𝗍𝗌</a></b></blockquote>"""

    ABOUT_TXT = """<b>╭───────────⍟
├ 🤖 𝖭𝖺𝗆𝖾 : {}
├ 🖥️ 𝖣𝖾𝗏𝖾𝗅𝗈𝗉𝖾𝗋𝗌 : {}
├ 👨‍💻 𝖯𝗋𝗈𝗀𝗋𝖺𝗆𝗆𝖾𝗋 : {}
├ 📕 𝖫𝗂𝖻𝗋𝖺𝗋𝗒 : {}
├ ✏️ 𝖫𝖺𝗇𝗀𝗎𝖺𝗀𝖾 : {}
├ 💾 𝖣𝖺𝗍𝖺𝖻𝖺𝗌𝖾 : {}
├ 📊 𝖵𝖾𝗋𝗌𝗂𝗈𝗇 : <a href=https://github.com/TechifyBots/Rename-Bot>{}</a>
╰───────────────⍟</b>"""

    HELP_TXT = """✏️ <b><u>𝖧𝗈𝗐 𝖳𝗈 𝖱𝖾𝗇𝖺𝗆𝖾 𝖠 𝖥𝗂𝗅𝖾</u></b>

<b>•></b> 𝖲𝖾𝗇𝖽 𝖠𝗇𝗒 𝖥𝗂𝗅𝖾 𝖠𝗇𝖽 𝖤𝗇𝗍𝖾𝗋 𝖳𝗁𝖾 𝖭𝖾𝗐 𝖥𝗂𝗅𝖾 𝖭𝖺𝗆𝖾.
𝖳𝗁𝖾𝗇 𝖲𝖾𝗅𝖾𝖼𝗍 𝖳𝗁𝖾 𝖱𝖾𝗊𝗎𝗂𝗋𝖾𝖽 𝖥𝗈𝗋𝗆𝖺𝗍 [ 𝖣𝗈𝖼𝗎𝗆𝖾𝗇𝗍, 𝖵𝗂𝖽𝖾𝗈, 𝖠𝗎𝖽𝗂𝗈 ].

ℹ️ 𝖥𝗈𝗋 𝖠𝗇𝗒 𝖮𝗍𝗁𝖾𝗋 𝖧𝖾𝗅𝗉, 𝖢𝗈𝗇𝗍𝖺𝖼𝗍 𝖮𝗎𝗋 <a href=https://t.me/TechifySupport>𝖲𝖴𝖯𝖯𝖮𝖱𝖳 𝖦𝖱𝖮𝖴𝖯</a>"""

    UPGRADE_PREMIUM = """
•⪼ ★ 𝖯𝗅𝖺𝗇𝗌    -  ⏳ 𝖣𝗎𝗋𝖺𝗍𝗂𝗈𝗇 - 💸 𝖯𝗋𝗂𝖼𝖾

•⪼ 🥉 𝖡𝗋𝗈𝗇𝗓𝖾    -  3 𝖣𝖺𝗒𝗌  -  ₹39
•⪼ 🥈 𝖲𝗂𝗅𝗏𝖾𝗋     -  7 𝖣𝖺𝗒𝗌  -  ₹59
•⪼ 🥇 𝖦𝗈𝗅𝖽      -  15 𝖣𝖺𝗒𝗌 -  ₹99
•⪼ 🏆 𝖯𝗅𝖺𝗍𝗂𝗇𝗎𝗆 -  1 𝖬𝗈𝗇𝗍𝗁 - ₹179
•⪼ 💎 𝖣𝗂𝖺𝗆𝗈𝗇𝖽  -  2 𝖬𝗈𝗇𝗍𝗁𝗌 - ₹339

- 𝖣𝖺𝗂𝗅𝗒 𝖴𝗉𝗅𝗈𝖺𝖽 𝖫𝗂𝗆𝗂𝗍: 𝖴𝗇𝗅𝗂𝗆𝗂𝗍𝖾𝖽
- 𝖣𝗂𝗌𝖼𝗈𝗎𝗇𝗍 𝖮𝗇 𝖠𝗅𝗅 𝖯𝗅𝖺𝗇𝗌: ₹9"""
    
    UPGRADE_PLAN = """
★ 𝖯𝗅𝖺𝗇 : 𝖯𝗋𝗈
⏳ 𝖣𝗎𝗋𝖺𝗍𝗂𝗈𝗇 : 1 𝖬𝗈𝗇𝗍𝗁
💸 𝖯𝗋𝗂𝖼𝖾 : ₹179
💾 𝖫𝗂𝗆𝗂𝗍 : 100 𝖦𝖡

★ 𝖯𝗅𝖺𝗇 : 𝖴𝗅𝗍𝗋𝖺 𝖯𝗋𝗈
⏳ 𝖣𝗎𝗋𝖺𝗍𝗂𝗈𝗇 : 1 𝖬𝗈𝗇𝗍𝗁
💸 𝖯𝗋𝗂𝖼𝖾 : ₹199
💾 𝖫𝗂𝗆𝗂𝗍 : 1000 𝖦𝖡

- 𝖣𝗂𝗌𝖼𝗈𝗎𝗇𝗍 𝖮𝗇 𝖠𝗅𝗅 𝖯𝗅𝖺𝗇𝗌 : ₹9"""
    
    THUMBNAIL = """🌌 <b><u>𝖧𝗈𝗐 𝖳𝗈 𝖲𝖾𝗍 𝖳𝗁𝗎𝗆𝖻𝗇𝖺𝗂𝗅</u></b>

<b>•></b> 𝖲𝖾𝗇𝖽 𝖠𝗇𝗒 𝖯𝗁𝗈𝗍𝗈 𝖳𝗈 𝖠𝗎𝗍𝗈𝗆𝖺𝗍𝗂𝖼𝖺𝗅𝗅𝗒 𝖲𝖾𝗍 𝖨𝗍 𝖠𝗌 𝖸𝗈𝗎𝗋 𝖥𝗂𝗅𝖾 𝖳𝗁𝗎𝗆𝖻𝗇𝖺𝗂𝗅.

<b>•></b> /delthumb - 𝖴𝗌𝖾 𝖳𝗁𝗂𝗌 𝖢𝗈𝗆𝗆𝖺𝗇𝖽 𝖳𝗈 𝖣𝖾𝗅𝖾𝗍𝖾 𝖸𝗈𝗎𝗋 𝖮𝗅𝖽 𝖳𝗁𝗎𝗆𝖻𝗇𝖺𝗂𝗅.

<b>•></b> /viewthumb - 𝖴𝗌𝖾 𝖳𝗁𝗂𝗌 𝖢𝗈𝗆𝗆𝖺𝗇𝖽 𝖳𝗈 𝖵𝗂𝖾𝗐 𝖸𝗈𝗎𝗋 𝖢𝗎𝗋𝗋𝖾𝗇𝗍 𝖳𝗁𝗎𝗆𝖻𝗇𝖺𝗂𝗅."""

    CAPTION = """📑 <b><u>𝖧𝗈𝗐 𝖳𝗈 𝖲𝖾𝗍 𝖢𝗎𝗌𝗍𝗈𝗆 𝖢𝖺𝗉𝗍𝗂𝗈𝗇</u></b>

<b>•></b> /setcaption - 𝖴𝗌𝖾 𝖳𝗁𝗂𝗌 𝖢𝗈𝗆𝗆𝖺𝗇𝖽 𝖳𝗈 𝖲𝖾𝗍 𝖠 𝖢𝗎𝗌𝗍𝗈𝗆 𝖢𝖺𝗉𝗍𝗂𝗈𝗇.

<b>•></b> /seecaption - 𝖴𝗌𝖾 𝖳𝗁𝗂𝗌 𝖢𝗈𝗆𝗆𝖺𝗇𝖽 𝖳𝗈 𝖵𝗂𝖾𝗐 𝖸𝗈𝗎𝗋 𝖢𝗎𝗌𝗍𝗈𝗆 𝖢𝖺𝗉𝗍𝗂𝗈𝗇.

<b>•></b> /delcaption - 𝖴𝗌𝖾 𝖳𝗁𝗂𝗌 𝖢𝗈𝗆𝗆𝖺𝗇𝖽 𝖳𝗈 𝖣𝖾𝗅𝖾𝗍𝖾 𝖸𝗈𝗎𝗋 𝖢𝗎𝗌𝗍𝗈𝗆 𝖢𝖺𝗉𝗍𝗂𝗈𝗇.

𝖤𝗑𝖺𝗆𝗉𝗅𝖾:
<code>/setcaption 📕 𝖥𝗂𝗅𝖾 𝖭𝖺𝗆𝖾: {filename}
💾 𝖲𝗂𝗓𝖾: {filesize}
⏰ 𝖣𝗎𝗋𝖺𝗍𝗂𝗈𝗇: {duration}</code>"""

    BOT_STATUS = """⚡️ <b>𝖡𝗈𝗍 𝖲𝗍𝖺𝗍𝗎𝗌</b> ⚡️

⌚️ 𝖡𝗈𝗍 𝖴𝗉𝗍𝗂𝗆𝖾: {}
👥 𝖳𝗈𝗍𝖺𝗅 𝖴𝗌𝖾𝗋𝗌: {}
💸 𝖳𝗈𝗍𝖺𝗅 𝖯𝗋𝖾𝗆𝗂𝗎𝗆 𝖴𝗌𝖾𝗋𝗌: {}
🌐 𝖭𝖾𝗍𝗐𝗈𝗋𝗄: {}
֍ 𝖴𝗉𝗅𝗈𝖺𝖽: {}
⊙ 𝖣𝗈𝗐𝗇𝗅𝗈𝖺𝖽: {}"""

    LIVE_STATUS = """⚡ 𝖫𝗂𝗏𝖾 𝖲𝖾𝗋𝗏𝖾𝗋 𝖲𝗍𝖺𝗍𝗎𝗌 ⚡

⏱️ 𝖴𝗉𝗍𝗂𝗆𝖾: "{}"
🖥️ 𝖢𝖯𝖴: "{}%"
🧠 𝖱𝖠𝖬: "{}%"
💽 𝖳𝗈𝗍𝖺𝗅 𝖣𝗂𝗌𝗄: "{}"
📦 𝖴𝗌𝖾𝖽 𝖲𝗉𝖺𝖼𝖾: "{} {}%"
💾 𝖥𝗋𝖾𝖾 𝖲𝗉𝖺𝖼𝖾: "{}"
⬆️ 𝖴𝗉𝗅𝗈𝖺𝖽: "{}"
⬇️ 𝖣𝗈𝗐𝗇𝗅𝗈𝖺𝖽: "{}"
🌐 𝖭𝖾𝗍𝗐𝗈𝗋𝗄: "{}"

‣ 𝖵𝟥.𝟢.𝟢 [𝖲𝖳𝖠𝖡𝖫𝖤]"""

    SEND_METADATA = """<b>📝 𝖲𝖾𝗇𝖽 𝖸𝗈𝗎𝗋 𝖢𝗎𝗌𝗍𝗈𝗆 𝖬𝖾𝗍𝖺𝖽𝖺𝗍𝖺 𝖢𝗈𝖽𝖾</b>

<code>--change-title @TechifyBots
--change-video-title @TechifyBots
--change-audio-title @TechifyBots
--change-subtitle-title @TechifyBots
--change-author @TechifyBots</code>

𝖱𝖾𝗉𝗅𝗒 𝗍𝗈 𝗍𝗁𝗂𝗌 𝗆𝖾𝗌𝗌𝖺𝗀𝖾 𝗐𝗂𝗍𝗁 𝗒𝗈𝗎𝗋 𝖼𝗈𝖽𝖾 (𝗍𝖾𝗑𝗍 𝗈𝗇𝗅𝗒)."""
    
    CUSTOM_FILE_NAME = """<u>🖋️ 𝖢𝗎𝗌𝗍𝗈𝗆 𝖥𝗂𝗅𝖾 𝖭𝖺𝗆𝖾</u>

𝖸𝗈𝗎 𝖢𝖺𝗇 𝖯𝗋𝖾-𝖠𝖽𝖽 𝖠 𝖯𝗋𝖾𝖿𝗂𝗑 𝖮𝗋 𝖲𝗎𝖿𝖿𝗂𝗑 𝖠𝗅𝗈𝗇𝗀 𝖶𝗂𝗍𝗁 𝖸𝗈𝗎𝗋 𝖭𝖾𝗐 𝖥𝗂𝗅𝖾 𝖭𝖺𝗆𝖾.

➢ /setprefix - 𝖴𝗌𝖾 𝖳𝗁𝗂𝗌 𝖢𝗈𝗆𝗆𝖺𝗇𝖽 𝖳𝗈 𝖠𝖽𝖽 𝖠 𝖯𝗋𝖾𝖿𝗂𝗑 𝖳𝗈 𝖸𝗈𝗎𝗋 𝖥𝗂𝗅𝖾𝗇𝖺𝗆𝖾.
➢ /seeprefix - 𝖴𝗌𝖾 𝖳𝗁𝗂𝗌 𝖢𝗈𝗆𝗆𝖺𝗇𝖽 𝖳𝗈 𝖵𝗂𝖾𝗐 𝖸𝗈𝗎𝗋 𝖯𝗋𝖾𝖿𝗂𝗑.
➢ /delprefix - 𝖴𝗌𝖾 𝖳𝗁𝗂𝗌 𝖢𝗈𝗆𝗆𝖺𝗇𝖽 𝖳𝗈 𝖣𝖾𝗅𝖾𝗍𝖾 𝖸𝗈𝗎𝗋 𝖯𝗋𝖾𝖿𝗂𝗑.
➢ /setsuffix - 𝖴𝗌𝖾 𝖳𝗁𝗂𝗌 𝖢𝗈𝗆𝗆𝖺𝗇𝖽 𝖳𝗈 𝖠𝖽𝖽 𝖠 𝖲𝗎𝖿𝖿𝗂𝗑 𝖳𝗈 𝖸𝗈𝗎𝗋 𝖥𝗂𝗅𝖾𝗇𝖺𝗆𝖾.
➢ /seesuffix - 𝖴𝗌𝖾 𝖳𝗁𝗂𝗌 𝖢𝗈𝗆𝗆𝖺𝗇𝖽 𝖳𝗈 𝖵𝗂𝖾𝗐 𝖸𝗈𝗎𝗋 𝖲𝗎𝖿𝖿𝗂𝗑.
➢ /delsuffix - 𝖴𝗌𝖾 𝖳𝗁𝗂𝗌 𝖢𝗈𝗆𝗆𝖺𝗇𝖽 𝖳𝗈 𝖣𝖾𝗅𝖾𝗍𝖾 𝖸𝗈𝗎𝗋 𝖲𝗎𝖿𝖿𝗂𝗑.

𝖤𝗑𝖺𝗆𝗉𝗅𝖾: <code>/setsuffix @TechifyBots</code>
𝖤𝗑𝖺𝗆𝗉𝗅𝖾: <code>/setprefix @TechifyBots</code>"""

    DEV_TXT = """<b><u>𝖲𝗉𝖾𝖼𝗂𝖺𝗅 𝖳𝗁𝖺𝗇𝗄𝗌 & 𝖣𝖾𝗏𝖾𝗅𝗈𝗉𝖾𝗋𝗌</u></b>

» 𝖲𝗈𝗎𝗋𝖼𝖾 𝖢𝗈𝖽𝖾 : <a href=https://github.com/TechifyBots/Rename-Bot>𝖱𝖾𝗇𝖺𝗆𝖾-𝖡𝗈𝗍</a>

• ❣️ <a href=https://github.com/RknDeveloper>𝖱𝗄𝗇𝖣𝖾𝗏𝖾𝗅𝗈𝗉𝖾𝗋</a>
• ❣️ <a href=https://github.com/DigitalBotz>𝖣𝗂𝗀𝗂𝗍𝖺𝗅𝖡𝗈𝗍𝗓</a>
• ❣️ <a href=https://github.com/TechifyBots>𝖳𝖾𝖼𝗁𝗂𝖿𝗒𝖡𝗈𝗍𝗌</a>"""
    
    PROGRESS = """<b>
╭━━━━━━━━◉🚀◉━━━━━━━━╮
┃   𝗣𝗥𝗢𝗖𝗘𝗦𝗦𝗜𝗡𝗚...❱━➣  
┣━━━━━━━━━━━━━━━━━━━━╯
┣⪼ 📦 𝗦𝗜𝗭𝗘: {1} | {2}
┣⪼ 📊 𝗗𝗢𝗡𝗘: {0}%
┣⪼ 🚀 𝗦𝗣𝗘𝗘𝗗: {3}/s
┣⪼ ⏰ 𝗘𝗧𝗔: {4}
╰━━━━━━━━◉🔥◉━━━━━━━━╯</b>"""
