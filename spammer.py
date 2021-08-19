# http://t.me/tokiohackspammerbot

import dotenv, os
import requests
import json, time
import telegram, telegram.ext
from telegram import message
from telegram.ext import MessageHandler, CommandHandler, Filters
from telegram.ext import CallbackContext
from telegram import Update

dotenv.load_dotenv()

# Upload json with chat list

TOKEN = os.environ['TOKEN']
HEROKU_APP_NAME = 'tokiohackspammerbot'
t_groups = []
t_message = None
uploading_type = None

# print(TOKEN)

updater = telegram.ext.Updater(TOKEN)
dispatcher = updater.dispatcher

def start(update: telegram.Update, context: telegram.ext.CallbackContext):
    update.message.reply_text("Hello, upload a chat list and press /spam to start spamming ", 
        reply_markup=telegram.ReplyKeyboardMarkup([['/spam', '/upload_chatlist', '/upload_message']], resize_keyboard=True))

def spam(update: Update, context: CallbackContext):
    global t_groups
    global t_message
    if len(t_groups) == 0 or t_message is None:
        update.message.reply_text(f"You have {len(t_groups)} chats and message = {t_message}. "
            f"Please upload a chatlist.json first or upload a message")
    else:
        for i in range(len(t_groups)):
            try:
                t_chat = context.bot.get_chat(t_groups[i])
                print(t_chat.type, t_chat.link, i)
                # not all chatid are correct
                print(context.bot.send_message(chat_id=t_groups[i], text=t_message, parse_mode="html"))
                time.sleep(0.5)
            except Exception as ex:
                print(f'[ {ex} ]\n')
            # if i > 200: break

def upload(update: Update, context: CallbackContext):
    global t_groups, t_message
    global uploading_type
    if uploading_type is None:
        update.message.reply_text(f"You did not specify what are you going to upload")
    elif uploading_type == "chatlist":
        try:
            file_id = update.message.document.file_id
            file_path = context.bot.get_file(file_id)['file_path']
            res = requests.get(file_path)
            t_groups = json.loads(res.text)
            update.message.reply_text(f" json looks fine 👌 {len(t_groups)} chats")
        except Exception as ex:
            update.message.reply_text(f" 🟧 Exception happend: {ex} ")
    elif uploading_type == "message":
        try:
            file_id = update.message.document.file_id
            file_path = context.bot.get_file(file_id)['file_path']
            res = requests.get(file_path)
            t_message = res.text
            update.message.reply_text(f" Your message looks OK 👌 this is your message:")
            update.message.reply_text(t_message, parse_mode="html")
        except Exception as ex:
            update.message.reply_text(f" 🟧 Exception happend: {ex} ")


def upload_message(update: Update, context: CallbackContext):
    global uploading_type
    uploading_type = "message"
    update.message.reply_text(f"now upload a message in HTML format")

def upload_chatlist(update: Update, context: CallbackContext):
    global uploading_type
    uploading_type = "chatlist"
    update.message.reply_text('now upload a chatlist in json format like this: ["@chat1", "@chat2"]')

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('spam', spam))
dispatcher.add_handler(CommandHandler('upload_chatlist', upload_chatlist))
dispatcher.add_handler(CommandHandler('upload_message', upload_message))
dispatcher.add_handler(MessageHandler(Filters.attachment, upload))


print(f'{updater.bot.get_me()}\n')

# updater.start_polling()

PORT = int(os.environ.get('PORT', '8443'))
print(PORT)
updater.start_webhook(listen="0.0.0.0",
                      port=PORT,
                      url_path=TOKEN,
                      webhook_url=f"https://{HEROKU_APP_NAME}.herokuapp.com/" + TOKEN)

print(updater.bot.getWebhookInfo())

updater.idle()