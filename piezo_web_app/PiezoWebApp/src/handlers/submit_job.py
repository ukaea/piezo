from tornado_json import schema

from PiezoWebApp.src.config.spark_job_validation_rules import VALIDATION_RULES
from PiezoWebApp.src.handlers.base_handler import BaseHandler
from PiezoWebApp.src.handlers.schema.schema_helpers import create_object_schema_from_validation_rules
from PiezoWebApp.src.handlers.schema.schema_helpers import create_object_schema_with_string_properties


# pylint: disable=abstract-method
class SubmitJobHandler(BaseHandler):
    @schema.validate(
        input_schema=create_object_schema_from_validation_rules(VALIDATION_RULES),
        input_example={
            'name': 'example_job_name',  # to be replaced by list of arguments we will allow the user to configure
            'language': 'Python',
            'path_to_main_app_file': '/path/to/main.file'

        },
        output_schema=create_object_schema_with_string_properties(['driver_name', 'message'], required=['message']),
        output_example={
            'message': 'Job driver created successfully',
            'driver_name': 'example-driver'
        }
    )
    def post(self, *args, **kwargs):
        name = self.body['name']
        self._logger.debug(f'Trying to submit job "{name}".')
        result = self._spark_job_service.submit_job(self.body)
        status = result['status']
        self._logger.debug(f'Submitting job "{name}" returned status code "{status.value}".')
        self.check_request_was_completed_successfully(result)
        del result['status']
        return result
