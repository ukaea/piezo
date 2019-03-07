from PiezoWebApp.src.models.spark_job_argument_classification import ArgumentClassification


class ValidationRule:
    def __init__(self, rule_dict):

        classification_string = self._safe_get_value('classification', rule_dict)
        self._classification = ArgumentClassification[classification_string]

        self._conditional_input_name = self._safe_get_value('conditional_input_name', rule_dict)
        self._conditional_input_value = self._safe_get_value('conditional_input_value', rule_dict)

        self._default = self._safe_get_value('default', rule_dict)
        self._minimum = self._safe_get_value('minimum', rule_dict)
        self._maximum = self._safe_get_value('maximum', rule_dict)
        self._options = self._safe_get_value('options', rule_dict)

        self._type = self._safe_get_value('type', rule_dict, value_if_missing="string")

    @staticmethod
    def _safe_get_value(key, dictionary, value_if_missing=None):
        if key in dictionary:
            return dictionary[key]
        return value_if_missing

    @property
    def classification(self):
        return self._classification

    @property
    def conditional_input_name(self):
        return self._conditional_input_name

    @property
    def conditional_input_value(self):
        return self._conditional_input_value

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

    @property
    def type(self):
        return self._type
