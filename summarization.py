import re
import nltk
import heapq
# nltk.download('punkt')
# nltk.download('stopwords')
from utils import preprocess_lematize
import os
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.luhn import LuhnSummarizer


def summarizer_sumy(text):
    parser = PlaintextParser.from_string(
        text.cleaned_text, Tokenizer('portuguese'))
    sumarizador = LuhnSummarizer()
    resumo = sumarizador(parser.document, 5)
    return resumo


def summarization_freq(original):
    # lista_palavras = nltk.word_tokenize(original)
    list_sentences = nltk.sent_tokenize(original)
    formatado = preprocess_lematize(original)
    frequencia_palavras = nltk.FreqDist(nltk.word_tokenize(formatado))
    # for a in frequencia_palavras:
    #     print(a, frequencia_palavras[a])

    frequencia_palavras_relativa = frequencia_palavras.copy()
    frequencia_maxima = max(frequencia_palavras.values())

    for palavra in frequencia_palavras.keys():
        frequencia_palavras_relativa[palavra] = (
            frequencia_palavras[palavra] / frequencia_maxima)

    # for a in frequencia_palavras_relativa:
    #     print(a, frequencia_palavras_relativa[a])

    notas_sentencas = {}
    for sentenca in list_sentences:
        for palavra in nltk.word_tokenize(sentenca.lower()):
            if palavra in frequencia_palavras_relativa.keys():
                if sentenca not in notas_sentencas.keys():
                    notas_sentencas[sentenca] = frequencia_palavras_relativa[palavra]
                else:
                    notas_sentencas[sentenca] += frequencia_palavras_relativa[palavra]

    sentencas_ordenadas = dict(sorted(notas_sentencas.items(),
                                      key=lambda item: item[1], reverse=True))
    quantity = round(0.3 * len(list_sentences))
    quantity = 1 if quantity < 1 else quantity
    best_sentencas = heapq.nlargest(
        quantity, notas_sentencas, key=notas_sentencas.get)
    # data = pd.DataFrame.from_dict(
    #     frequencia_palavras, orient='index').sort_values(frequencia_palavras[0], ascending=False)
    # print(data)

    return list_sentences, best_sentencas


def save_summary(title, list_sentences, best_sentencas):
    HTML_TEMPLATE = """<html>
    <head>
        <title>{0}</title>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    </head>
    <body>{1}</body>

    </html>"""
    text = ''
    for i in list_sentences:
        if i in best_sentencas:
            text += str(i).replace(i, f"<mark>{i}</mark>")
        else:
            text += i

    arquivo = open(os.path.join(title + '.html'), 'wb')
    html = HTML_TEMPLATE.format(title + ' - Resumo', text)
    arquivo.write(html.encode('utf-8'))
    arquivo.close()
# formatted_text = preprocesamento(texto_original)
# print(sumarization_by_freq(texto_original, 5))
