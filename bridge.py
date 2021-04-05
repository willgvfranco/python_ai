from scraper import html_scraper, scrap_them_all
from utils import preprocess, preprocess_lematize, strings_concatenate
from word_cloud import generate_wordcloud
from summarization import summarization_freq, save_summary, summarizer_sumy
from goose3 import Goose


global_url = "http://www.olharalerta.com.br/noticias/"
news_container = "ul.lista-noticias"
news_url = "a"
news_regex = ""

# get article
g = Goose()
url = 'https://iaexpert.academy/2020/11/09/ia-preve-resultado-das-eleicoes-americanas/'
artigo_portugues = g.extract(url)


url_list = html_scraper(global_url, news_container, news_url)
article_list = scrap_them_all(url_list[0])


# Creating a HTML with summary from a text
list_freq, best_sentencas = summarization_freq(article_list['description'])
save_summary('teste', list_freq, best_sentencas)


# Summary with sumy
resumo = summarizer_sumy(artigo_portugues)
for i in resumo:
    print(i)
