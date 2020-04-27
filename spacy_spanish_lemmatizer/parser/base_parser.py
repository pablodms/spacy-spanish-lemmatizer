import json
import os
from ..config import Config
import sys


class BaseParser:

    COMMON_RULES = {}
    COMMON_EXCEPTIONS = {}

    def __init__(self):

        with open(Config.COMMON_RULES, encoding="utf-8") as json_file:
            self.COMMON_RULES = json.load(json_file)

        with open(Config.COMMON_EXCEPTIONS, encoding="utf-8") as json_file:
            self.COMMON_EXCEPTIONS = json.load(json_file)

    def _clean_directory(self, directory):
        for file in os.listdir(directory):
            if not file.startswith('.'):
                path = os.path.join(directory, file)
                if os.path.isfile(path):
                    os.unlink(path)

    def clean(self):
        sys.stdout.write("Cleaning temporary files...\n")
        self._clean_directory(Config.TEMP_FOLDER)

    def download(self):
        raise Exception("Not implemented")

    def parse(self):
        raise Exception("Not implemented")

    def process(self):
        self.download()
        self.parse()
        self.clean()

    def reset(self):
        sys.stdout.write("Cleaning data...\n")
        self._clean_directory(Config.DATA_FOLDER)
