from scraper import html_scraper, scrap_them_all
from utils import preprocess, preprocess_lematize, strings_concatenate
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# response = requests.get(global_url)
# data = response.content
# soup = BeautifulSoup(data, features="xml",
#  from_encoding='utf-8')


def generate_wordcloud(article_list):
    feed_content = ""
    feed_content = strings_concatenate(article_list)

    formatted_feed_content = preprocess(feed_content)
    wordcloud = WordCloud().generate(formatted_feed_content)

    plt.figure(figsize=(20, 20))
    plt.axis('off')
    plt.imshow(wordcloud)
    wordcloud.to_file("teste.png")
