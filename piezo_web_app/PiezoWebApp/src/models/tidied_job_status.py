class TidiedJobStatus:
    def __init__(self, job_name, status, tidied, err_msg, err_status):
        self._job_name = job_name
        self._status = status
        self._tidied = tidied
        self._err_msg = err_msg
        self._err_status = err_status

    @property
    def job_name(self):
        return self._job_name

    @property
    def status(self):
        return self._status

    @property
    def tidied(self):
        return self._tidied

    @property
    def err_msg(self):
        return self._err_msg

    @property
    def err_status(self):
        return self._err_status
