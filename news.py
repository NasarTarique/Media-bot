from newsapi import NewsApiClient
from config import NEWS_API_KEY


def get_news():
    newsapi = NewsApiClient(api_key=NEWS_API_KEY)
    headlines = newsapi.get_top_headlines(country='in')
    str ='News:\n'
    for x in range(11):
        str = str+headlines['articles'][x]['title']+'\n'+headlines['articles'][x]['description']+'\n'+headlines['articles'][x]['url']+'\n\n'
    return str


