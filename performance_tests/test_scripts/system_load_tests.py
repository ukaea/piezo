import csv
import time

import performance_assessment
import web_api_interaction


def single_system_load_test(base_url, num_jobs, **kwargs):
    if not web_api_interaction.is_system_clean(base_url):
        raise RuntimeError("Jobs currently running on the system")

    k8s_script = 'pi'

    submitted_jobs = [web_api_interaction.submit_job(base_url, k8s_script) for _ in range(num_jobs)]
    print(f'Submitted {num_jobs} "{k8s_script}" jobs to piezo')

    finished_job_timings = []
    counter = 0
    while counter < 24 and submitted_jobs:
        counter += 1
        time.sleep(5)
        still_running = []
        for job_name in submitted_jobs:
            if web_api_interaction.is_job_finished(base_url, job_name):
                job_timings = performance_assessment.get_job_timings(base_url, job_name)
                finished_job_timings.append(job_timings)
            else:
                still_running.append(job_name)
        submitted_jobs = still_running

    if submitted_jobs:
        raise RuntimeError("Jobs still running")

    return finished_job_timings


def run_system_load_tests(base_url, job_numbers, job_options):
    timings = []
    fixed_options = {
        "image_pull_policy": ["Always", "IfNotPresent"]
    }

    user_options = {
        "driver_cores": [0.1, 1],
        "driver_memory": ["512m", "2048m"],
        "executors": [1, 10],
        "executor_cores": [1, 4],
        "executor_memory": ["512m", "4096m"]
    }

    for num_jobs in job_numbers:
        for job_option in job_options:
            timings.append(single_system_load_test(base_url, num_jobs, **job_option.user_args))

    job_options_headers = list(job_options[0].user_args)
    headers = ['num_jobs'] + job_options_headers + ['k8s_queue_avg', 'spark_spinup_avg', 'job_run_avg', 'spark_spindown_avg']

    with open('system_load_test_results.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',')
        csvwriter.writerow(headers)
        for i in range(len(job_numbers)):
            for j in range(len(job_options)):
                user_args = job_options[j].user_args
                job_results = [job_numbers[i]] + [user_args[arg_name] for arg_name in job_options_headers] + [
                    performance_assessment.average_time_for(timings[i], 'k8s_queue_time'),
                    performance_assessment.average_time_for(timings[i], 'spark_spinup_time'),
                    performance_assessment.average_time_for(timings[i], 'job_run_time'),
                    performance_assessment.average_time_for(timings[i], 'spark_spindown_time')
                ]
                csvwriter.writerow(job_results)
