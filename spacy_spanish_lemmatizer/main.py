from .lemmatizer import Lemmatizer
from spacy.language import Language

class SpacyCustomLemmatizer(object):
    def __call__(self, doc):
        lemmatizer = Lemmatizer()
        for token in doc:
            token.lemma_ = lemmatizer(token.text, token.pos_, token.lemma_)
        return doc

@Language.factory("spanish_lemmatizer")
def create_spanish_lemmatizer(nlp, name):
  return SpacyCustomLemmatizer()
