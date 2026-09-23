import logging
import datetime
import time
from pyrogram import Client, filters, StopPropagation, enums
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, ChatJoinRequest, ChatMemberUpdated
from pyrogram.errors import UserNotParticipant
from config import Config
from helper.database import digital_botz

logger = logging.getLogger(__name__)

# Statuses that mean the user really is in the channel. BANNED is answered by
# get_chat_member() instead of raising, so membership must never be inferred from
# "no exception" alone.
JOINED_STATUSES = (
    enums.ChatMemberStatus.MEMBER,
    enums.ChatMemberStatus.ADMINISTRATOR,
    enums.ChatMemberStatus.OWNER,
)

# One invite link per channel, reused until it expires. Minting a link for every
# blocked message burns Telegram's per-chat invite limit and ends in FloodWait.
_invite_cache = {}

# A still-blocked user is prompted at most once per this many seconds and keeps the
# prompt they already have, so repeat messages cannot be turned into message spam.
PROMPT_COOLDOWN = 15

class TechifyBots:
    def __init__(self):
        # Same client as the main Database instance, not a second pool.
        self.join_requests = digital_botz.db["join_requests"]
        self.fsub_cache = digital_botz.db["fsub_cache"]

    # Audit trail only. Access is decided by re-checking Telegram, never by this record:
    # a pending join request is not yet a membership and an approval can be revoked.
    async def add_join_req(self, user_id: int, channel_id: int):
        await self.join_requests.update_one(
            {"user_id": user_id},
            {"$addToSet": {"channels": channel_id}, "$set": {"created_at": datetime.datetime.now(datetime.timezone.utc)}},
            upsert=True
        )

    async def del_join_req(self):
        await self.join_requests.drop()
        await self.fsub_cache.drop()

    async def save_fsub_msg(self, user_id: int, message_id: int):
        await self.fsub_cache.update_one(
            {"user_id": user_id},
            {"$set": {"message_id": message_id, "created_at": datetime.datetime.now(datetime.timezone.utc)}},
            upsert=True
        )

    async def get_fsub_msg(self, user_id: int):
        return await self.fsub_cache.find_one({"user_id": user_id})

    async def delete_fsub_msg_db(self, user_id: int):
        await self.fsub_cache.delete_one({"user_id": user_id})

tb = TechifyBots()

async def _clear_prompt(bot: Client, user_id: int, doc: dict):
    msg_id = doc.get("message_id")
    if msg_id:
        try:
            await bot.delete_messages(user_id, msg_id)
        except Exception as e:
            logger.warning("FSUB: could not delete prompt %s for %s: %s", msg_id, user_id, e)
    await tb.delete_fsub_msg_db(user_id)

async def _is_member(bot: Client, user_id: int, channel_id: int):
    """True/False when Telegram answered, None when it could not be asked."""
    try:
        member = await bot.get_chat_member(channel_id, user_id)
    except UserNotParticipant:
        return False
    except Exception as e:
        logger.error("FSUB: cannot verify user %s in channel %s: %s", user_id, channel_id, e)
        return None

    if member.status in JOINED_STATUSES:
        return True
    # A restricted (muted) user is still in the channel, a banned one is not.
    return member.status == enums.ChatMemberStatus.RESTRICTED and bool(member.is_member)

async def check_all_channels_joined(bot: Client, user_id: int) -> bool:
    for channel_id in (*Config.AUTH_CHANNELS, *Config.AUTH_REQ_CHANNELS):
        if await _is_member(bot, user_id, channel_id) is not True:
            return False
    return True

async def auto_delete_fsub_and_start(client: Client, user_id: int):
    if not await check_all_channels_joined(client, user_id):
        return
    doc = await tb.get_fsub_msg(user_id)
    if doc:
        await _clear_prompt(client, user_id, doc)
    user = await client.get_users(user_id)
    bot_username = getattr(client, "username", "")  # cached by set_identity() in bot.start()
    try:
        await client.send_message(
            user_id,
            f"<b>{user.mention},\n\nʏᴏᴜ ʜᴀᴠᴇ ᴊᴏɪɴᴇᴅ ᴀʟʟ ʀᴇǫᴜɪʀᴇᴅ ᴄʜᴀɴɴᴇʟs.\n\nᴄʟɪᴄᴋ ᴛʜᴇ ʙᴜᴛᴛᴏɴ ʙᴇʟᴏᴡ ᴛᴏ ᴄᴏɴᴛɪɴᴜᴇ</b>",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("▶️ 𝖲𝗍𝖺𝗋𝗍", url=f"https://telegram.me/{bot_username}?start=start")]]
            )
        )
    except Exception:
        logger.exception("FSUB: could not send start link to %s", user_id)

def is_auth_req_channel(_, __, update):
    return update.chat.id in Config.AUTH_REQ_CHANNELS

@Client.on_chat_join_request(filters.create(is_auth_req_channel))
async def join_reqs(client: Client, message: ChatJoinRequest):
    user_id = message.from_user.id
    try:
        await tb.add_join_req(user_id, message.chat.id)
    except Exception:
        # Recording is for the audit trail; access is re-verified against Telegram
        # on every message, so a failed write must not break the user's flow.
        logger.exception("FSUB: could not record join request for %s", user_id)
    await auto_delete_fsub_and_start(client, user_id)

@Client.on_chat_member_updated(filters.chat(Config.AUTH_CHANNELS))
async def check_normal_join(client: Client, message: ChatMemberUpdated):
    if message.from_user and message.new_chat_member and message.new_chat_member.status in [
        enums.ChatMemberStatus.MEMBER,
        enums.ChatMemberStatus.ADMINISTRATOR,
        enums.ChatMemberStatus.OWNER
    ]:
        await auto_delete_fsub_and_start(client, message.from_user.id)

@Client.on_message(filters.command("delreq") & filters.private & filters.user(Config.ADMIN))
async def del_requests(client: Client, message: Message):
    try:
        await tb.del_join_req()
    except Exception:
        logger.exception("FSUB: could not clear join request cache")
        return await message.reply("<b>⚠️ Could not clear the cache, check logs.</b>")
    await message.reply("<b>⚙ Cleared join request records and pending membership prompts.</b>")

async def _invite_link(bot: Client, channel_id: int, join_request: bool) -> str:
    key = (channel_id, join_request)
    now = time.time()
    cached = _invite_cache.get(key)

    if cached and cached[1] > now:
        return cached[0]

    if Config.FSUB_EXPIRE > 0:
        expire_date = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=Config.FSUB_EXPIRE)
        expires_at = now + Config.FSUB_EXPIRE * 60 - 30
    else:
        expire_date = None
        expires_at = float("inf")  # permanent link, cacheable for the process lifetime

    invite = await bot.create_chat_invite_link(channel_id, expire_date=expire_date, creates_join_request=join_request)
    _invite_cache[key] = (invite.invite_link, expires_at)
    return invite.invite_link


async def _pending_joins(bot: Client, user_id: int):
    """Return (joinable, unverifiable); joinable holds (title, link) for real non-members."""
    channels = [(cid, False) for cid in Config.AUTH_CHANNELS]
    channels += [(cid, True) for cid in Config.AUTH_REQ_CHANNELS]

    joinable, unverifiable = [], []

    for channel_id, join_request in channels:
        member = await _is_member(bot, user_id, channel_id)

        if member is True:
            continue

        if member is None:
            unverifiable.append(channel_id)
            continue

        try:
            chat = await bot.get_chat(channel_id)
            link = await _invite_link(bot, channel_id, join_request)
            joinable.append((chat.title, link))
        except Exception as e:
            logger.error("FSUB: cannot build invite link for channel %s: %s", channel_id, e)
            unverifiable.append(channel_id)

    return joinable, unverifiable


def _age_seconds(created_at) -> float:
    if not isinstance(created_at, datetime.datetime):
        return float("inf")
    if created_at.tzinfo is None:
        created_at = created_at.replace(tzinfo=datetime.timezone.utc)
    return (datetime.datetime.now(datetime.timezone.utc) - created_at).total_seconds()


async def get_fsub(bot: Client, message: Message) -> bool:
    """True when the user may proceed. Every failure path denies access."""
    try:
        user_id = message.from_user.id

        if user_id == Config.ADMIN:
            return True

        prompt = await tb.get_fsub_msg(user_id)
        joinable, unverifiable = await _pending_joins(bot, user_id)

        if not joinable and not unverifiable:
            if prompt:
                await _clear_prompt(bot, user_id, prompt)
            return True

        if prompt:
            if _age_seconds(prompt.get("created_at")) < PROMPT_COOLDOWN:
                return False  # the prompt already sent still stands
            await _clear_prompt(bot, user_id, prompt)

        if not joinable:
            msg = await message.reply(
                "<blockquote><b>⚠️ 𝖬𝖾𝗆𝖻𝖾𝗋𝗌𝗁𝗂𝗉 𝖢𝗁𝖾𝖼𝗄 𝖥𝖺𝗂𝗅𝖾𝖽</b></blockquote>\n\n"
                f"{message.from_user.mention}, 𝗒𝗈𝗎𝗋 𝖺𝖼𝖼𝖾𝗌𝗌 𝖼𝗈𝗎𝗅𝖽 𝗇𝗈𝗍 𝖻𝖾 𝗏𝖾𝗋𝗂𝖿𝗂𝖾𝖽 𝗋𝗂𝗀𝗁𝗍 𝗇𝗈𝗐.\n"
                "𝖯𝗅𝖾𝖺𝗌𝖾 𝗍𝗋𝗒 𝖺𝗀𝖺𝗂𝗇 𝗂𝗇 𝖺 𝗆𝗈𝗆𝖾𝗇𝗍."
            )
            await tb.save_fsub_msg(user_id, msg.id)
            return False

        bot_username = getattr(bot, "username", "")  # cached by set_identity()
        buttons = []

        for i in range(0, len(joinable), 2):
            row = []
            for j in range(2):
                if i + j < len(joinable):
                    title, link = joinable[i + j]
                    row.append(InlineKeyboardButton(f"{i + j + 1}. {title}", url=link))
            buttons.append(row)

        buttons.append(
            [InlineKeyboardButton("🔄 𝖳𝗋𝗒 𝖠𝗀𝖺𝗂𝗇", url=f"https://telegram.me/{bot_username}?start=start")]
        )

        text = (
            "<blockquote><b>🔒 𝖠𝖼𝖼𝖾𝗌𝗌 𝖱𝖾𝗌𝗍𝗋𝗂𝖼𝗍𝖾𝖽!</b></blockquote>\n\n"
            f"{message.from_user.mention}, 𝖳𝗈 𝖴𝗌𝖾 𝖳𝗁𝗂𝗌 𝖡𝗈𝗍, 𝖸𝗈𝗎 𝖭𝖾𝖾𝖽 𝖳𝗈 𝖩𝗈𝗂𝗇 𝖠𝖫𝖫 𝖱𝖾𝗊𝗎𝗂𝗋𝖾𝖽 𝖢𝗁𝖺𝗇𝗇𝖾𝗅𝗌.\n\n"
            f"𝖱𝖾𝗊𝗎𝗂𝗋𝖾𝖽 𝖢𝗁𝖺𝗇𝗇𝖾𝗅𝗌 ({len(joinable)})\n\n"
            "𝖠𝖿𝗍𝖾𝗋 𝖩𝗈𝗂𝗇𝗂𝗇𝗀, 𝖢𝗅𝗂𝖼𝗄 <b>“𝖳𝗋𝗒 𝖠𝗀𝖺𝗂𝗇”</b> 𝖡𝖾𝗅𝗈𝗐."
        )
        if unverifiable:
            text += "\n\n⚠️ 𝖲𝗈𝗆𝖾 𝖼𝗁𝖺𝗇𝗇𝖾𝗅𝗌 𝖼𝗈𝗎𝗅𝖽 𝗇𝗈𝗍 𝖻𝖾 𝖼𝗁𝖾𝖼𝗄𝖾𝖽 𝗒𝖾𝗍."

        msg = await message.reply(text, reply_markup=InlineKeyboardMarkup(buttons))
        await tb.save_fsub_msg(user_id, msg.id)
        return False
    except Exception:
        # getattr: from_user itself may be None, and naming user_id here would then
        # raise UnboundLocalError, which is what lets the update reach the handlers.
        logger.exception("FSUB: gate failed for %s, denying access", getattr(message.from_user, "id", None))
        return False


@Client.on_message(filters.private & ~filters.user(Config.ADMIN) & ~filters.bot & ~filters.service & ~filters.me, group=-10)
async def global_fsub_checker(client: Client, message: Message):
    if not Config.IS_FSUB:
        return
    if not await get_fsub(client, message):
        raise StopPropagation
