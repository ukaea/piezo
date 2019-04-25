from PiezoWebApp.src.handlers.base_handler import BaseHandler
from PiezoWebApp.src.handlers.schema import schema
from PiezoWebApp.src.handlers.schema.schema_helpers import create_object_schema_with_string_properties


# pylint: disable=abstract-method
class SubmitJobHandler(BaseHandler):
    @schema.validate(
        input_example={
            'name': 'example-job-name',  # to be replaced by list of arguments we will allow the user to configure
            'language': 'Python',
            'path_to_main_app_file': '/path/to/main.file'

        },
        output_schema=create_object_schema_with_string_properties(
            ['job_name', 'message', 'spark_ui'], required=['message']),
        output_example={
            'message': 'Job driver created successfully',
            'job_name': 'example-job-name-abc12',
            'spark_ui': 'http://piezo.com/example-job-name-abc12-ui-svc'
        }
    )
    def post(self, *args, **kwargs):
        name = self.body['name'] if 'name' in self.body else None
        self._logger.debug(f'Trying to submit job "{name}".')
        result = self._spark_job_service.submit_job(self.body)
        status = result['status']
        self._logger.debug(f'Submitting job "{name}" returned status code "{status}".')
        self.check_request_was_completed_successfully(result)
        del result['status']
        return result
