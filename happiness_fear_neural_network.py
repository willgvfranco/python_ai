import spacy
import pandas as pd
import string
import spacy
import random
import seaborn as sns
import numpy as np

from spacy.lang.pt.stop_words import STOP_WORDS

from utils import preprocessamento, padronizar_base_dados

pln = spacy.load('pt_core_news_sm')

base_dados_final = padronizar_base_dados('./lessons/base_treinamento.txt')


def create_neural_model():
    rede_neural = spacy.blank('pt')
    categorias = rede_neural.create_pipe('textcat')
    categorias.add_label('ALEGRIA')
    categorias.add_label('MEDO')
    rede_neural.add_pipe(categorias)

    return rede_neural


historico = []

rede_neural.begin_training()
for epoca in range(1000):
    random.shuffle(base_dados_final)
    losses = {}
    for batch in spacy.util.minibatch(base_dados_final, 30):
        textos = [rede_neural(texto) for texto, entities in batch]
        annotations = [{'cats': entities} for texto, entities in batch]
        rede_neural.update(textos, annotations, losses=losses)
    if epoca % 100 == 0:
        print(losses)
        historico.append(losses)

rede_neural.to_disk("./lessons/modelo")
