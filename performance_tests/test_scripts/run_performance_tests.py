import system_load_tests
from web_api_interaction import SubmitJobOptions


if __name__ == '__main__':
    job_numbers = [1, 3, 10]
    piezo_base_url = 'http://host-172-16-113-146.nubes.stfc.ac.uk:31856/piezo'
    job_options = [
        SubmitJobOptions(driver_cores=0.1, driver_memory="512m", executors=1, executor_cores=1, executor_memory="512m"),
        SubmitJobOptions(driver_cores=1.0, driver_memory="2048m", executors=10, executor_cores=4, executor_memory="4096m")
    ]
    system_load_results = system_load_tests.run_system_load_tests(piezo_base_url, job_numbers, job_options)

