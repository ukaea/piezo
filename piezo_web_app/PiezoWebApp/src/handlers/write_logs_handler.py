from tornado_json import schema

from PiezoWebApp.src.handlers.base_handler import BaseHandler
from PiezoWebApp.src.handlers.schema.schema_helpers import create_object_schema_with_string_properties


# pylint: disable=abstract-method
class WriteLogsHandler(BaseHandler):
    @schema.validate(
        input_schema=create_object_schema_with_string_properties(
            ['job_name', 'namespace'], required=['job_name', 'namespace']),
        input_example={
            'job_name': 'example-job',
            'namespace': 'default'
        },
        output_schema=create_object_schema_with_string_properties(['message'], required=['message']),
        output_example={
            'message': 'Logs written to "/path/to/log.txt" in bucket "bucket-name"'
        }
    )
    def post(self, *args, **kwargs):
        job_name = self.get_body_attribute('job_name', required=True)
        namespace = self.get_body_attribute('namespace', required=True)
        self._logger.debug(f'Trying to write logs to file for job "{job_name}".')
        result = self._spark_job_service.write_logs_to_file(job_name, namespace)
        status = result['status']
        self._logger.debug(f'Writing logs to file for job "{job_name}" returned status code "{status}".')
        self.check_request_was_completed_successfully(result)
        del result['status']
        return result
