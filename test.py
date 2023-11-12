import datetime
from telegram import Update, Message
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
TOKEN = '6226428057:AAFfBofQJzEyeN5sqOjuH0x4LtY9oVpUGyc'

# Dictionary to store join dates of members
member_join_dates = {}

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hello! I am your group management bot.')

def days_left(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id

    if user_id not in member_join_dates:
        update.message.reply_text('You have not joined the group yet.')
        return

    join_date = member_join_dates[user_id]
    current_date = datetime.datetime.now()
    remaining_days = (join_date + datetime.timedelta(days=30) - current_date).days

    if remaining_days > 0:
        update.message.reply_text(f'Days left for removal: {remaining_days}')
    else:
        update.message.reply_text('Your time has come. You will be removed from the group.')

def join_handler(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    join_date = datetime.datetime.now()
    member_join_dates[user_id] = join_date

def main() -> None:
    updater = Updater(TOKEN)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("days", days_left))
    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, join_handler))

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()
