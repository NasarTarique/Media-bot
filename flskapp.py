from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Updater, Dispatcher, CommandHandler, CallbackContext
from threading import Thread
from queue import Queue
from config import TOKEN


def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.message.chat.id,
                             text='Hello ! Use the /timer command ')


def callback_alarm(context: CallbackContext):
    context.bot.send_message(chat_id=context.job.context, text='BEEP')


def callback_timer(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.message.chat.id,
                             text='setting timer for 1 minute')
    context.job_queue.run_once(callback_alarm, 60, context=update.message.chat.id)


app = Flask(__name__)
update_queue = Queue()
bot = Bot(TOKEN)
updater = Updater(TOKEN, use_context=True)
j = updater.job_queue
dispatcher = Dispatcher(bot, update_queue, job_queue=j, use_context=True)
timer_handler = CommandHandler('timer', callback_timer,pass_job_queue=True )
dispatcher.add_handler(timer_handler)
updater.dispatcher.add_handler(CommandHandler('start', start,pass_update_queue=True))

thread = Thread(target=dispatcher.start, name='dispatcher')
thread.start()


@app.route('/')
def index():
    return '.'


@app.route('/{}'.format(TOKEN), methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True))
    update_queue.put(update)
    return 'ok'


if __name__ == '__main__':
    app.run(debug=True)
