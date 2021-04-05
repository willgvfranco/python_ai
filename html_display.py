from IPython.core.display import HTML
texto = ''


def display_bests_html(lista_sentencas, bests):

    display(HTML(f'<h1>Summary</h1>'))
    for sentenca in lista_sentencas:
        #texto += sentenca
        if sentenca in melhores_sentencas:
            texto += str(sentenca).replace(sentenca,
                                           f"<mark>{sentenca}</mark>")
        else:
            texto += sentenca
    display(HTML(f"""{texto}"""))
