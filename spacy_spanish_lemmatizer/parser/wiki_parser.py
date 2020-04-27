# coding: utf8
from .base_parser import BaseParser
import bz2
import json
import os
import re
import urllib.request
import xml.etree.ElementTree as ET
import sys
from ..config import Config


class WikiParser(BaseParser):

    """
    Builds Spanish lemmatizer based in latest Wiktionary dump file.
    """

    DERIVATIVE_ADJECTIVE_TAGS = [
        "f.adj2",
        "forma adjetivo",
        "forma adjetivo 2",
        "superlativo",
        "forma participio",
    ]

    DERIVATIVE_PRONOUN_TAGS = ["forma pronombre"]

    DERIVATIVE_NOUN_TAGS = [
        "f.s.p",
        "forma diminutivo",
        "forma sustantivo",
        "forma sustantivo plural",
        "forma_sustantivo plural ",
        "plural",
        "forma participio",
        "forma adjetivo",
        "forma adjetivo 2",
        "f.adj2",
    ]

    DERIVATIVE_VERB_TAGS = ["gerundio", "participio", "forma verbo", "f.v"]

    DERIVATIVE_ADVERB_TAGS = ["adverbio de sustantivo", "adverbio de adjetivo"]

    DUMP_URL = "https://dumps.wikimedia.org/eswiktionary/latest/eswiktionary-latest-pages-articles.xml.bz2"  # noqa

    SKIP_TITLES = [
        "MediaWiki:",
        "Plantilla:",
        "Wikcionario:",
        "Archivo:",
        "Categoría:",
        "Módulo:",
        "Apéndice:",
    ]

    def __init__(self):
        super(WikiParser, self).__init__()
        wikiFile = "eswiktionary-latest-pages-articles.xml"
        self.OUTPUT_LEMMA = Config.TEMP_FOLDER + os.sep + wikiFile
        self.COMPRESSED_LEMMA = Config.TEMP_FOLDER + os.sep + wikiFile + ".bz2"
        self.__results = {}
        self.__adjectives_irreg = {}
        self.__pronouns_irreg = {}
        self.__nouns_irreg = {}
        self.__verbs_irreg = {}
        self.__adverbs_irreg = {}
        self.__category_regex = re.compile(
            r"== ?\{\{([^}]+)\}\} ?=="
        )  # Matches nouns, verbs, adverbs categories
        self.__multiple_lang_regex = re.compile(
            r"\{\{([a-zA-Z]{2})(?:\|\||-)[a-zA-Z0-9]{1,2}\}\}"
        )  # Matches language tags like {{ES||1}}, {{ES-EN}}
        self.__lengua_regex = re.compile(
            r"== ?{{lengua\|([^}]+)}} ?=="
        )  # Matches language tags like == {{lengua|es}} ==
        self.__acception_regex = re.compile(
            r"\: ?{{([^}]+)}}"
        )  # Matches variations from base, like plurals or verb conjugations

    def __download_source(self):
        sys.stdout.write(
            "Downloading wiktionary dump from: "
            + self.DUMP_URL
            + " (it may take some time)\n"
        )
        urllib.request.urlretrieve(self.DUMP_URL, self.COMPRESSED_LEMMA)

    def __decompress_source(self):
        sys.stdout.write("Decompressing dump file: " + self.COMPRESSED_LEMMA + "\n")
        with open(self.OUTPUT_LEMMA, "wb") as new_file, bz2.BZ2File(
            self.COMPRESSED_LEMMA, "rb"
        ) as file:
            for data in iter(lambda: file.read(100 * 1024), b""):
                new_file.write(data)

    def __iterate_languages(self, text, regex, target_lang):
        match = regex.search(text)
        while match:
            start = match.end(0)
            cut = text[start:]
            next_match = regex.search(cut)
            language = match[1].lower()
            end = next_match.start(0) if next_match else len(cut)
            if language == target_lang:
                return self.__process_lang(cut[:end])
            text = cut[end:]
            match = regex.search(text)
        return []

    def __process_text(self, text, target_lang):

        lengua_match = self.__lengua_regex.search(text)
        if lengua_match:
            return self.__iterate_languages(
                text, self.__lengua_regex, target_lang
            )
        multiple_lang_match = self.__multiple_lang_regex.search(text)
        if multiple_lang_match:
            return self.__iterate_languages(
                text, self.__multiple_lang_regex, target_lang
            )
        return []

    """
    Generate entries for lemmatization
    """

    def __generate_lemmatization(self):
        sys.stdout.write("Generating lemmatization...\n")
        is_valid_word_regex = re.compile(r"^[\w-]+$")
        # Allow dashes and alpha chars in words
        for key, values in self.__results.items():
            if " " in key:
                continue

            is_noun = False
            is_adjective_form = False
            for value in values:
                tokens = value.split("|")
                # Check if considered term is a pure Noun
                if tokens[0].startswith("sustantivo"):
                    is_noun = True

                if len(tokens) > 1:
                    category = None
                    term = None
                    form = tokens[0] == "forma"

                    for token in tokens[1:]:
                        # Remove leading and ending whitespaces
                        token = token.strip()
                        if "tipo=" in token:
                            category = token.split("=")[1]
                        elif is_valid_word_regex.match(token):
                            term = token
                            break

                    if not term:
                        continue

                    # Prioritize first derivation found over next ones
                    if not self.__adjectives_irreg.get(key, None) and (
                        (form and category == "adjetivo")
                        or tokens[0] in self.DERIVATIVE_ADJECTIVE_TAGS
                    ):
                        is_adjective_form = True
                        self.__adjectives_irreg[key] = term
                    if not self.__pronouns_irreg.get(key, None) and (
                        (form and category == "pronombre")
                        or tokens[0] in self.DERIVATIVE_ADJECTIVE_TAGS
                    ):
                        self.__pronouns_irreg[key] = term
                    if not self.__nouns_irreg.get(key, None) and (
                        (form and category == "sustantivo")
                        or tokens[0] in self.DERIVATIVE_NOUN_TAGS
                    ):
                        self.__nouns_irreg[key] = term
                    if not self.__verbs_irreg.get(key, None) and (
                        (form and category == "verbo")
                        or tokens[0] in self.DERIVATIVE_VERB_TAGS
                    ):
                        self.__verbs_irreg[key] = term
                    if not self.__adverbs_irreg.get(key, None) and (
                        (form and category == "adverbio")
                        or tokens[0] in self.DERIVATIVE_ADVERB_TAGS
                    ):
                        self.__adverbs_irreg[key] = term

            # Prefer noun forms over adjective forms in noun exceptions
            if is_noun and is_adjective_form and key in self.__nouns_irreg:
                del self.__nouns_irreg[key]

        # Fix incorrect derivations
        self.__nouns_irreg["soldados"] = "soldado"
        # Último is not a derived form of 'ulterior'
        self.__adjectives_irreg.pop("último", None)
        self.__resolve_derived_terms(self.__adjectives_irreg)
        self.__resolve_derived_terms(self.__pronouns_irreg)
        self.__resolve_derived_terms(self.__verbs_irreg)
        self.__resolve_derived_terms(self.__nouns_irreg)
        self.__resolve_derived_terms(self.__adverbs_irreg)

        self.__remove_covered_entries()

    def __parse_source(self):
        sys.stdout.write("Parsing downloaded file...\n")
        namespace_regex = re.compile(r"\{[^}]+\}")
        iterable = ET.iterparse(self.OUTPUT_LEMMA)
        event, root = next(iterable)
        NS = namespace_regex.match(root.tag)[0]
        for event, elem in iterable:
            if (elem.tag == NS + 'page'):
                titulo = elem.find(NS + "title").text
                # These page entries are useless
                iterator = (e for e in self.SKIP_TITLES if titulo.startswith(e))
                if next(iterator, None):
                    continue

                revision = elem.find(NS + "revision")
                contenido = revision.find(NS + "text")
                result = self.__process_text(contenido.text, "es")
                if result != []:
                    self.__results[titulo] = result

                elem.clear()

    def __process_lang(self, text):
        results = []
        categories = self.__category_regex.findall(text)
        for category in categories:
            results.append(category)
        acceptions = self.__acception_regex.findall(text)
        for acception in acceptions:
            results.append(acception)
        return results

    def __remove_covered_entries(self):
        remove_keys = []
        verb_rules = self.COMMON_RULES.get('verb', {})
        for key, val in self.__verbs_irreg.items():
            for old, new in verb_rules.items():
                if key.endswith(old) and key[: len(key)-len(old)] + new == val:
                    remove_keys.append(key)
                    break

        for key in remove_keys:
            self.__verbs_irreg.pop(key)

    def __resolve_derived_terms(self, dictionary):
        for key, value in dictionary.items():
            next_value = dictionary.get(value, None)
            while next_value and next_value != value:
                value = next_value
                next_value = dictionary.get(next_value, None)
            dictionary[key] = value

    """
    Outputs lemmatization results
    """

    def __export(self):
        sys.stdout.write("Exporting lemmatizer files...\n")
        dets_irreg = self.COMMON_EXCEPTIONS.get("det", {})
        content = {
            "type": "wiki",
            "adj": self.__adjectives_irreg,
            "adverb": self.__adverbs_irreg,
            "noun": self.__nouns_irreg,
            "verb": self.__verbs_irreg,
            "pron": self.__pronouns_irreg,
            "det": dets_irreg,
        }

        with open(Config.OUTPUT_FILE, "w", encoding="utf-8") as destination:
            json.dump(
                content,
                destination,
                sort_keys=True,
                indent=True,
                ensure_ascii=False
            )

    def download(self):
        self.__download_source()
        self.__decompress_source()

    def parse(self):
        self.__parse_source()
        self.__generate_lemmatization()
        self.__export()
