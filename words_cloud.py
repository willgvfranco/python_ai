import requests
from bs4 import BeautifulSoup
import json
import feedparser
from goose3 import Goose

global_url = "https://g1.globo.com/rss/g1/"
# response = requests.get(global_url)
# data = response.content
# soup = BeautifulSoup(data, features="xml",
#  from_encoding='utf-8')

d = feedparser.parse(global_url)
g = Goose()
article_list = []


print(teste)
# for news in d['entries']:
#     print(news['link'])
#     article_list.append(g.extract(news['link']))

# print(article_list)
# print(article_list)

# feed_content = ''
# for articles in articles_all:
#     feed_content += article['key']
