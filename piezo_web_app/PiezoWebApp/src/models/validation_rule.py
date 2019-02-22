class ValidationRule:
    def __init__(self, key, classification, default, minimum=None, maximum=None):
        self._key = key
        self._classification = classification
        self._default = default
        self._minimum = minimum
        self._maximum = maximum

    @property
    def key(self):
        return self._key

    @property
    def classification(self):
        return self._classification

    @property
    def default(self):
        return self._default

    @property
    def minimum(self):
        return self._minimum

    @property
    def maximum(self):
        return self._maximum
