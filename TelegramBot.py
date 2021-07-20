'''
import telegram
from telegram.ext import CallbackContext, Updater, CommandHandler, CallbackQueryHandler
from telegram.ext import Filters
from telegram.ext import MessageHandler


class TelegramBot:
    def __init__(self, token):
        self.token = token
        updater = Updater(token, use_context=True)

        queue_updater = updater.job_queue
        dp = updater.dispatcher
        handler = MessageHandler(Filters.text | Filters.command, self.messageHandler)
        dp.add_handler(handler)
        updater.start_polling(timeout=0)
        updater.idle()

    def messageHandler(self, update, context):
        pass
'''