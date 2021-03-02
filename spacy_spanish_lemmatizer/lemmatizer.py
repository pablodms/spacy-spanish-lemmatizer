import json
from .config import Config


class Lemmatizer:

    def __init__(self):
        self.__lookup_table = {}
        self.__rules = {}
        with open(Config.OUTPUT_FILE, encoding="utf-8") as json_file:
            self.__lookup_table = json.load(json_file)
        with open(Config.COMMON_RULES, encoding="utf-8") as json_file:
            self.__rules = json.load(json_file)

    def __call__(self, token, pos, old_lemma):
        pos = pos.lower()
        token = token.lower()
        # hard lookup
        lookup_data = self.__lookup_table.get(pos, {})
        lookup = lookup_data.get(token, None)
        if lookup:
            return lookup
        # general rules
        current_rules = self.__rules.get(pos, {})
        for old, new in current_rules.items():
            if token.endswith(old):
                return token[: len(token)-len(old)] + new
        # Return the original token if it is a preposition or
        # if the original lemmatizer has not been executed
        if pos == "adp" or not old_lemma:
           return token
        # use lemma from spaCy
        return old_lemma.lower()

