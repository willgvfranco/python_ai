from bs4 import BeautifulSoup
import re
import nltk
import string
# nltk.download('punkt')
# nltk.download('stopwords')
import spacy
from spacy.lang.pt.stop_words import STOP_WORDS

pln = spacy.load('pt_core_news_sm')


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


def preprocessamento(texto):
    texto = texto.lower()
    doc = pln(texto)

    lista = []
    for token in doc:
        # lista.append(token.text)
        lista.append(token.lemma_)

    lista = [palavra for palavra in lista if palavra not in STOP_WORDS and palavra not in string.punctuation]
    lista = ' '.join([str(elemento) for elemento in lista if not elemento.isdigit()])

    return lista


def padronizar_base_dados(raw):
    base_dados = pd.read_csv(raw, encoding='utf-8')
    base_dados['texto'] = base_dados['texto'].apply(preprocessamento)
    base_dados_csv = []
    for texto, emocao in zip(base_dados['texto'], base_dados['emocao']):
        if emocao == 'alegria':
            dic = ({'ALEGRIA': True, 'MEDO': False})
        elif emocao == 'medo':
            dic = ({'ALEGRIA': False, 'MEDO': True})

        base_dados_csv.append([texto, dic.copy()])

    return base_dados_csv


def strings_concatenate(article_list):
    feed_content = ""
    for article in article_list:
        feed_content += article['description']

    return feed_content
