import spacy
import pandas as pd
import string
import spacy
import random
import seaborn as sns
import numpy as np
import re
from spacy.lang.pt.stop_words import STOP_WORDS
import matplotlib.pyplot as plt

pln = spacy.load('pt_core_news_sm')

base_treinamento = pd.read_csv('./lessons/Train50.csv', delimiter=';')
base_treinamento.drop(['id', 'tweet_date', 'query_used'], axis=1, inplace=True)
base_teste = pd.read_csv('./lessons/Test.csv', delimiter=';')
base_teste.drop(['id', 'tweet_date', 'query_used'], axis=1, inplace=True)


def preprocessamento_twitter(texto):
    # Letras minúsculas
    texto = texto.lower()

    # Nome do usuário
    texto = re.sub(r"@[A-Za-z0-9$-_@.&+]+", ' ', texto)

    # URLs
    texto = re.sub(r"https?://[A-Za-z0-9./]+", ' ', texto)

    # Espaços em branco
    texto = re.sub(r" +", ' ', texto)

    # risada
    # texto = re.sub(r"\b(?:a{0,2}h{1,2}a{0,2}){2,}h?\b", 'emocaopositiva', texto)

    # risada
    # texto = re.sub(r"[k]{5,}", 'emocaopositiva', texto)

    # Emoticons
    lista_emocoes = {':)': 'emocaopositiva',
                     ':d': 'emocaopositiva',
                     ':(': 'emocaonegativa',
                     '=)': 'emocaopositiva',
                     '=(': 'emocaonegativa',
                     '=/': 'emocaonegativa',
                     ':/': 'emocaonegativa'
                     }

    for emocao in lista_emocoes:
        texto = texto.replace(emocao, lista_emocoes[emocao])

    doc = pln(texto)
    lista = []
    for token in doc:
        # lista.append(token.text)
        lista.append(token.lemma_)

    lista = [palavra for palavra in lista if palavra not in STOP_WORDS and palavra not in string.punctuation]
    lista = ' '.join([str(elemento) for elemento in lista if not elemento.isdigit()])

    return lista


def adaptar_bd_twitter(base_dados):
    # base_dados = pd.read_csv(raw, encoding='utf-8')
    # base_dados['texto'] = base_dados['texto'].apply(preprocessamento)

    base_dados_final = []
    for texto, emocao in zip(base_dados['tweet_text'], base_dados['sentiment']):
        if emocao == 1:
            dic = ({'POSITIVO': True, 'NEGATIVO': False})
        elif emocao == 0:
            dic = ({'POSITIVO': False, 'NEGATIVO': True})

        base_dados_final.append([texto, dic.copy()])

    return base_dados_final


base_treinamento['tweet_text'] = base_treinamento['tweet_text'].apply(preprocessamento_twitter)
# base_teste['tweet_text'] = base_teste['tweet_text'].apply(preprocessamento_twitter)
base_dados_treinamento_final = adaptar_bd_twitter(base_treinamento)
# base_dados_teste_final = adaptar_bd_twitter(base_teste)

modelo = spacy.blank('pt')
categorias = modelo.create_pipe("textcat")
categorias.add_label("POSITIVO")
categorias.add_label("NEGATIVO")
modelo.add_pipe(categorias)
historico = []

modelo.begin_training()
for epoca in range(20):
    random.shuffle(base_dados_treinamento_final)
    losses = {}
    for batch in spacy.util.minibatch(base_dados_treinamento_final, 512):
        textos = [modelo(texto) for texto, entities in batch]
        annotations = [{'cats': entities} for texto, entities in batch]
        modelo.update(textos, annotations, losses=losses)
        historico.append(losses)
    if epoca % 5 == 0:
        print(losses)

historico_loss = []
for i in historico:
    historico_loss.append(i.get('textcat'))

historico_loss = np.array(historico_loss)
print(historico_loss)

plt.plot(historico_loss)
plt.title('Progressão do erro')
plt.xlabel('Batches')
plt.ylabel('Erro')

modelo.to_disk("./modelo1")