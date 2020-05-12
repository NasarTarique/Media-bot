from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Updater, Dispatcher, CommandHandler, CallbackContext
from threading import Thread
from queue import Queue
from config import TOKEN
import news

app = Flask(__name__)
update_queue = Queue()
bot = Bot(TOKEN)
updater = Updater(TOKEN, use_context=True)
j = updater.job_queue
listofjobs = []


def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.message.chat.id,
                             text='''Hello ! This Socail Media bot brings you news update daily and also posts from 
                             insta,twitter and youtube by the users you have selected  if the users you have selected 
                              have uploaded anything in the past 24 hrs you will see their posts along with news in 
                              telegram saving you from endless scrolling and addiction of social media . you will get 
                              updates only once every 24 hours . 
                              type /help to know more ''')


def help(update: Update, context: CallbackContext):
    txt = '''(Note : you will get posts from insta ,twitter and youtube only from the users you have selected not the 
    ones you follow or are subscribed to) \n commands:\n /startAll : Get updates of last 24 hrs from insta, twitter , 
    youtube and also get news daily \n/startNews : get only news updates\n /startInsta : Get updates only from 
    instagram \n /startTweet : get updates only from Twitter \n /startYT : get updates only from youtube\n /instaid [
    your username]: Add your instagram username \n /instapwd [password]: Add your insta password \n /tweetid [your 
    username]: Add your twiiter username\n /tweetpwd [password]:Add your twitter password \n /AddInstaUser [username  
    ]: Add the person whose insta post updates you want \n /AddTweetUser [username ] : Add the twitter handle whose 
    tweets you want to see  \n /AddYtSub [channel_name]: Add the youtube channel name whose vid updates you want\n 
    /RemoveTweetUser [username ]: stop the tweet update from this user \n /RemoveInstaUser [username] : stop post 
    update from this user \n /RemoveYtSub [username] : stop video updates from this channel\n /stopALL : stop the daily 
    updates \n /stopInsta : stops instagram updates\n /stopTweet : stop twitter updates \n /stopYt : stop youtube 
    updates \n /stopNews :stop news updates '''
    context.bot.send_message(chat_id=update.message.chat.id, text=txt)


def callback_news(context: CallbackContext):
    txt = news.get_news()
    context.bot.send_message(chat_id=context.job.context, text=txt)


def start_news(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.message.chat.id,
                             text='You will now get top news headlines daily.\n Use /stopNews to stop getting updates')
    job_dict = dict(chat_id=update.message.chat.id)
    job_dict['news_job'] = j.run_repeating(callback_news, interval=300, first=0, context=update.message.chat.id)
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
