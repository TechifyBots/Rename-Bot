from pyrogram import Client, filters
from pyrogram.enums import MessageMediaType, ParseMode
from pyrogram.errors import FloodWait
from pyrogram.file_id import FileId
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply, ReplyParameters
from PIL import Image
from helper.utils import progress_for_pyrogram, convert, humanbytes, add_prefix_suffix, remove_path
from helper.database import digital_botz
from helper.ffmpeg import change_metadata, get_duration
from config import Config, rkn
import os, time, asyncio
from html import escape
import logging

UPLOAD_TEXT = """Uploading Started...."""
DOWNLOAD_TEXT = """Download Started..."""

logger = logging.getLogger(__name__)

app = Client("4gb_FileRenameBot", api_id=Config.API_ID, api_hash=Config.API_HASH, session_string=Config.STRING_SESSION, parse_mode=ParseMode.HTML)

@Client.on_message(filters.private & (filters.audio | filters.document | filters.video))
async def rename_start(client, message):
    user_id  = message.from_user.id
    rkn_file = getattr(message, message.media.value)
    filename = rkn_file.file_name
    filesize = humanbytes(rkn_file.file_size)
    mime_type = rkn_file.mime_type
    dcid = FileId.decode(rkn_file.file_id).dc_id
    extension_type = mime_type.split('/')[0]

    media_info_text = (
        f"<b><i>ᴍᴇᴅɪᴀ ɪɴꜰᴏ:</i></b>\n\n"
        f"◈ ᴏʟᴅ ꜰɪʟᴇ ɴᴀᴍᴇ: <code>{escape(str(filename))}</code>\n\n"
        f"◈ ᴇxᴛᴇɴꜱɪᴏɴ: <code>{escape(extension_type.upper())}</code>\n"
        f"◈ ꜰɪʟᴇ ꜱɪᴢᴇ: <code>{filesize}</code>\n"
        f"◈ ᴍɪᴍᴇ ᴛʏᴩ: <code>{escape(str(mime_type))}</code>\n"
        f"◈ ᴅᴄ ɪᴅ: <code>{dcid}</code>\n\n"
        "ᴘʟᴇᴀsᴇ ᴇɴᴛᴇʀ ᴛʜᴇ ɴᴇᴡ ғɪʟᴇɴᴀᴍᴇ ᴡɪᴛʜ ᴇxᴛᴇɴsɪᴏɴ ᴀɴᴅ ʀᴇᴘʟʏ ᴛʜɪs ᴍᴇssᴀɢᴇ...."
    )

    if client.premium and client.uploadlimit:
        await digital_botz.reset_uploadlimit_access(user_id)
        user_data = await digital_botz.get_user_data(user_id)
        limit = user_data.get('uploadlimit', 0)
        used = user_data.get('used_limit', 0)
        remain = int(limit) - int(used)
        used_percentage = int(used) / int(limit) * 100
        if remain < int(rkn_file.file_size):
            return await message.reply_text(f"{used_percentage:.2f}% Of Daily Upload Limit {humanbytes(limit)}.\n\n Media Size: {filesize}\n Your Used Daily Limit {humanbytes(used)}\n\nYou have only <b>{humanbytes(remain)}</b> Data.\nPlease, Buy Premium Plan s.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🪪 Uᴘɢʀᴀᴅᴇ", callback_data="plans")]]))
         
    if await digital_botz.has_premium_access(user_id) and client.premium:
        if not Config.STRING_SESSION:
            if rkn_file.file_size > 2000 * 1024 * 1024:
                 return await message.reply_text("Sᴏʀʀy Bʀᴏ Tʜɪꜱ Bᴏᴛ Iꜱ Dᴏᴇꜱɴ'ᴛ Sᴜᴩᴩᴏʀᴛ Uᴩʟᴏᴀᴅɪɴɢ Fɪʟᴇꜱ Bɪɢɢᴇʀ Tʜᴀɴ 2Gʙ+")
        try:
            await message.reply_text(
                text=media_info_text,
                reply_markup=ForceReply(True)
            )       
            await asyncio.sleep(30)
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await message.reply_text(
                text=media_info_text,
                reply_markup=ForceReply(True)
            )
        except Exception as e:
            logger.exception("Error in rename_start: %s", e)
    else:
        if rkn_file.file_size > 2000 * 1024 * 1024 and client.premium:
            return await message.reply_text("If you want to rename 4GB+ files then you will have to buy premium. /plans")
        try:
            await message.reply_text(
                text=media_info_text,
                reply_markup=ForceReply(True)
            )       
            await asyncio.sleep(30)
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await message.reply_text(
                text=media_info_text,
                reply_markup=ForceReply(True)
            )
        except Exception as e:
            logger.exception("Error in rename_start (non-premium): %s", e)

@Client.on_message(filters.private & filters.reply)
async def refunc(client, message):
    reply_message = message.reply_to_message
    if (reply_message.reply_markup) and isinstance(reply_message.reply_markup, ForceReply):
        if rkn.SEND_METADATA.splitlines()[0] in (reply_message.text or ""):
            return  # handled by metadata.save_metadata_code
        new_name = message.text 
        await message.delete() 
        msg = await client.get_messages(message.chat.id, reply_message.id)
        file = msg.reply_to_message
        media = getattr(file, file.media.value)
        if not "." in new_name:
            if "." in media.file_name:
                extn = media.file_name.rsplit('.', 1)[-1]
            else:
                extn = "mkv"
            new_name = new_name + "." + extn
        await reply_message.delete()
        button = [[InlineKeyboardButton("📁 Dᴏᴄᴜᴍᴇɴᴛ",callback_data = "upload#document")]]
        if file.media in [MessageMediaType.VIDEO, MessageMediaType.DOCUMENT]:
            button.append([InlineKeyboardButton("🎥 Vɪᴅᴇᴏ", callback_data = "upload#video")])
        elif file.media == MessageMediaType.AUDIO:
            button.append([InlineKeyboardButton("🎵 Aᴜᴅɪᴏ", callback_data = "upload#audio")])
        await client.send_message(
            chat_id=message.chat.id,
            text=f"<b>Sᴇʟᴇᴄᴛ Tʜᴇ Oᴜᴛᴩᴜᴛ Fɪʟᴇ Tyᴩᴇ</b>\n<b>• Fɪʟᴇ Nᴀᴍᴇ :-</b><code>{escape(str(new_name))}</code>",
            reply_parameters=ReplyParameters(message_id=file.id),
            reply_markup=InlineKeyboardMarkup(button)
        )

async def upload_files(bot, sender_id, upload_type, file_path, ph_path, caption, duration, rkn_processing):
    """
    Unified function to upload files based on type
    - Supports both 2GB and 4GB files
    - Uses same function for all file sizes
    - Handles document, video, and audio files
    """
    try:
        # Check if file exists
        if not os.path.exists(file_path):
            return None, f"File not found: {file_path}"
        # Upload document files (2GB & 4GB)
        if upload_type == "document":
            filw = await bot.send_document(
                sender_id,
                document=file_path,
                thumb=ph_path,
                caption=caption,
                progress=progress_for_pyrogram,
                progress_args=(UPLOAD_TEXT, rkn_processing, time.time()))
        # Upload video files (2GB & 4GB)  
        elif upload_type == "video":
            filw = await bot.send_video(
                sender_id,
                video=file_path,
                caption=caption,
                thumb=ph_path,
                duration=duration,
                progress=progress_for_pyrogram,
                progress_args=(UPLOAD_TEXT, rkn_processing, time.time()))
        # Upload audio files (2GB & 4GB)
        elif upload_type == "audio":
            filw = await bot.send_audio(
                sender_id,
                audio=file_path,
                caption=caption,
                thumb=ph_path,
                duration=duration,
                progress=progress_for_pyrogram,
                progress_args=(UPLOAD_TEXT, rkn_processing, time.time()))
        else:
            return None, f"Unknown upload type: {upload_type}"
        # Return uploaded file object
        return filw, None
    except Exception as e:
        # Return error if upload fails
        return None, str(e)

#@Client.on_callback_query(filters.regex("upload"))
async def upload_doc(bot, update):
    rkn_processing = await update.message.edit("<code>Processing...</code>")
    # Creating Directory for Metadata
    if not os.path.isdir("Metadata"):
        os.mkdir("Metadata")
    user_id = int(update.message.chat.id) 
    new_name = update.message.text
    new_filename_ = new_name.split(":-")[1]
    user_data = await digital_botz.get_user_data(user_id)
    try:
        # adding prefix and suffix
        prefix = user_data.get('prefix', None)
        suffix = user_data.get('suffix', None)
        new_filename = await add_prefix_suffix(new_filename_, prefix, suffix)
    except Exception as e:
        return await rkn_processing.edit(f"⚠️ Something went wrong can't able to set Prefix or Suffix ☹️ \n\n❄️ Contact My Creator -> @TechifyBots\nError: {escape(str(e))}")
    # msg file location 
    file = update.message.reply_to_message
    media = getattr(file, file.media.value)
    # File paths for download and metadata
    file_path = f"Renames/{new_filename}"
    metadata_path = f"Metadata/{new_filename}"
    await rkn_processing.edit("<code>Try To Download....</code>")
    if bot.premium and bot.uploadlimit:
        used = user_data.get('used_limit', 0)        
        total_used = int(used) + int(media.file_size)
        await digital_botz.set_used_limit(user_id, total_used)
    try:            
        dl_path = await bot.download_media(message=file, file_name=file_path, progress=progress_for_pyrogram, progress_args=(DOWNLOAD_TEXT, rkn_processing, time.time()))                    
    except Exception as e:
        if bot.premium and bot.uploadlimit:
            used_remove = int(used) - int(media.file_size)
            await digital_botz.set_used_limit(user_id, used_remove)
        return await rkn_processing.edit(f"Download Error: {escape(str(e))}")

    metadata_mode = await digital_botz.get_metadata_mode(user_id)
    if metadata_mode:        
        metadata = await digital_botz.get_metadata_code(user_id)
        if metadata:
            await rkn_processing.edit("I Fᴏᴜɴᴅ Yᴏᴜʀ Mᴇᴛᴀᴅᴀᴛᴀ\n\n<b><i>Pʟᴇᴀsᴇ Wᴀɪᴛ...</i></b>\n<b>Aᴅᴅɪɴɢ Mᴇᴛᴀᴅᴀᴛᴀ Tᴏ Fɪʟᴇ....</b>")            
            if await change_metadata(dl_path, metadata_path, metadata):            
                await rkn_processing.edit("Metadata Added.....")
                logger.info("Metadata added")
            else:
                await rkn_processing.edit("Failed to add metadata, uploading original file...")
                metadata_mode = False
        else:
            await rkn_processing.edit("No metadata found, uploading original file...")
            metadata_mode = False
    else:
        await rkn_processing.edit("<code>Try To Uploading....</code>")
    duration = await get_duration(file_path if os.path.exists(file_path) else dl_path)
    ph_path = None
    c_caption = user_data.get('caption', None)
    c_thumb = user_data.get('file_id', None)
    if c_caption:
         try:
             # adding custom caption 
             caption = c_caption.format(filename=escape(str(new_filename)), filesize=escape(humanbytes(media.file_size)), duration=escape(str(convert(duration))))
         except Exception as e:
             if bot.premium and bot.uploadlimit:
                 used_remove = int(used) - int(media.file_size)
                 await digital_botz.set_used_limit(user_id, used_remove)
             return await rkn_processing.edit(text=f"Yᴏᴜʀ Cᴀᴩᴛɪᴏɴ Eʀʀᴏʀ Exᴄᴇᴩᴛ Kᴇyᴡᴏʀᴅ Aʀɢᴜᴍᴇɴᴛ ●> ({escape(str(e))})")             
    else:
         caption = f"<b>{escape(str(new_filename))}</b>\n\n<b>User:</b> {escape(str(update.from_user.first_name))}\n<b>User ID:</b> <code>{user_id}</code>"
    if (media.thumbs or c_thumb):
         # downloading thumbnail path
         try:
             if c_thumb:
                 ph_path = await bot.download_media(c_thumb) 
             else:
                 ph_path = await bot.download_media(media.thumbs[0].file_id)
             
             if ph_path and os.path.exists(ph_path):
                 with Image.open(ph_path) as img:
                     img.convert("RGB").resize((320, 320), Image.Resampling.LANCZOS).save(ph_path, "JPEG")
         except Exception as e:
             logger.exception("Error processing thumbnail: %s", e)
             ph_path = None

    upload_type = update.data.split("#")[1]
    # Use the correct file path based on metadata mode
    final_file_path = metadata_path if metadata_mode and os.path.exists(metadata_path) else file_path
    if media.file_size > 2000 * 1024 * 1024:
        # Upload file using unified function for large files
        filw, error = await upload_files(
            app, Config.LOG_CHANNEL, upload_type, final_file_path, 
            ph_path, caption, duration, rkn_processing
        )
        if error:
            if bot.premium and bot.uploadlimit:
                used_remove = int(used) - int(media.file_size)
                await digital_botz.set_used_limit(user_id, used_remove)
            await remove_path(ph_path, file_path, dl_path, metadata_path)
            return await rkn_processing.edit(f"Upload Error: {escape(str(error))}")

        from_chat = filw.chat.id
        mg_id = filw.id
        await bot.copy_message(chat_id=Config.BIN_CHANNEL, from_chat_id=from_chat, message_id=mg_id)
        await asyncio.sleep(2)
        await bot.copy_message(update.from_user.id, from_chat, mg_id)
        await bot.delete_messages(from_chat, mg_id)
    else:
        # Upload file using unified function for regular files
        filw, error = await upload_files(
            bot, update.message.chat.id, upload_type, final_file_path, 
            ph_path, caption, duration, rkn_processing
        )
        if error:
            if bot.premium and bot.uploadlimit:
                used_remove = int(used) - int(media.file_size)
                await digital_botz.set_used_limit(user_id, used_remove)
            await remove_path(ph_path, file_path, dl_path, metadata_path)
            return await rkn_processing.edit(f"Upload Error: {escape(str(error))}")
        await bot.copy_message(chat_id=Config.BIN_CHANNEL, from_chat_id=filw.chat.id, message_id=filw.id)
    await remove_path(ph_path, file_path, dl_path, metadata_path)
    return await rkn_processing.edit("Uploaded Successfully....")
