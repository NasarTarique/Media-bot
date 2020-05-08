from newsapi import NewsApiClient
from config import NEWS_API_KEY
import datetime

newsapi = NewsApiClient(api_key=NEWS_API_KEY)

todays_date = datetime.datetime.utcnow().date()
yesterdays_date  = todays_date - datetime.timedelta(days=1)
top_headlines = newsapi.get_everything(sources='bbc-news', language='en', from_param=yesterdays_date, to=todays_date, sort_by='relevancy')
