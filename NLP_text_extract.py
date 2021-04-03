from goose3 import Goose
from NLP_summarization_by_freq import sumarization_by_freq, preprocess

g = Goose()
url = 'https://opresenterural.com.br/agricultores-de-santa-catarina-buscam-inovacoes-para-aumentar-a-renda-no-meio-rural/'
article = g.extract(url)


formatted_article = preprocess(article.cleaned_text)
# print(formatted_article)

list_sentences, best_sentencas = sumarization_by_freq(article.cleaned_text, 5)

for frase in best_sentencas:
    print(f"{frase}")

a = 1
