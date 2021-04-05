from scraper import html_scraper

global_url = "https://www.agenciadanoticia.com.br/noticias/"
news_container = "ul.listaNoticiasEditoria"
news_url = "li > a"
news_regex = ""

article_list = html_scraper(global_url, news_container, news_url)
article_list = [
    'http://www.afolhadomedionorte.com.br/social-em-acao-assistencia-social-de-nova-olimpia-realiza-entrega-de-kits-de-pascoa/']
