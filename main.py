import os
import logging
from pyrogram import Client, filters
from pyrogram.types import InputMediaPhoto, InlineKeyboardMarkup, InlineKeyboardButton
from creds import Credentials
from telegraph import upload_file, Telegraph

logging.basicConfig(level=logging.WARNING)

telegraph = Telegraph()
telegraph.create_account(short_name='777')

tgraph = Client(
    "Image upload bot",
    bot_token=Credentials.BOT_TOKEN,
    api_id=Credentials.API_ID,
    api_hash=Credentials.API_HASH
)

all_media_path = []
media_group = []
messages = 0
telegraph_heading = "Best of 18+ video 🔞️"

@tgraph.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text(
        text=f"Hello {message.from_user.mention},\n\nI'm a telegram to telegra.ph image uploader bot by @temp_demo",
        disable_web_page_preview=True
    )

@tgraph.on_message(filters.command("cancel"))
async def start(client, message):
    all_media_path.clear()
    media_group.clear()
    global messages
    messages = 0
    await message.reply_text(
        text="Successfully cancelled ongoing process",
        disable_web_page_preview=True
    )

@tgraph.on_message(filters.command("sct"))
async def start(client, message):
    userMessage = message.command
    if len(userMessage) > 1:
        userMessage.pop(0)
        global telegraph_heading
        telegraph_heading = ' '.join(userMessage)
        await message.reply_text(f"Custom title for telegra.ph posts is succesfully changed to {telegraph_heading}", True)
    else:
        await message.reply_text("Something Went Wrong !!, Please try again ...", True)

    
@tgraph.on_message(filters.animation)
async def getimage(client, message):
    dwn = await message.reply_text("Downloading to my server...", True)
    all_media_path.append(await message.download())
    await dwn.edit_text(
        text=f"You sent an animation.\n\n<b>Received {len(all_media_path)} File(s)\n\nPlease click below button to strat uploading.</b>",
        disable_web_page_preview=False,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Done, Upload to telegra.ph", callback_data="upload"
                    )
                ]
            ]
        )
    )

@tgraph.on_message(filters.media_group)
async def getmedia(client, message):
        global media_group, messages
        dwn = await message.reply_text("Downloading to my server...", True)
        media_group = await message.get_media_group()
        messages += 1
        await dwn.edit_text(
        text=f"Please click on below button when you finish with sending all files.\n\n<b>Received {messages} File(s)</b>",
        disable_web_page_preview=False,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="Done, Upload to telegra.ph", callback_data="upload"
                        )
                    ]
                ]
            )
        )
    
@tgraph.on_message(filters.photo)
async def getimage(client, message):
    dwn = await message.reply_text("Downloading to my server...", True)
    all_media_path.append(await message.download())
    await dwn.edit_text(
        text=f"Please click on below button when you finish with sending all files.\n\n<b>Received {len(all_media_path)} File(s)</b>",
        disable_web_page_preview=False,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Done, Upload to telegra.ph", callback_data="upload"
                    )
                ]
            ]
        )
    )
    
def get_content(content):
    finalContent = []
    for tags in content:
        finalContent.append({
            "tag": "figure",
            "children": [
                {
                    "tag": "img",
                    "attrs": { "src": f"https://telegra.ph{tags}" }
                }
            ]
        })
    finalContent.append({
        "tag": "strong", 
        "children": ["💠 Backup Channel :\n"]
    })
    finalContent.append({
        "tag": "a",
        "attrs": { "href": "https://t.me/joinchat/ojOOaC4tqkU5MTVl" },
        "children": [" ➤ https://t.me/joinchat/ojOOaC4tqkU5MTVl \n\n"]
    })
    finalContent.append({
        "tag": "strong", 
        "children": ["♻️ Other Channels \n"]
    })
    finalContent.append({
        "tag": "a",
        "attrs": { "href": "https://t.me/my_channels_list_official" },
        "children": [" ➤ https://t.me/my_channels_list_official"]
    })
    return finalContent    
        

@tgraph.on_callback_query()
async def getimage(client, update):
    await update.message.edit_text(
            text="Uploading to telegra.ph",
            disable_web_page_preview=False
        )
    try:
        global media_group
        media_group = sorted(media_group, key=lambda o: o['message_id'])
        for media_path in media_group:
            all_media_path.append(await media_path.download())
        url_path = upload_file(all_media_path)
        final_content = get_content(url_path)
        global telegraph_heading
        response = telegraph.create_page(
            telegraph_heading,
            content=final_content,
            author_name='Rohit Sharma',
            author_url='https://t.me/my_channels_list_official'
        )
        await update.message.edit_text(f"{'https://telegra.ph/{}'.format(response['path'])}")
        clear_media_path()
    except Exception as error:
        await update.message.edit_text(f"Oops something went wrong\n{error}")
        clear_media_path()
        return


def clear_media_path ():
    if len(all_media_path) == 0:
        return
    else:
       to_remove_existing_media = all_media_path
       all_media_path.clear()
       media_group.clear()
       global messages
       messages = 0
       for media_path in to_remove_existing_media:
            os.remove(media_path)
            
tgraph.run()
