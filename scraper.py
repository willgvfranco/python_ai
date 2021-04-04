from bs4 import BeautifulSoup
import feedparser
from utils import html_clear
from goose3 import Goose
import requests
import re


def xml_scraper(global_url):
    response = feedparser.parse(global_url)
    article_list = []

    for news in response['entries']:
        description = html_clear(news['summary'])
        article_list.append({
            'title': news['title'],
            'pub_date': news['published_parsed'],
            'link': news['link'],
            'description': description})

    return article_list


global_url = "https://www.agenciadanoticia.com.br/noticias/"
news_container = "ul.listaNoticiasEditoria"
news_url = "li > a"
news_regex = ""


def html_scraper(global_url, news_container, news_url, news_regex=None):

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
    }
    response = requests.get(global_url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser',
                         from_encoding='utf-8')

    article_list = []
    if(news_container.startswith('re=')):
        container = soup.findAll(href=re.compile(
            news_container.replace("re=", "", 1)))
    elif('.' in news_container):
        formatted_container = news_container.split(".")
        container = soup.findAll(
            formatted_container[0], class_=formatted_container[1])
    else:
        container = soup.findAll(news_container)

    new_container = []
    for news in container:
        multiple_container = news.findAll('a')
        if(multiple_container):
            for child in multiple_container:
                new_container.append(child)
    if(new_container):
        container = new_container

    for news in container:
        md_url = news.select_one(news_url)
        if(not md_url):
            if('href' in news.attrs):
                fn_url = news.attrs['href']
            else:
                continue
        else:
            md2_url = news.select_one(news_url)['href']
            if('javascript' in md2_url):
                continue
            fn_url = news.select_one(news_url)['href']

        if(news_regex):
            fn_url = news_regex + fn_url
        if('¬' in fn_url):
            fn_url = fn_url.replace("¬", "&not", 1)

        article_list.append(fn_url)
    return article_list


article_list = html_scraper(global_url, news_container, news_url)
article_list = [
    'http://www.afolhadomedionorte.com.br/social-em-acao-assistencia-social-de-nova-olimpia-realiza-entrega-de-kits-de-pascoa/']


def scrap_one(article_list):
    g = Goose()
    art = g.extract(article_list)
    noticia_final = ({
        "title": art.title,
        "link": art.final_url,
        "description": art.cleaned_text,
        "data": art.publish_datetime_utc
    })
    return noticia_final


# a = scrap_one(article_list[0])
# print(a)

# scrap_one(global_url)
