class ArgumentValidator:

    @staticmethod
    def language_validator(language):
        return language in ["Python", "Scala", "R"]

    def