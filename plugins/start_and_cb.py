import random, asyncio, datetime, time, psutil, shutil
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply, LinkPreviewOptions, CallbackQuery
from helper.database import digital_botz
from config import Config, rkn
from helper.utils import humanbytes
from plugins import __version__ as _bot_version_, __developer__, __database__, __library__, __language__, __programer__
from plugins.file_rename import upload_doc

upgrade_button = InlineKeyboardMarkup([[        
        InlineKeyboardButton('ʙᴜʏ ᴘʀᴇᴍɪᴜᴍ ✓', user_id=int(Config.ADMIN)),
         ],[
        InlineKeyboardButton("ʙᴀᴄᴋ", callback_data = "start")
]])

upgrade_trial_button = InlineKeyboardMarkup([[        
        InlineKeyboardButton('ʙᴜʏ ᴘʀᴇᴍɪᴜᴍ ✓', user_id=int(Config.ADMIN)),
         ],[
        InlineKeyboardButton("ᴛʀɪᴀʟ", callback_data = "give_trial"),
        InlineKeyboardButton("ʙᴀᴄᴋ", callback_data = "start")
]])
        
@Client.on_message(filters.private & filters.command("start"))
async def start(client, message):
    start_button = [[
        InlineKeyboardButton('ᴀʙᴏᴜᴛ', callback_data='about'),
        InlineKeyboardButton('ʜᴇʟᴘ', callback_data='help')       
         ]]
    if client.premium:
        start_button.append([InlineKeyboardButton('💸 ᴜᴘɢʀᴀᴅᴇ ᴛᴏ ᴘʀᴇᴍɪᴜᴍ 💸', callback_data='upgrade')])
    user = message.from_user
    await digital_botz.add_user(client, message) 
    if Config.PIC:
        await message.reply_photo(Config.PIC, caption=rkn.START_TXT.format(user.mention), reply_markup=InlineKeyboardMarkup(start_button))    
    else:
        await message.reply_text(text=rkn.START_TXT.format(user.mention), reply_markup=InlineKeyboardMarkup(start_button), link_preview_options=LinkPreviewOptions(is_disabled=True))

@Client.on_message(filters.private & filters.command('setprefix'))
async def add_prefix(client, message):
    if len(message.command) == 1:
        return await message.reply_text("**__Give The Prefix__\n\nExᴀᴍᴩʟᴇ:- `/setprefix @TechifyBots`**")
    prefix = message.text.split(" ", 1)[1]
    RknDev = await message.reply_text("Please Wait ...")
    await digital_botz.set_prefix(message.from_user.id, prefix)
    await RknDev.edit("__**✅ ᴘʀᴇꜰɪx ꜱᴀᴠᴇᴅ**__")

@Client.on_message(filters.private & filters.command('delprefix'))
async def delete_prefix(client, message):
    RknDev = await message.reply_text("Please Wait ...")
    prefix = await digital_botz.get_prefix(message.from_user.id)
    if not prefix:
        return await RknDev.edit("__**😔 ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴀɴʏ ᴘʀᴇꜰɪx**__")
    await digital_botz.set_prefix(message.from_user.id, None)
    await RknDev.edit("__**❌️ ᴘʀᴇꜰɪx ᴅᴇʟᴇᴛᴇᴅ**__")

@Client.on_message(filters.private & filters.command('seeprefix'))
async def see_prefix(client, message):
    RknDev = await message.reply_text("Please Wait ...")
    prefix = await digital_botz.get_prefix(message.from_user.id)
    if prefix:
        await RknDev.edit(f"**ʏᴏᴜʀ ᴘʀᴇꜰɪx:-**\n\n`{prefix}`")
    else:
        await RknDev.edit("__**😔 ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴀɴʏ ᴘʀᴇꜰɪx**__")

@Client.on_message(filters.private & filters.command('setsuffix'))
async def add_suffix(client, message):
    if len(message.command) == 1:
        return await message.reply_text("**__Give The Suffix__\n\nExᴀᴍᴩʟᴇ:- `/setsuffix @TechifyBots`**")
    suffix = message.text.split(" ", 1)[1]
    RknDev = await message.reply_text("Please Wait ...")
    await digital_botz.set_suffix(message.from_user.id, suffix)
    await RknDev.edit("__**✅ ꜱᴜꜰꜰɪx ꜱᴀᴠᴇᴅ**__")

@Client.on_message(filters.private & filters.command('delsuffix'))
async def delete_suffix(client, message):
    RknDev = await message.reply_text("Please Wait ...")
    suffix = await digital_botz.get_suffix(message.from_user.id)
    if not suffix:
        return await RknDev.edit("__**😔 ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴀɴʏ ꜱᴜꜰꜰɪx**__")
    await digital_botz.set_suffix(message.from_user.id, None)
    await RknDev.edit("__**❌️ ꜱᴜꜰꜰɪx ᴅᴇʟᴇᴛᴇᴅ**__")

@Client.on_message(filters.private & filters.command('seesuffix'))
async def see_suffix(client, message):
    RknDev = await message.reply_text("Please Wait ...")
    suffix = await digital_botz.get_suffix(message.from_user.id)
    if suffix:
        await RknDev.edit(f"**ʏᴏᴜʀ ꜱᴜꜰꜰɪx:-**\n\n`{suffix}`")
    else:
        await RknDev.edit("__**😔 ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴀɴʏ ꜱᴜꜰꜰɪx**__")

@Client.on_message(filters.private & filters.command('setcaption'))
async def add_caption(client, message):
    rkn = await message.reply_text("__**ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ**__")
    if len(message.command) == 1:
       return await rkn.edit("**__Gɪᴠᴇ Tʜᴇ Cᴀᴩᴛɪᴏɴ__\n\nExᴀᴍᴩʟᴇ:- `/setcaption {filename}\n\n💾 Sɪᴢᴇ: {filesize}\n\n⏰ Dᴜʀᴀᴛɪᴏɴ: {duration}\n**By: @TechifyBots`**")
    caption = message.text.split(" ", 1)[1]
    await digital_botz.set_caption(message.from_user.id, caption=caption)
    await rkn.edit("__**✅ Cᴀᴩᴛɪᴏɴ Sᴀᴠᴇᴅ**__")
   
@Client.on_message(filters.private & filters.command('delcaption'))
async def delete_caption(client, message):
    rkn = await message.reply_text("__**ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ**__")
    caption = await digital_botz.get_caption(message.from_user.id)  
    if not caption:
       return await rkn.edit("__**😔 Yᴏᴜ Dᴏɴ'ᴛ Hᴀᴠᴇ Aɴy Cᴀᴩᴛɪᴏɴ**__")
    await digital_botz.set_caption(message.from_user.id, caption=None)
    await rkn.edit("__**❌️ Cᴀᴩᴛɪᴏɴ Dᴇʟᴇᴛᴇᴅ**__")
                                       
@Client.on_message(filters.private & filters.command('seecaption'))
async def see_caption(client, message):
    rkn = await message.reply_text("__**ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ**__")
    caption = await digital_botz.get_caption(message.from_user.id)  
    if caption:
       await rkn.edit(f"**Yᴏᴜ'ʀᴇ Cᴀᴩᴛɪᴏɴ:-**\n\n`{caption}`")
    else:
       await rkn.edit("__**😔 Yᴏᴜ Dᴏɴ'ᴛ Hᴀᴠᴇ Aɴy Cᴀᴩᴛɪᴏɴ**__")

@Client.on_message(filters.private & filters.command('viewthumb'))
async def viewthumb(client, message):
    rkn = await message.reply_text("__**ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ**__")
    thumb = await digital_botz.get_thumbnail(message.from_user.id)
    if thumb:
        await client.send_photo(chat_id=message.chat.id, photo=thumb)
        await rkn.delete()
    else:
        await rkn.edit("😔 __**Yᴏᴜ Dᴏɴ'ᴛ Hᴀᴠᴇ Aɴy Tʜᴜᴍʙɴᴀɪʟ**__") 
		
@Client.on_message(filters.private & filters.command('delthumb'))
async def removethumb(client, message):
    rkn = await message.reply_text("__**ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ**__")
    thumb = await digital_botz.get_thumbnail(message.from_user.id)
    if thumb:
        await digital_botz.set_thumbnail(message.from_user.id, file_id=None)
        await rkn.edit("❌️ __**Tʜᴜᴍʙɴᴀɪʟ Dᴇʟᴇᴛᴇᴅ**__")
        return
    await rkn.edit("😔 __**Yᴏᴜ Dᴏɴ'ᴛ Hᴀᴠᴇ Aɴy Tʜᴜᴍʙɴᴀɪʟ**__")

@Client.on_message(filters.private & filters.photo)
async def addthumbs(client, message):
    rkn = await message.reply_text("__**ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ**__")
    await digital_botz.set_thumbnail(message.from_user.id, file_id=message.photo.file_id)                
    await rkn.edit("✅️ __**Tʜᴜᴍʙɴᴀɪʟ Sᴀᴠᴇᴅ**__")

@Client.on_message(filters.private & filters.command("myplan"))
async def myplan(client, message):
    if not client.premium:
        return # premium mode disabled ✓
    user_id = message.from_user.id
    user = message.from_user.mention
    if await digital_botz.has_premium_access(user_id):
        data = await digital_botz.get_user(user_id)
        expiry_str_in_ist = data.get("expiry_time")
        time_left_str = expiry_str_in_ist - datetime.datetime.now()
        text = f"ᴜꜱᴇʀ :- {user}\nᴜꜱᴇʀ ɪᴅ :- <code>{user_id}</code>\n"
        if client.uploadlimit:
            await digital_botz.reset_uploadlimit_access(user_id)                
            user_data = await digital_botz.get_user_data(user_id)
            limit = user_data.get('uploadlimit', 0)
            used = user_data.get('used_limit', 0)
            remain = int(limit) - int(used)
            type = user_data.get('usertype', "Free")
            text += f"ᴘʟᴀɴ :- `{type}`\nᴅᴀɪʟʏ ᴜᴘʟᴏᴀᴅ ʟɪᴍɪᴛ :- `{humanbytes(limit)}`\nᴛᴏᴅᴀʏ ᴜsᴇᴅ :- `{humanbytes(used)}`\nʀᴇᴍᴀɪɴ :- `{humanbytes(remain)}`\n"
        text += f"ᴛɪᴍᴇ ʟᴇꜰᴛ : {time_left_str}\nᴇxᴘɪʀʏ ᴅᴀᴛᴇ : {expiry_str_in_ist}"
        await message.reply_text(text)
    else:
        if client.uploadlimit:
            user_data = await digital_botz.get_user_data(user_id)
            limit = user_data.get('uploadlimit', 0)
            used = user_data.get('used_limit', 0)
            remain = int(limit) - int(used)
            type = user_data.get('usertype', "Free")
            text = f"ᴜꜱᴇʀ :- {user}\nᴜꜱᴇʀ ɪᴅ :- <code>{user_id}</code>\nᴘʟᴀɴ :- `{type}`\nᴅᴀɪʟʏ ᴜᴘʟᴏᴀᴅ ʟɪᴍɪᴛ :- `{humanbytes(limit)}`\nᴛᴏᴅᴀʏ ᴜsᴇᴅ :- `{humanbytes(used)}`\nʀᴇᴍᴀɪɴ :- `{humanbytes(remain)}`\nᴇxᴘɪʀᴇᴅ ᴅᴀᴛᴇ :- ʟɪғᴇᴛɪᴍᴇ\n\nɪꜰ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴛᴀᴋᴇ ᴘʀᴇᴍɪᴜᴍ ᴛʜᴇɴ ᴄʟɪᴄᴋ ᴏɴ ʙᴇʟᴏᴡ ʙᴜᴛᴛᴏɴ 👇"
            await message.reply_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("💸 ᴄʜᴇᴄᴋᴏᴜᴛ ᴘʀᴇᴍɪᴜᴍ ᴘʟᴀɴꜱ 💸", callback_data='upgrade')]]))
        else:
            m=await message.reply_sticker("CAACAgIAAxkBAAIBTGVjQbHuhOiboQsDm35brLGyLQ28AAJ-GgACglXYSXgCrotQHjibHgQ")
            await message.reply_text(f"ʜᴇʏ {user},\n\nʏᴏᴜ ᴅᴏ ɴᴏᴛ ʜᴀᴠᴇ ᴀɴʏ ᴀᴄᴛɪᴠᴇ ᴘʀᴇᴍɪᴜᴍ ᴘʟᴀɴs, ɪꜰ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴛᴀᴋᴇ ᴘʀᴇᴍɪᴜᴍ ᴛʜᴇɴ ᴄʟɪᴄᴋ ᴏɴ ʙᴇʟᴏᴡ ʙᴜᴛᴛᴏɴ 👇",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("💸 ᴄʜᴇᴄᴋᴏᴜᴛ ᴘʀᴇᴍɪᴜᴍ ᴘʟᴀɴꜱ 💸", callback_data='upgrade')]]))			 
            await asyncio.sleep(2)
            await m.delete()

@Client.on_message(filters.private & filters.command("plans"))
async def plans(client, message):
    if not client.premium:
        return # premium mode disabled ✓
    user = message.from_user
    upgrade_msg = rkn.UPGRADE_PLAN.format(user.mention) if client.uploadlimit else rkn.UPGRADE_PREMIUM.format(user.mention)
    free_trial_status = await digital_botz.get_free_trial_status(user.id)
    if not await digital_botz.has_premium_access(user.id):
        if not free_trial_status:
            await message.reply_text(text=upgrade_msg, reply_markup=upgrade_trial_button, link_preview_options=LinkPreviewOptions(is_disabled=True))
        else:
            await message.reply_text(text=upgrade_msg, reply_markup=upgrade_button, link_preview_options=LinkPreviewOptions(is_disabled=True))
    else:
        await message.reply_text(text=upgrade_msg, reply_markup=upgrade_button, link_preview_options=LinkPreviewOptions(is_disabled=True))

@Client.on_callback_query()
async def cb_handler(client, query: CallbackQuery):
    data = query.data 
    if data == "start":
        start_button = [[
        InlineKeyboardButton('ᴀʙᴏᴜᴛ', callback_data='about'),
        InlineKeyboardButton('ʜᴇʟᴘ', callback_data='help')       
         ]]
        if client.premium:
            start_button.append([InlineKeyboardButton('💸 ᴜᴘɢʀᴀᴅᴇ ᴛᴏ ᴘʀᴇᴍɪᴜᴍ 💸', callback_data='upgrade')])
        await query.message.edit_text(
            text=rkn.START_TXT.format(query.from_user.mention),
            link_preview_options=LinkPreviewOptions(is_disabled=True),
            reply_markup = InlineKeyboardMarkup(start_button))
        
    elif data == "help":
        await query.message.edit_text(
            text=rkn.HELP_TXT,
            link_preview_options=LinkPreviewOptions(is_disabled=True),
            reply_markup=InlineKeyboardMarkup([[
                #⚠️ don't change source code & source link ⚠️ #
                InlineKeyboardButton("ᴛʜᴜᴍʙɴᴀɪʟ", callback_data = "thumbnail"),
                InlineKeyboardButton("ᴄᴀᴘᴛɪᴏɴ", callback_data = "caption")
                ],[
                InlineKeyboardButton("ꜰɪʟᴇ ɴᴀᴍᴇ", callback_data = "custom_file_name"),
                InlineKeyboardButton("ᴍᴇᴛᴀᴅᴀᴛᴀ", callback_data = "custom_metadata")
                ],[
                InlineKeyboardButton("ʙᴀᴄᴋ", callback_data = "start")
                ]]))         
        
    elif data == "about":
        about_button = [[
         #⚠️ don't change source code & source link ⚠️ #
        InlineKeyboardButton("sᴏᴜʀᴄᴇ", callback_data = "source_code"), #Whoever is deploying this repo is given a warning ⚠️ not to remove this repo link #first & last warning ⚠️
        InlineKeyboardButton("ʙᴏᴛ sᴛᴀᴛᴜs", callback_data = "bot_status")
        ],[
        InlineKeyboardButton("ʟɪᴠᴇ sᴛᴀᴛᴜs", callback_data = "live_status")           
        ]]
        if client.premium:
            about_button[-1].append(InlineKeyboardButton("ᴜᴘɢʀᴀᴅᴇ", callback_data = "upgrade"))
            about_button.append([InlineKeyboardButton("ʙᴀᴄᴋ", callback_data = "start")])
        else:
            about_button[-1].append(InlineKeyboardButton("ʙᴀᴄᴋ", callback_data = "start"))
        await query.message.edit_text(
            text=rkn.ABOUT_TXT.format(client.mention, __developer__, __programer__, __library__, __language__, __database__, _bot_version_),
            link_preview_options=LinkPreviewOptions(is_disabled=True),
            reply_markup=InlineKeyboardMarkup(about_button))    
        
    elif data == "upgrade":
        if not client.premium:
            return await query.message.delete()
        user = query.from_user
        upgrade_msg = rkn.UPGRADE_PLAN.format(user.mention) if client.uploadlimit else rkn.UPGRADE_PREMIUM.format(user.mention)
        free_trial_status = await digital_botz.get_free_trial_status(query.from_user.id)
        if not await digital_botz.has_premium_access(query.from_user.id):
            if not free_trial_status:
                await query.message.edit_text(text=upgrade_msg, reply_markup=upgrade_trial_button, link_preview_options=LinkPreviewOptions(is_disabled=True))   
            else:
                await query.message.edit_text(text=upgrade_msg, reply_markup=upgrade_button, link_preview_options=LinkPreviewOptions(is_disabled=True))
        else:
            await query.message.edit_text(text=upgrade_msg, reply_markup=upgrade_button, link_preview_options=LinkPreviewOptions(is_disabled=True))
           
    elif data == "give_trial":
        if not client.premium:
            return await query.message.delete()
        await query.message.delete()
        free_trial_status = await digital_botz.get_free_trial_status(query.from_user.id)
        if not free_trial_status:            
            await digital_botz.give_free_trial(query.from_user.id)
            new_text = "**ʏᴏᴜʀ ᴘʀᴇᴍɪᴜᴍ ᴛʀɪᴀʟ ʜᴀs ʙᴇᴇɴ ᴀᴅᴅᴇᴅ ғᴏʀ 𝟷𝟸 ʜᴏᴜʀs.\n\nʏᴏᴜ ᴄᴀɴ ᴜsᴇ ꜰʀᴇᴇ ᴛʀᴀɪʟ ꜰᴏʀ 𝟷𝟸 ʜᴏᴜʀs ꜰʀᴏᴍ ɴᴏᴡ 😀\n\nआप अब से 𝟷𝟸 घण्टा के लिए निःशुल्क ट्रायल का उपयोग कर सकते हैं 😀**"
        else:
            new_text = "**🤣 ʏᴏᴜ ᴀʟʀᴇᴀᴅʏ ᴜsᴇᴅ ғʀᴇᴇ ɴᴏᴡ ɴᴏ ᴍᴏʀᴇ ғʀᴇᴇ ᴛʀᴀɪʟ. ᴘʟᴇᴀsᴇ ʙᴜʏ sᴜʙsᴄʀɪᴘᴛɪᴏɴ ʜᴇʀᴇ ᴀʀᴇ ᴏᴜʀ 👉 /plans**"
        await client.send_message(query.from_user.id, text=new_text)

    elif data == "thumbnail":
        await query.message.edit_text(
            text=rkn.THUMBNAIL,
            link_preview_options=LinkPreviewOptions(is_disabled=True),
            reply_markup=InlineKeyboardMarkup([[
             InlineKeyboardButton("ʙᴀᴄᴋ", callback_data = "help")]]))

    elif data == "caption":
        await query.message.edit_text(
            text=rkn.CAPTION,
            link_preview_options=LinkPreviewOptions(is_disabled=True),
            reply_markup=InlineKeyboardMarkup([[
             InlineKeyboardButton("ʙᴀᴄᴋ", callback_data = "help")]]))

    elif data == "custom_file_name":
        await query.message.edit_text(
            text=rkn.CUSTOM_FILE_NAME,
            link_preview_options=LinkPreviewOptions(is_disabled=True),
            reply_markup=InlineKeyboardMarkup([[
             InlineKeyboardButton("ʙᴀᴄᴋ", callback_data = "help")]]))

    elif data == "custom_metadata":
        await query.message.edit_text(
            text=rkn.METADATA,
            link_preview_options=LinkPreviewOptions(is_disabled=True),
            reply_markup=InlineKeyboardMarkup([[
             InlineKeyboardButton("ʙᴀᴄᴋ", callback_data = "help")]]))

    elif data == "bot_status":
        total_users = await digital_botz.total_users_count()
        if client.premium:
            total_premium_users = await digital_botz.total_premium_users_count()
        else:
            total_premium_users = "Disabled ✅"
        uptime = time.strftime("%Hh%Mm%Ss", time.gmtime(time.time() - client.uptime))
        sent = humanbytes(psutil.net_io_counters().bytes_sent)
        recv = humanbytes(psutil.net_io_counters().bytes_recv)
        await query.message.edit_text(
            text=rkn.BOT_STATUS.format(uptime, total_users, total_premium_users, sent, recv),
            link_preview_options=LinkPreviewOptions(is_disabled=True),
            reply_markup=InlineKeyboardMarkup([[
             InlineKeyboardButton("ʙᴀᴄᴋ", callback_data = "about")]]))

    elif data == "live_status":
        currentTime = time.strftime("%Hh%Mm%Ss", time.gmtime(time.time() - client.uptime))
        total, used, free = shutil.disk_usage(".")
        total = humanbytes(total)
        used = humanbytes(used)
        free = humanbytes(free)
        sent = humanbytes(psutil.net_io_counters().bytes_sent)
        recv = humanbytes(psutil.net_io_counters().bytes_recv)
        cpu_usage = psutil.cpu_percent(interval=0.5)
        ram_usage = psutil.virtual_memory().percent
        disk_usage = psutil.disk_usage('/').percent
        await query.message.edit_text(
            text=rkn.LIVE_STATUS.format(currentTime, cpu_usage, ram_usage, total, used, disk_usage, free, sent, recv),
            link_preview_options=LinkPreviewOptions(is_disabled=True),
            reply_markup=InlineKeyboardMarkup([[
             InlineKeyboardButton("ʙᴀᴄᴋ", callback_data = "about")]]))

    elif data == "source_code":
        await query.message.edit_text(
            text=rkn.DEV_TXT,
            link_preview_options=LinkPreviewOptions(is_disabled=True),
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("💞 sᴏᴜʀᴄᴇ ᴄᴏᴅᴇ 💞", url="https://github.com/TechifyBots/Rename-Bot")
            ],[
                InlineKeyboardButton("ᴄʟᴏꜱᴇ", callback_data = "close"),
                InlineKeyboardButton("ʙᴀᴄᴋ", callback_data = "about")
            ]])
        )

    elif data.startswith("upload"):
        await upload_doc(client, query)

    elif data == "close":
        try:
            await query.message.delete()
            await query.message.reply_to_message.delete()
            await query.message.continue_propagation()
        except Exception:
            await query.message.delete()
            await query.message.continue_propagation()
