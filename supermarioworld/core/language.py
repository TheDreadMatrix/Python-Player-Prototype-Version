from supermarioworld.johnson import readData


class Locale:
    AVAILABLE_LANGUAGES = {
        "ru",
        "en"
    }
    def __init__(self, game, language_key: str):
        self.game = game

        language_key = language_key.lower()

        if language_key not in self.AVAILABLE_LANGUAGES:
            language_key = "en"


        self.language_data = readData(game.paths.ConfigPath(f"locale/{language_key}.json"))


    def switchLanguage(self, language_key: str):
        language_key = language_key.lower()

        if language_key not in self.AVAILABLE_LANGUAGES:
            language_key = "en"

        self.language_data = readData(self.game.paths.ConfigPath(f"locale/{language_key}.json"))


    def gettext(self, word_key):
        return self.language_data.get(word_key, word_key)