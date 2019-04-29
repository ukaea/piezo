import requests


def get_response_data(base_url, route, json):
    url = f'{base_url}/{route}'
    response = requests.request('GET', url, json=json)
    json = response.json()
    if 'data' in json:
        return json['data']
    else:
        print(url)
        print(json)
        print(response)
        print(json)
        raise RuntimeError('Unexpected response!')


def get_jobs(base_url):
    data = get_response_data(base_url, 'getjobs', {})
    jobs = dict(data)['spark_jobs']
    return jobs


def get_job_status(base_url, job_name):
    data = get_response_data(base_url, 'jobstatus', {'job_name': job_name})
    return data


def get_job_log(base_url, job_name):
    data = get_response_data(base_url, 'getlogs', {'job_name': job_name})
    log_content = data['message']
    return log_content


def is_job_finished(base_url, job_name):
    status_data = get_job_status(base_url, job_name)
    job_status = status_data['job_status']
    return job_status == 'COMPLETED'


def is_system_clean(base_url):
    tidy_jobs(base_url)
    jobs = get_jobs(base_url)
    return not jobs


def submit_job(base_url, k8s_script, **kwargs):
    json_body = {
        'name': k8s_script,
        'language': 'Python',
        'python_version': '2',
        'path_to_main_app_file': f's3a://kubernetes/inputs/{k8s_script}.py',
        'label': 'performanceTest',
        **kwargs
    }
    url = f'{base_url}/submitjob'
    response = requests.request('POST', url, json=json_body)
    job_name = dict(response.json())['data']['job_name']
    return job_name


class SubmitJobOptions:
    def __init__(self, driver_cores: float, driver_memory: str, executors: int, executor_cores: int, executor_memory: str):
        self._driver_cores = driver_cores
        self._driver_memory = driver_memory
        self._executors = executors
        self._executor_cores = executor_cores
        self._executor_memory = executor_memory

    @property
    def user_args(self):
        return {
            'driver_cores': self._driver_cores,
            'driver_memory': self._driver_memory,
            'executors': self._executors,
            'executor_cores': self._executor_cores,
            'executor_memory': self._executor_memory
        }


def tidy_jobs(base_url):
    url = f'{base_url}/tidyjobs'
    requests.request('POST', url, json={})
