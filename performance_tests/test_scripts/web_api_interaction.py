import requests


def get_response_data(base_url, route, json):
    url = f'{base_url}/{route}'
    response = requests.request('GET', url, json=json)
    return response.json()['data']


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


def submit_job(base_url, k8s_script):
    json_body = {
        'name': k8s_script,
        'language': 'Python',
        'python_version': '2',
        'path_to_main_app_file': f's3a://kubernetes/inputs/{k8s_script}.py',
        'label': 'performanceTest'
    }
    url = f'{base_url}/submitjob'
    response = requests.request('POST', url, json=json_body)
    job_name = dict(response.json())['data']['job_name']
    return job_name
