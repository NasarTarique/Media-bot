import tweepy
import json
import datetime

User_list =['elonmusk']
client = open('client_secret.json',)
client_dictionary = json.load(client)
auth = tweepy.OAuthHandler(client_dictionary['consumer_key'], client_dictionary['consumer_secret'])
api = tweepy.API(auth)
str = ''
count =0
today = datetime.datetime.utcnow().date()
print(today)
yesterday = today - datetime.timedelta(days=1)
for user in User_list:
    status_list = api.user_timeline(user)
    while True:
        x=0
        status=status_list[0]
        x+=1
        print(status.created_at)
        if status.created_at<yesterday:
            str = str + status.text+'\n'
            count += 1

    str = str+'\n'

print(str)

