from tornado_json import schema

from PiezoWebApp.src.handlers.base_handler import BaseHandler
from PiezoWebApp.src.handlers.schema.schema_helpers import create_object_schema_with_string_properties


class SubmitJobHandler(BaseHandler):
    @schema.validate(
        input_schema=create_object_schema_with_string_properties(['body'], required=['body']),
        input_example={
            'body': 'body_placeholder'  # to be replaced by list of arguments we will allow the user to configure
        }
    )
    def post(self, *args, **kwargs):
        body = self.get_body_attribute('body', required=True)
        result = self._kubernetes_adapter.submit_job(body)
        return result
