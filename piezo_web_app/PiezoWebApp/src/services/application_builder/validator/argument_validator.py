class ArgumentValidator:

    def __init__(self):
        self.valid_languages = ["Python", "Scala"]

    def language_is_valid(self, language):
        return language in self.valid_languages


