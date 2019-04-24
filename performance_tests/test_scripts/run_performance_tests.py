import time

import web_api_interaction
import performance_assessment

if __name__ == '__main__':
    piezo_base_url = 'http://host-172-16-113-146.nubes.stfc.ac.uk:31924/piezo'
    job_name = web_api_interaction.submit_job(piezo_base_url, 'pi')
    print(f'"pi" job running as "{job_name}"')
    counter = 0
    is_job_finished = web_api_interaction.is_job_finished(piezo_base_url, job_name)
    while counter < 10 and not is_job_finished:
        time.sleep(10)
        is_job_finished = web_api_interaction.is_job_finished(piezo_base_url, job_name)
        counter += 1
    job_timings = performance_assessment.get_job_timings(piezo_base_url, job_name)
    print(job_timings)
