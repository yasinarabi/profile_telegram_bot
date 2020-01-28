from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import process
import db
import os

updater = Updater("902896754:AAEceV8ktEaTaAoeQrjeDpfLwypD9DeOKF8", use_context=True)


def tele_pic(update, context):
    user_id = str(update.effective_chat.id)
    photo_name = user_id + '.jpg'
    new_photo_name = "new" + photo_name
    file_id = update.message.photo[-1]
    new_file = context.bot.getFile(file_id)
    new_file.download(photo_name)
    process.add_fg(photo_name)
    photo = open(new_photo_name, 'rb')
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo)
    photo.close()
    if os.path.exists(photo_name):
        os.remove(photo_name)
    if os.path.exists(new_photo_name):
        os.remove(new_photo_name)
    db.add_process(user_id)


def start(update, context):
    db.start_put(str(update.effective_chat.id))
    context.bot.send_message(chat_id=update.effective_chat.id, text="خوش آمدید\nاین ربات کاری است از بسیج دانشجویی داشگاه شهید باهنر کرمان\nبرای حمایت از ما در کانال ما عضو شوید.\n@bdbahonar")
    context.bot.send_message(chat_id=update.effective_chat.id, text="برای ادامه عکس مورد نظر خود را برای ربات بفرستید.\nهمچنین می توانید نظرات خود را از طریق ربات برای ما ارسال کنید.")


def ex_message(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="پیام دریافت شده معتبر نیست.\nخواهشمندیم عکس مورد نظر خود را به صورت photo و با سایز مناسب به ربات ارسال کنید.")


def message(update, context):
    user_id = str(update.effective_chat.id)
    text = update.message.text
    db.save_message(user_id, text)
    context.bot.send_message(chat_id=user_id, text="با تشکر\nنظر شما ثبت شد و به اطلاع تیم پشتیبانی رسید.")


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
