


import spacy

#en_core_web_sm
#es_core_news_md

try:
    spacy.load('en_core_web_sm')
    spacy.load('es_core_news_md')
    print('Has already installed spacy models')
except OSError:
    print('Downloading language model for the spaCy POS tagger\n'
        "(don't worry, this will only happen once)")
    from spacy.cli import download
    download('en_core_web_sm')
    download('es_core_news_md')