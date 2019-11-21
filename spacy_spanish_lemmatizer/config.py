import os


class Config:

    BASE_FOLDER = os.path.realpath(os.path.join(__file__, ".."))
    DATA_FOLDER = BASE_FOLDER + os.sep + "data"
    TEMP_FOLDER = BASE_FOLDER + os.sep + "tmp"
    COMMON_FOLDER = BASE_FOLDER + os.sep + "common"
    COMMON_RULES = COMMON_FOLDER + os.sep + "rules.json"
    COMMON_EXCEPTIONS = COMMON_FOLDER + os.sep + "exceptions.json"
    OUTPUT_FILE = DATA_FOLDER + os.sep + "entries.json"
