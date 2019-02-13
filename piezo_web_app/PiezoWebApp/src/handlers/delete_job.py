from tornado_json import schema

from PiezoWebApp.src.handlers.base_handler import BaseHandler
from PiezoWebApp.src.handlers.schema.schema_helpers import create_object_schema_with_string_properties


class GetLogsHandler(BaseHandler):
    @schema.validate(
        input_schema=create_object_schema_with_string_properties(
            ['job_name', 'namespace'],
            required=['job_name', 'namespace']),
        input_example={
            'job_name': 'example-spark-job',
            'namespace': 'default'
        }
    )
    def delete(self, *args, **kwargs):
        job_name = self.get_body_attribute('job_name', required=True)
        namespace = self.get_body_attribute('namespace', required=True)
        result = self._kubernetes_adapter.delete_job(job_name, namespace)
        return result
