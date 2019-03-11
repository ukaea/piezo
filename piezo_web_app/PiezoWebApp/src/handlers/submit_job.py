from PiezoWebApp.src.handlers.base_handler import BaseHandler
from PiezoWebApp.src.handlers.schema import schema
from PiezoWebApp.src.handlers.schema.schema_helpers import create_object_schema_with_string_properties


# pylint: disable=abstract-method
class SubmitJobHandler(BaseHandler):
    @schema.validate(
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
        result = self._spark_job_service.submit_job(self.body)
        status = result['status']
        self._logger.debug(f'Submitting job returned status code "{status}".')
        self.check_request_was_completed_successfully(result)
        del result['status']
        return result
