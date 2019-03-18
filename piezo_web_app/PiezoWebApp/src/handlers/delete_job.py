from tornado_json import schema

from PiezoWebApp.src.handlers.base_handler import BaseHandler
from PiezoWebApp.src.handlers.schema.schema_helpers import create_object_schema_with_string_properties


# pylint: disable=abstract-method
class DeleteJobHandler(BaseHandler):
    @schema.validate(
        input_schema=create_object_schema_with_string_properties(
            ['job_name'],
            required=['job_name']),
        input_example={
            'job_name': 'example-spark-job'
        }
    )
    def delete(self, *args, **kwargs):
        job_name = self.get_body_attribute('job_name', required=True)
        self._logger.debug(f'Trying to delete job "{job_name}".')
        result = self._spark_job_service.delete_job(job_name)
        self._logger.debug(
            f'Deleting job "{job_name}" returned result "{result["status"]}".'
        )
        self.check_request_was_completed_successfully(result)
        del result['status']
        return result
