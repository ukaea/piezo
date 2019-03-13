from tornado_json import schema

from PiezoWebApp.src.handlers.base_handler import BaseHandler
from PiezoWebApp.src.handlers.schema.schema_helpers import create_object_schema_with_string_properties


# pylint: disable=abstract-method
class GetJobsHandler(BaseHandler):
    @schema.validate(
        input_schema=create_object_schema_with_string_properties(
            ['label']),
        input_example={
            'label': 'test'
        },
        output_schema={
            "type": "object",
            "properties": {
                "message": {"type": "string"},
                "spark_jobs": {
                    "type": "object",
                    "properties": {
                        "job_name": {"type": "string"},
                        "status": {"type": "string"}
                    }
                }
            },
        }
    )
    def get(self, *args, **kwargs):
        label = self.get_body_attribute('label', default="ALL", required=False)
        result = self._spark_job_service.get_jobs(label)
        self._logger.debug(f'Getting list of spark applications with label "{label}" returned: "{result["status"]}".')
        self.check_request_was_completed_successfully(result)
        del result['status']
        return result
