from tornado_json.requesthandlers import APIHandler
from tornado_json import exceptions

from PiezoWebApp.src.utils.str_helper import is_str_empty


# pylint: disable=abstract-method
class BaseHandler(APIHandler):
    # pylint: disable=arguments-differ
    def initialize(self, logger, spark_job_service, validation_ruleset):
        self._logger = logger
        self._spark_job_service = spark_job_service
        self._validation_ruleset = validation_ruleset
        self.clear_header("Server")

    @property
    def validation_ruleset(self):
        return self._validation_ruleset

    def get_body_attribute(self, key, default=None, required=False, value_type=str):
        # pylint: disable=no-member
        if key in self.body:
            self._check_attribute_is_not_empty(key, default, required, value_type)
            return self.body[key]
        if required:
            raise exceptions.APIError(400, f'Attribute "{key}" is missing')
        return default

    def _check_attribute_is_not_empty(self, key, default, required, value_type):
        # pylint: disable=no-member
        if value_type == str and is_str_empty(self.body[key]) is False:
            return
        if value_type == list and (self.body[key] is not None) and len(self.body[key]) > 0:
            return
        # If missing see if can use as default
        if required:
            raise exceptions.APIError(400, f'Attribute "{key}" is empty')
        self.body[key] = default

    @staticmethod
    def check_request_was_completed_successfully(result):
        exceptions.api_assert(result["status"] == 200,
                              result["status"],
                              result['message'])
