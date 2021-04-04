from bs4 import BeautifulSoup


def html_clear(text):
    if text == '':
        return ''
    return BeautifulSoup(text, 'html5lib').get_text()
