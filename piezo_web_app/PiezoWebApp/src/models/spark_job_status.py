class SparkJobStatus:

    def __init__(self, api_response):
        self._api_response = api_response
        self._default = "UNKNOWN"

    @property
    def status(self):
        try:
            return self._api_response['status']['applicationState']['state']
        except KeyError:
            return self._default

    @property
    def creation_time(self):
        try:
            return self._api_response['metadata']['creationTimestamp']
        except KeyError:
            return self._default

    @property
    def submission_attempts(self):
        try:
            return self._api_response['status']['submissionAttempts']
        except KeyError:
            return self._default

    @property
    def last_submitted(self):
        try:
            return self._api_response['status']['lastSubmissionAttemptTime']
        except KeyError:
            return self._default

    @property
    def terminated_time(self):
        try:
            return self._api_response['status']['terminationTime']
        except KeyError:
            return self._default

    @property
    def err_msg(self):
        try:
            return self._api_response['status']['applicationState']['errorMessage']
        except KeyError:
            return self._default
