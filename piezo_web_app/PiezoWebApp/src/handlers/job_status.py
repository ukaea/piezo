from tornado_json import schema

from PiezoWebApp.src.handlers.base_handler import BaseHandler
from PiezoWebApp.src.handlers.schema.schema_helpers import create_object_schema_with_string_properties


# pylint: disable=abstract-method
class JobStatusHandler(BaseHandler):
    @schema.validate(
        input_schema=create_object_schema_with_string_properties(
            ['job_name'], required=['job_name']),
        input_example={
            'job_name': 'example-job'
        }
    )
    def get(self, *args, **kwargs):
        spark_job = self.get_body_attribute('job_name', required=True)
        self._logger.debug(f'Trying to get status of spark job "{spark_job}".')
        result = self._spark_job_service.get_job_status(spark_job)
        self._logger.debug(
            f'Getting status of spark job "{spark_job}" returned '
            f'result "{result["status"]}".'
        )
        self.check_request_was_completed_successfully(result)
        del result['status']
        return result
