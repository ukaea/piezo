from tornado_json import schema

from PiezoWebApp.src.handlers.base_handler import BaseHandler
from PiezoWebApp.src.handlers.schema.schema_helpers import create_object_schema_with_string_properties


# pylint: disable=abstract-method
class OutputFilesHandler(BaseHandler):
    @schema.validate(
        input_schema=create_object_schema_with_string_properties(
            ['job_name'], required=['job_name']),
        input_example={
            'job_name': 'example-job'
        }
    )
    def get(self, *args, **kwargs):
        spark_job = self.get_body_attribute('job_name', required=True)
        self._logger.debug(f'Trying to get output files for spark job "{spark_job}".')
        result = self._spark_job_service.get_output_files_temp_urls(spark_job)
        self._logger.debug(
            f'Getting output files for spark job "{spark_job}" returned result "{result["status"]}".'
        )
        self.check_request_was_completed_successfully(result)
        del result['status']
        return result
