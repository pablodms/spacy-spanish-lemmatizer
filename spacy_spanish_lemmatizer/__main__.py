import sys
from .parser.parser_factory import ParserFactory

if __name__ == "__main__":
    argv_len = len(sys.argv)

    if argv_len == 3 and sys.argv[1] == "download":
        parser = ParserFactory.get(sys.argv[2])
        parser.process()
    else:
        sys.stdout.write(
            """ Usage: python -m spacy_spanish_lemmatizer download wiki """
        )
