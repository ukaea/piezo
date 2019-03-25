class SparkJobStatus:

    def __init__(self, api_response):
        self._api_response = api_response
        self._status = "UNKOWN"
        self._creation_time = "UNKNOWN"
        self._submission_attempts = "UNKNOWN"
        self._last_submitted = "UNKNOWN"
        self._termination_time = "UNKNOWN"
        self._err_msg = "UNKNOWN"

    @property
    def status(self):
        try:
            return self._api_response['status']['applicationState']['state']
        except KeyError:
            return self._status

    @property
    def creation_time(self):
        try:
            return self._api_response['metadata']['creationTimestamp']
        except KeyError:
            return self._creation_time

    @property
    def submission_attempts(self):
        try:
            return self._api_response['status']['submissionAttempts']
        except KeyError:
            return self._submission_attempts

    @property
    def last_submitted(self):
        try:
            return self._api_response['status']['lastSubmissionAttemptTime']
        except KeyError:
            return self._last_submitted

    @property
    def terminated_time(self):
        try:
            return self._api_response['status']['terminationTime']
        except KeyError:
            return self._termination_time

    @property
    def err_msg(self):
        try:
            return self._api_response['status']['applicationState']['errorMessage']
        except KeyError:
            return self._err_msg
