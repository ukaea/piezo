class ValidationRule:
    def __init__(self, classification, default, minimum=None, maximum=None, options=None):
        self._classification = classification
        self._default = default
        self._minimum = minimum
        self._maximum = maximum
        self._options = options

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

    @property
    def options(self):
        return self._options
