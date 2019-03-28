from tornado_json import schema

from PiezoWebApp.src.handlers.base_handler import BaseHandler

class TidyJobsHandler(BaseHandler):
    @schema.validate(
        output_schema={
            "type": "object",
            "properties": {
                "Jobs processed": {"type": "object"},
                "Jobs untouched": {"type": "object"},
                "Jobs failed to process": {"type": "object"}
            },
        }
    )
    def post(self, *args, **kwargs):
        result = self._spark_job_service.tidy_jobs()
        self._logger.debug(f'Tidying spark application returned: "{result["status"]}".')
        self.check_request_was_completed_successfully(result)
        del result['status']
        return result
