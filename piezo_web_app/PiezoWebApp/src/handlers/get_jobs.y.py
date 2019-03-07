from PiezoWebApp.src.handlers.base_handler import BaseHandler


# pylint: disable=abstract-method
class JobStatusHandler(BaseHandler):
    def get(self, *args, **kwargs):
        result = self._spark_job_service.get_jobs()
        self._logger.debug(f'Getting list of spark applications present returned: "{result}"')
        self.check_request_was_completed_successfully(result)
        del result['status']
        return result
