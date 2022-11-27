from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from tools.config import Config
from tools.process import add_fg
from tools.db import MysqlDB
import os

database = MysqlDB()
config = Config()
updater = Updater(config.get_token(), use_context=True)

def tele_pic(update, context):
    # Download user photo
    user_id = str(update.effective_chat.id)
    photo_name = f"./tmp/{user_id}.jpg"
    result_photo_name = f"./tmp/result{user_id}.jpg"
    file_id = update.message.photo[-1]
    new_file = context.bot.getFile(file_id)
    new_file.download(photo_name)
    # Process photo
    add_fg(photo_name, result_photo_name)
    # Send result to user
    photo = open(result_photo_name, 'rb')
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo)
    photo.close()
    # Delete user photo and result photo
    if os.path.exists(photo_name):
        os.remove(photo_name)
    if os.path.exists(result_photo_name):
        os.remove(result_photo_name)
    # Save log to database
    database.add_process(update.effective_chat.id)

def tele_file(update, context):
    # Download user photo
    user_id = str(update.effective_chat.id)
    photo_name = f"./tmp/{user_id}.jpg"
    result_photo_name = f"./tmp/result{user_id}.jpg"
    file_id = update.message.document.file_id
    new_file = context.bot.getFile(file_id)
    new_file.download(photo_name)
    # Process photo
    add_fg(photo_name, result_photo_name)
    # Send result to user
    photo = open(result_photo_name, 'rb')
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo)
    photo.close()
    # Delete user photo and result photo
    if os.path.exists(photo_name):
        os.remove(photo_name)
    if os.path.exists(result_photo_name):
        os.remove(result_photo_name)
    # Save log to database
    database.add_process(update.effective_chat.id)


def start(update, context):
    user_id = str(update.effective_chat.id)
    message = "ٌWelcome To Profile Bot\n" \
              "You can contact us by sending messages in bot chat.\n"
    database.start_put(update.effective_chat.id)
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    # Process Profile Photo of User
    profile_photos = context.bot.get_user_profile_photos(update.effective_user.id)
    if profile_photos["total_count"] > 0:
        # Download user profile photo
        photo_name = f"./tmp/{user_id}.jpg"
        result_photo_name = f"./tmp/result{user_id}.jpg"
        profile_photo_id = profile_photos["photos"][0][-1]["file_id"]
        new_file = context.bot.getFile(profile_photo_id)
        new_file.download(photo_name)
        # Process photo
        add_fg(photo_name, result_photo_name)
        # Send result to user
        photo = open(result_photo_name, 'rb')
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo)
        photo.close()
        # Delete user photo and result photo
        if os.path.exists(photo_name):
            os.remove(photo_name)
        if os.path.exists(result_photo_name):
            os.remove(result_photo_name)
        # Save log to database
        database.add_process(update.effective_chat.id)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Send your photos to create profiles.")


def ex_message(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Entered message format is not valid")


def message(update, context):
    user_id = update.effective_chat.id
    text = update.message.text
    database.save_message(user_id, text)
    context.bot.send_message(chat_id=user_id, text="Your message saved and forwarded to support team.\nThanks")


if __name__ == '__main__':

    if not os.path.exists("./tmp"):
        os.makedirs("./tmp")
    dp = updater.dispatcher

    start_handler = CommandHandler("start", start)
    photo_handle = MessageHandler(Filters.photo, tele_pic)
    file_photo_handler = MessageHandler(Filters.document.category('image'), tele_file)
    ex_handler = MessageHandler(Filters.video, ex_message)
    message_handler = MessageHandler(Filters.text, message)

    dp.add_handler(photo_handle)
    dp.add_handler(start_handler)
    dp.add_handler(file_photo_handler)
    dp.add_handler(ex_handler)
    dp.add_handler(message_handler)

    updater.start_polling()
    updater.idle()


# TODO:
#       2. Create tmp folder at start if not exists
#       3. Update README.md
