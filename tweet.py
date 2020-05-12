import tweepy
import json


client = open('client_secret.json',)
client_dictionary = json.load(client)
auth = tweepy.OAuthHandler(client_dictionary['consumer_key'], client_dictionary['consumer_secret'])
api = tweepy.API(auth)