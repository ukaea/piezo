from tornado_json import schema

from PiezoWebApp.src.handlers.base_handler import BaseHandler


class TidyJobsHandler(BaseHandler):
    @schema.validate(
        output_schema={
            "type": "object",
            "properties": {
                "jobs_processed": {"type": "object"},
                "jobs_skipped": {"type": "object"},
                "jobs_failed_to_process": {"type": "object"}
            },
        }
    )
    def post(self, *args, **kwargs):
        result = self._spark_job_service.tidy_jobs()
        self._logger.debug(f'Tidying spark application returned: "{result}".')
        self.check_request_was_completed_successfully(result)
        del result['status']
        return result
