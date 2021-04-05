import re
import nltk
import heapq
# nltk.download('punkt')
# nltk.download('stopwords')
from utils import preprocess_lematize

# texto_original = """A inteligência artificial é a inteligência similar à humana.
#                     Definem como o estudo de agente artificial com inteligência.
#                     Ciência e engenharia de produzir máquinas com inteligência.
#                     Resolver problemas e possuir inteligência.
#                     Relacionada ao comportamento inteligente.
#                     Construção de máquinas para raciocinar.
#                     Aprender com os erros e acertos.
#                     Inteligência artificial é raciocinar nas situações do cotidiano."""


def sumarization_freq(original, quantity):
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
    best_sentencas = heapq.nlargest(
        quantity, notas_sentencas, key=notas_sentencas.get)
    # data = pd.DataFrame.from_dict(
    #     frequencia_palavras, orient='index').sort_values(frequencia_palavras[0], ascending=False)
    # print(data)

    return list_sentences, best_sentencas


# formatted_text = preprocesamento(texto_original)
# print(sumarization_by_freq(texto_original, 5))
