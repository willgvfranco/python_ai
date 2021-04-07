import spacy
import pandas as pd
import string
import spacy
import random
import seaborn as sns
import numpy as np

from spacy.lang.pt.stop_words import STOP_WORDS

from utils import preprocessamento

julia = spacy.load("./lessons/modelo")

texto_positivo = "eu gosto de feijão"
texto_negativo = "medo de você"

texto_positivo = preprocessamento(texto_positivo)
texto_negativo = preprocessamento(texto_negativo)

previsao = julia(texto_positivo)
previsao2 = julia(texto_negativo)