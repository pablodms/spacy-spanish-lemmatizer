from .base_parser import BaseParser
from .wiki_parser import WikiParser


class ParserFactory:
    @staticmethod
    def get(type):
        if type == "wiki":
            return WikiParser()
        else:
            return BaseParser()
