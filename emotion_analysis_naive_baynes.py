import nltk

base = [('eu sou admirada por muitos', 'alegria'),
        ('me sinto completamente amado', 'alegria'),
        ('amar e maravilhoso', 'alegria'),
        ('estou me sentindo muito animado novamente', 'alegria'),
        ('eu estou muito bem hoje', 'alegria'),
        ('que belo dia para dirigir um carro novo', 'alegria'),
        ('o dia est� muito bonito', 'alegria'),
        ('estou contente com o resultado do teste que fiz no dia de ontem', 'alegria'),
        ('o amor e lindo', 'alegria'),
        ('nossa amizade e amor vai durar para sempre', 'alegria'),
        ('estou amedrontado', 'medo'),
        ('ele esta me ameacando a dias', 'medo'),
        ('isso me deixa apavorada', 'medo'),
        ('este lugar e apavorante', 'medo'),
        ('se perdermos outro jogo seremos eliminados e isso me deixa com pavor', 'medo'),
        ('tome cuidado com o lobisomem', 'medo'),
        ('se eles descobrirem estamos encrencados', 'medo'),
        ('estou tremendo de medo', 'medo'),
        ('eu tenho muito medo dele', 'medo'),
        ('estou com medo do resultado dos meus testes', 'medo')]

stopwords = nltk.corpus.stopwords.words('portuguese')
stopwords += ['a', 'agora', 'algum', 'alguma', 'aquele', 'aqueles', 'de', 'deu', 'do', 'e', 'estou', 'esta', 'esta',
              'ir', 'meu', 'muito', 'mesmo', 'no', 'nossa', 'o', 'outro', 'para', 'que', 'sem', 'talvez', 'tem', 'tendo',
              'tenha', 'teve', 'tive', 'todo', 'um', 'uma', 'umas', 'uns', 'vou']


# def remove_stopwords(text):
#     sentences = []
#     for (words, emotion) in text:
#         semstop = [p for p in words.split() if p not in stopwords]
#         sentences.append((semstop, emotion))
#     return sentences


# print(remove_stopwords(base))


def apply_stemmer(text):
    stemmer = nltk.stem.RSLPStemmer()
    stemming = []
    for (words, emotion) in text:
        ind_stemming = [str(stemmer.stem(p))
                        for p in words.split() if p not in stopwords]
        stemming.append((ind_stemming, emotion))
    return stemming


sentences_stemming = apply_stemmer(base)
print(apply_stemmer(base))


# Take all words and put on an array together
def search_words(sentences):
    all_words = []
    for (words, emotion) in sentences:
        all_words.extend(words)

    frequency = nltk.FreqDist(all_words)
    unique_words = frequency.keys()
    return unique_words


unique_words = search_words(sentences_stemming)


def extract_words(document):
    doc = set(document)
    characteristics = {}
    for words in unique_words:
        characteristics['%s' % words] = (words in doc)
    return characteristics


basecompleta = nltk.classify.apply_features(extract_words, sentences_stemming)
# print(basecompleta)


classificador = nltk.NaiveBayesClassifier.train(basecompleta)
# print(classificador.labels())
# print(classificador.show_most_informative_features(10))


teste = "Estou feliz"
testestemming = []
stemmer = nltk.stem.RSLPStemmer()
for (words) in teste.split():
    comstem = [p for p in words.split()]
    testestemming.append(str(stemmer.stem(comstem[0])))
# print(testestemming)

novo = extract_words(testestemming)
# print(novo)
# print(classificador.classify(novo))

distribuicao = classificador.prob_classify(novo)
for classe in distribuicao.samples():
    print("%s: %f" % (classe, distribuicao.prob(classe)))
