# http://t.me/tokiohackspammerbot

import dotenv, os
import telegram, telegram.ext
from telegram.ext import MessageHandler, CommandHandler
from telegram.ext import CallbackContext
from telegram import Update

dotenv.load_dotenv()

TOKEN = os.environ['TOKEN']
HEROKU_APP_NAME = 'tokiohackspammerbot'

print(TOKEN)

updater = telegram.ext.Updater(TOKEN)
dispatcher = updater.dispatcher

def start(update: telegram.Update, context: telegram.ext.CallbackContext):
    update.message.reply_text("Hello, to start spamming press /spam", 
        reply_markup=telegram.ReplyKeyboardMarkup([['/spam']]))

def spam(update: Update, context: CallbackContext):
    # read list.json
    import json, time
    t_groups = []
    with open('list.json', 'r', encoding='utf8') as f:
        f_content = f.read()
        t_groups = json.loads(f_content)
    # send message to all in a loop
    for i in range(len(t_groups)):
        try:
            t_chat = context.bot.get_chat(t_groups[i])
            print(t_chat.type, t_chat.link, i)
            # not all chatid are correct
            print(context.bot.send_message(chat_id=t_groups[i], text="Hello"))
            time.sleep(0.5)
        except Exception as ex:
            print(f'[ {ex} ]\n')
        if i > 200: break


dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('spam', spam))

print(updater.bot.get_me())
# updater.start_polling()

# import os
PORT = int(os.environ.get('PORT', '8443'))
print(PORT)
updater.start_webhook(listen="0.0.0.0",
                      port=PORT,
                      url_path=TOKEN,
                      webhook_url=f"https://{HEROKU_APP_NAME}.herokuapp.com/" + TOKEN)


updater.idle()