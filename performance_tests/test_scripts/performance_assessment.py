import dateutil.parser
import re

import web_api_interaction


def get_job_timings(base_url, job_name):
    # Get timings from job status
    job_status_data = web_api_interaction.get_job_status(base_url, job_name)
    created = dateutil.parser.parse(job_status_data['created'])
    submitted = dateutil.parser.parse(job_status_data['last_submitted'])
    terminated = dateutil.parser.parse(job_status_data['terminated'])

    # Get first timestamp from log file
    job_log = web_api_interaction.get_job_log(base_url, job_name)
    start_timestamp_search = re.search('\\nJOB-START@20(\d){2}-[0-1]\d-[0-3]\d [0-2]\d:[0-5]\d:[0-5]\dZ', job_log)
    first_timestamp = start_timestamp_search.group(0).split('@')[1]
    first_timestamp = dateutil.parser.parse(first_timestamp)
    end_timestamp_search = re.search('\\nJOB-END@20(\d){2}-[0-1]\d-[0-3]\d [0-2]\d:[0-5]\d:[0-5]\dZ', job_log)
    end_timestamp = end_timestamp_search.group(0).split('@')[1]
    end_timestamp = dateutil.parser.parse(end_timestamp)

    return {
        'k8s_queue_time': submitted - created,
        'spark_spinup_time': first_timestamp - submitted,
        'job_run_time': end_timestamp - first_timestamp,
        'spark_spindown_time': terminated - end_timestamp
    }
