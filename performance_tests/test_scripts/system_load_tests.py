import csv
import time

import performance_assessment
import web_api_interaction


def single_system_load_test(base_url, num_jobs):
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


def run_system_load_tests(base_url, job_numbers):
    timings = []
    for num_jobs in job_numbers:
        timings.append(single_system_load_test(base_url, num_jobs))
    with open('system_load_test_results.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',')
        csvwriter.writerow(['num_jobs', 'k8s_queue_avg', 'spark_spinup_avg', 'job_run_avg', 'spark_spindown_avg'])
        for i in range(len(job_numbers)):
            csvwriter.writerow([
                job_numbers[i],
                performance_assessment.average_time_for(timings[i], 'k8s_queue_time'),
                performance_assessment.average_time_for(timings[i], 'spark_spinup_time'),
                performance_assessment.average_time_for(timings[i], 'job_run_time'),
                performance_assessment.average_time_for(timings[i], 'spark_spindown_time')
            ])
