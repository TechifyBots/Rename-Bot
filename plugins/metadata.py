from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery, ForceReply, InlineKeyboardButton, InlineKeyboardMarkup, LinkPreviewOptions
from helper.database import digital_botz
from config import rkn
from html import escape

TRUE = [[InlineKeyboardButton('Metadata On', callback_data='metadata_1'),
       InlineKeyboardButton('✅', callback_data='metadata_1')
       ],[
       InlineKeyboardButton('Set Custom Metadata', callback_data='custom_metadata')]]
FALSE = [[InlineKeyboardButton('Metadata Off', callback_data='metadata_0'),
        InlineKeyboardButton('❌', callback_data='metadata_0')
       ],[
       InlineKeyboardButton('Set Custom Metadata', callback_data='custom_metadata')]]


@Client.on_message(filters.private & filters.command('metadata'))
async def handle_metadata(bot: Client, message: Message):
    RknDev = await message.reply_text("<b>Please Wait...</b>")
    bool_metadata = await digital_botz.get_metadata_mode(message.from_user.id)
    user_metadata = await digital_botz.get_metadata_code(message.from_user.id)
    await RknDev.edit(
        f"Your Current Metadata:-\n\n➜ <code>{escape(str(user_metadata))}</code>",
        reply_markup=InlineKeyboardMarkup(TRUE if bool_metadata else FALSE)
    )

@Client.on_callback_query(filters.regex('.*?(custom_metadata|metadata).*?'))
async def query_metadata(bot: Client, query: CallbackQuery):
    await query.answer()
    data = query.data
    if data.startswith('metadata_'):
        _bool = data.split('_')[1]
        user_metadata = await digital_botz.get_metadata_code(query.from_user.id)
        bool_meta = _bool == "1"
        await digital_botz.set_metadata_mode(query.from_user.id, bool_meta=not bool_meta)
        await query.message.edit(f"Your Current Metadata:-\n\n➜ <code>{escape(str(user_metadata))}</code>", reply_markup=InlineKeyboardMarkup(FALSE if bool_meta else TRUE))
           
    elif data == 'custom_metadata':
        await query.message.reply_text(
            rkn.SEND_METADATA,
            reply_markup=ForceReply(selective=True),
            link_preview_options=LinkPreviewOptions(is_disabled=True),
        )
        await query.message.delete()


@Client.on_message(filters.private & filters.reply & filters.text)
async def save_metadata_code(bot: Client, message: Message):
    reply_to = message.reply_to_message
    if not reply_to or not reply_to.from_user or not reply_to.from_user.is_self:
        return
    if not (reply_to.reply_markup and isinstance(reply_to.reply_markup, ForceReply)):
        return
    if rkn.SEND_METADATA.splitlines()[0] not in (reply_to.text or ""):
        return
    await digital_botz.set_metadata_code(message.from_user.id, metadata_code=message.text)
    await reply_to.delete()
    await message.reply_text("<b>Your Metadata Code Set Successfully ✅</b>")
