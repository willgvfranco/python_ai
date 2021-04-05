from scraper import html_scraper, scrap_them_all
from utils import preprocess, preprocess_lematize
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# response = requests.get(global_url)
# data = response.content
# soup = BeautifulSoup(data, features="xml",
#  from_encoding='utf-8')


global_url = "http://www.olharalerta.com.br/noticias/"
news_container = "ul.lista-noticias"
news_url = "a"
news_regex = ""

feed_content = ""
url_list = html_scraper(global_url, news_container, news_url)
article_list = scrap_them_all(url_list[0:4])
for article in article_list:
    feed_content += article['description']

formatted_feed_content = preprocess(feed_content)


wordcloud = WordCloud().generate(formatted_feed_content)

plt.figure(figsize=(20, 20))
plt.axis('off')
plt.imshow(wordcloud)
wordcloud.to_file("teste.png")
