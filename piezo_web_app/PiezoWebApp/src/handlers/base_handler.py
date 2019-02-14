from tornado_json.requesthandlers import APIHandler
from tornado_json import exceptions

from PiezoWebApp.src.utils.str_helper import is_str_empty


class BaseHandler(APIHandler):
    def initialize(self, kubernetes_service):
        self._kubernetes_service = kubernetes_service

    def get_body_attribute(self, key, default=None, required=False, value_type=str):
        # pylint: disable=no-member
        if key in self.body:
            self._check_attribute_is_not_empty(key, default, required, value_type)
            return self.body[key]
        if required:
            raise exceptions.APIError(400, 'Attribute missing')
        return default

    def _check_attribute_is_not_empty(self, key, default, required, value_type):
        # pylint: disable=no-member
        if value_type == str and is_str_empty(self.body[key]) is False:
                return
        elif value_type == list and (self.body[key] is not None) and len(self.body[key]) > 0:
            return
        # If missing see if can use as default
        if required:
            raise exceptions.APIError(400, f'Attribute "{key}" is empty')
        self.body[key] = default
