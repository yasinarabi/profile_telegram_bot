from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from tools.config import Config
from tools.process import add_fg
from tools.db import MysqlDB
import os

database = MysqlDB()
config = Config()
updater = Updater(config.get_token(), use_context=True)

def tele_pic(update, context):
    user_id = str(update.effective_chat.id)
    photo_name = user_id + '.jpg'
    new_photo_name = "new" + photo_name
    file_id = update.message.photo[-1]
    new_file = context.bot.getFile(file_id)
    new_file.download(photo_name)
    add_fg(photo_name)
    photo = open(new_photo_name, 'rb')
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo)
    photo.close()
    if os.path.exists(photo_name):
        os.remove(photo_name)
    if os.path.exists(new_photo_name):
        os.remove(new_photo_name)
    database.add_process(update.effective_chat.id)


def start(update, context):
    database.start_put(update.effective_chat.id)
    context.bot.send_message(chat_id=update.effective_chat.id, text="ٌWelcome To Profile Bot")
    context.bot.send_message(chat_id=update.effective_chat.id, text="You can contact us with sending messages in the bot chat ")


def ex_message(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Entered message format is not valid")


def message(update, context):
    user_id = update.effective_chat.id
    text = update.message.text
    database.save_message(user_id, text)
    context.bot.send_message(chat_id=user_id, text="Your message saved and forwarded to support team.\nThanks")


if __name__ == '__main__':
    dp = updater.dispatcher

    start_handler = CommandHandler("start", start)
    photo_handle = MessageHandler(Filters.photo, tele_pic)
    ex_handler = MessageHandler(Filters.video, ex_message)
    message_handler = MessageHandler(Filters.text, message)

    dp.add_handler(photo_handle)
    dp.add_handler(start_handler)
    dp.add_handler(ex_handler)
    dp.add_handler(message_handler)

    updater.start_polling()
    updater.idle()
