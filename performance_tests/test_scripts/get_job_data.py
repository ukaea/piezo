import dateutil.parser
import re
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


def get_job_timings(base_url, job_name):
    # Get timings from job status
    job_status_data = get_job_status(base_url, job_name)
    created = dateutil.parser.parse(job_status_data['created'])
    submitted = dateutil.parser.parse(job_status_data['last_submitted'])
    terminated = dateutil.parser.parse(job_status_data['terminated'])

    # Get first timestamp from log file
    job_log = get_job_log(base_url, job_name)
    start_timestamp_search = re.search('\\nJOB-START@20(\d){2}-[0-1]\d-[0-3]\d [0-2]\d:[0-5]\d:[0-5]\dZ', job_log)
    first_timestamp = dateutil.parser.parse(start_timestamp_search.group(0))
    end_timestamp_search = re.search('\\nJOB-END@20(\d){2}-[0-1]\d-[0-3]\d [0-2]\d:[0-5]\d:[0-5]\dZ', job_log)
    end_timestamp = dateutil.parser.parse(end_timestamp_search.group(0))

    return {
        'k8s_queue_time': submitted - created,
        'spark_spinup_time': first_timestamp - submitted,
        'job_run_time': terminated - first_timestamp
    }


if __name__ == '__main__':
    piezo_base_url = 'http://host-172-16-113-146.nubes.stfc.ac.uk:31924/piezo'
    jobs = get_jobs(piezo_base_url)
    print(jobs)
    first_job_name = list(jobs)[0]
    job_timings = get_job_timings(piezo_base_url, first_job_name)
    print(job_timings)
