from tornado_json import schema

from PiezoWebApp.src.handlers.base_handler import BaseHandler
from PiezoWebApp.src.handlers.schema.schema_helpers import create_object_schema_with_string_properties


# pylint: disable=abstract-method
class SubmitJobHandler(BaseHandler):
    @schema.validate(
        input_schema=create_object_schema_with_string_properties(
            ['job_name', 'namespace'], required=['job_name', 'namespace']),
        input_example={
            'job_name': 'example_job_name',  # to be replaced by list of arguments we will allow the user to configure
            'namespace': 'default'
        }
    )
    def post(self, *args, **kwargs):
        job_name = self.get_body_attribute('job_name', required=True)
        namespace = self.get_body_attribute('namespace', required=True)
        self._logger.debug(f'Trying to submit job "{job_name}" to namespace "{namespace}".')
        body = {'job_name': job_name, 'namespace': namespace}
        result = self._kubernetes_service.submit_job(body)
        self._logger.debug(f'Submitting job "{job_name}" to namespace "{namespace}" returned result "{result}".')
        return result
