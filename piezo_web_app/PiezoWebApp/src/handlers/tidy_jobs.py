from tornado_json import schema

from PiezoWebApp.src.handlers.base_handler import BaseHandler

class TidyJobsHandler(BaseHandler):
    @schema.validate(
        output_schema={
            "type": "object",
            "properties": {
                "Jobs processed": {"type": "string"},
                "Jobs untouched": {"type": "string"}
            },
        }
    )
    def POST(self, *args, **kwargs):
        result = self._spark_job_service.tidy_jobs()
        self._logger.debug(f'Tidying spark application returned: "{result["status"]}".')
        self.check_request_was_completed_successfully(result)
        del result['status']
        return result
