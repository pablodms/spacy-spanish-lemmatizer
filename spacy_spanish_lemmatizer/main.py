from .lemmatizer import Lemmatizer


class SpacyCustomLemmatizer(object):
    def __call__(self, doc):
        lemmatizer = Lemmatizer()
        for token in doc:
            token.lemma_ = lemmatizer(token.text, token.pos_, token.lemma_)
        return doc
