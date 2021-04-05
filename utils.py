from bs4 import BeautifulSoup
import re
import nltk
import string
# nltk.download('punkt')
# nltk.download('stopwords')
import spacy


def html_clear(text):
    if text == '':
        return ''
    return BeautifulSoup(text, 'html5lib').get_text()


def preprocess(text):
    text = re.sub('\s+', ' ', text)
    formatted_text = text.lower()
    tokens = []
    stopwords = nltk.corpus.stopwords.words('portuguese')
    for token in nltk.word_tokenize(formatted_text):
        tokens.append(token)
    tokens = [
        palavra for palavra in tokens if palavra not in stopwords and palavra not in string.punctuation]
    formatted_text = ' '.join([str(elemento)
                               for elemento in tokens if not elemento.isdigit()])

    return formatted_text


def preprocess_lematize(text):
    formatted_text = text.lower()
    text = re.sub('\s+', ' ', text)

    pln = spacy.load("pt_core_news_sm")

    document = pln(text)
    tokens = []
    stopwords = nltk.corpus.stopwords.words('portuguese')
    for token in document:
        tokens.append(token.lemma_)
    tokens = [
        palavra for palavra in tokens if palavra not in stopwords and palavra not in string.punctuation]
    formatted_text = ' '.join([str(elemento)
                               for elemento in tokens if not elemento.isdigit()])

    return formatted_text


def strings_concatenate(article_list):
    feed_content = ""
    for article in article_list:
        feed_content += article['description']

    return feed_content
