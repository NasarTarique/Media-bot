from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Updater, Dispatcher, CommandHandler, CallbackContext
from threading import Thread
from queue import Queue
import datetime
import os 
import news

TOKEN = os.environ.get('TOKEN')

app = Flask(__name__)
update_queue = Queue()
bot = Bot(TOKEN)
updater = Updater(TOKEN, use_context=True)
j = updater.job_queue
listofjobs = []


start_txt = ''' Hello ! This Media bot will send you  news update everyday so you can get the latest news right on telegram .
                type /help for the commands.
            '''

hlp_txt = '''
            /startNews : get daily news updates
            /stopNews : stop getting daily news updates
            NOTE: You will get updates at everyday at 11 am (UTC)
          '''


def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.message.chat.id,text = start_txt)


def help(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.message.chat.id, text=hlp_txt)


def callback_news(context: CallbackContext):
    txt = news.get_news()
    context.bot.send_message(chat_id=context.job.context, text=txt)


def start_news(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.message.chat.id,
                             text='You will now get top news headlines daily.\n Use /stopNews to stop getting updates')
    job_dict = dict(chat_id=update.message.chat.id)
    job_dict['news_job'] = j.run_daily(callback_news, time= datetime.time(11,0,0), context=update.message.chat.id)
    listofjobs.append(job_dict)


def stop_news(update: Update, context: CallbackContext):
    for job_dict in listofjobs:
        if job_dict['chat_id'] == update.message.chat.id:
            job_dict['news_job'].schedule_removal()
            update.message.reply_text("The daily update has been scheduled for removal")


dispatcher = Dispatcher(bot, update_queue, job_queue=j, use_context=True)
dispatcher.add_handler(CommandHandler('help', help, pass_update_queue=True))
dispatcher.add_handler(CommandHandler('start', start, pass_update_queue=True))
dispatcher.add_handler(CommandHandler('startNews', start_news, pass_job_queue=True))
dispatcher.add_handler(CommandHandler('stopNews', stop_news, pass_job_queue=True, pass_chat_data=True))
j.set_dispatcher(dispatcher)
thread = Thread(target=dispatcher.start, name='dispatcher')
thread.start()
thread2 = Thread(target=j.start(), name='j')
thread2.start()


@app.route('/')
def index():
    return '.'


@app.route('/{}'.format(TOKEN), methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    update_queue.put(update)
    return 'ok'


if __name__ == '__main__':
    app.run(debug=True)
    j.start()
    dispatcher.start()
