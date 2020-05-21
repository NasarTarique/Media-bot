import logging
import os
from newsapi import NewsApiClient


NEWS_API_KEY = os.environ.get('NEWS_API_KEY')

logging.basicConfig(filename="news.log", level=logging.DEBUG)
logger = logging.getLogger()


def get_news():
    newsapi = NewsApiClient(api_key=NEWS_API_KEY)
    headlines = newsapi.get_top_headlines(country='in')
    strn = 'News:\n'
    for x in range(9):
        try:
            test_str = strn+'\n'+headlines['articles'][x]['title']+'\n'+headlines['articles'][x]['description']+'\n'+headlines['articles'][x]['url']+'\n\n '
        except TypeError as err:
            logger.info("Null values in articles dictionary")
        else:
            strn = strn+'\n'+headlines['articles'][x]['title']+'\n'+headlines['articles'][x]['description']+'\n'+headlines['articles'][x]['url']+'\n\n '

    return strn

