from unittest.mock import patch

from PiezoWebApp.src.services.spark_job.spark_job_constants import CRD_GROUP
from PiezoWebApp.src.services.spark_job.spark_job_constants import CRD_PLURAL
from PiezoWebApp.src.services.spark_job.spark_job_constants import CRD_VERSION
from PiezoWebApp.src.services.spark_job.spark_job_constants import NAMESPACE

from PiezoWebApp.tests.services.spark_job.spark_job_service_test import TestSparkJobService


class SparkJobServiceGetJobStatusTest(TestSparkJobService):
    @patch('PiezoWebApp.src.services.spark_job.spark_job_service.SparkJobService.get_jobs',
           return_value={"spark_jobs": {"job1": "RUNNING",
                                        "job2": "PENDING",
                                        "job3": "SUCCEEDED",
                                        "job4": "COMPLETED",
                                        "job5": "CrashLoopBackOff",
                                        "job6": "UNKNOWN",
                                        "job7": "FAILED",
                                        "job8": "COMPLETED"},
                         "status": 200})
    def test_tidy_jobs_calls_write_and_delete_with_correct_jobs(self, get_jobs):
        # Arrange
        self.mock_kubernetes_adapter.delete_options.return_value = 'Delete_options'
        # Act
        response = self.test_service.tidy_jobs()
        # Assert
        self.mock_logger.debug.assert_any_call('Not processing job "job1", current status is "RUNNING"')
        self.mock_logger.debug.assert_any_call('Not processing job "job2", current status is "PENDING"')
        self.mock_logger.debug.assert_any_call('Not processing job "job3", current status is "SUCCEEDED"')
        self.mock_logger.debug.assert_any_call('Not processing job "job5", current status is "CrashLoopBackOff"')
        self.mock_logger.debug.assert_any_call('Not processing job "job6", current status is "UNKNOWN"')
        self.mock_kubernetes_adapter.read_namespaced_pod_log.assert_any_call('job4-driver', 'default')
        self.mock_kubernetes_adapter.read_namespaced_pod_log.assert_any_call('job7-driver', 'default')
        self.mock_kubernetes_adapter.read_namespaced_pod_log.assert_any_call('job8-driver', 'default')
        assert self.mock_kubernetes_adapter.read_namespaced_pod_log.call_count == 3
        self.mock_kubernetes_adapter.delete_namespaced_custom_object.assert_any_call(CRD_GROUP,
                                                                                     CRD_VERSION,
                                                                                     NAMESPACE,
                                                                                     CRD_PLURAL,
                                                                                     'job4',
                                                                                     'Delete_options')
        self.mock_kubernetes_adapter.delete_namespaced_custom_object.assert_any_call(CRD_GROUP,
                                                                                     CRD_VERSION,
                                                                                     NAMESPACE,
                                                                                     CRD_PLURAL,
                                                                                     'job7',
                                                                                     'Delete_options')
        self.mock_kubernetes_adapter.delete_namespaced_custom_object.assert_any_call(CRD_GROUP,
                                                                                     CRD_VERSION,
                                                                                     NAMESPACE,
                                                                                     CRD_PLURAL,
                                                                                     'job8',
                                                                                     'Delete_options')
        assert self.mock_kubernetes_adapter.delete_namespaced_custom_object.call_count == 3
        assert response == {'status': 200,
                            'message': '8 Spark jobs found',
                            'jobs_tidied': {'job4': 'COMPLETED',
                                            'job7': 'FAILED',
                                            'job8': 'COMPLETED'},
                            'jobs_untouched': {'job1': 'RUNNING',
                                               'job2': 'PENDING',
                                               'job3': 'SUCCEEDED',
                                               'job5': 'CrashLoopBackOff',
                                               'job6': 'UNKNOWN'},
                            'jobs_failed_to_process': {}}
        get_jobs.assert_called_once_with(label=None)

    @patch('PiezoWebApp.src.services.spark_job.spark_job_service.SparkJobService.get_jobs',
           return_value={'status': 999, 'message': 'Unexpected response from Kubernetes API when trying to get'
                                                   ' list of spark jobs: K8s Reason'})
    def test_tidy_jobs_returns_kubernetes_api_exception_reason_raised_getting_jobs(self, get_jobs):
        # Act
        result = self.test_service.tidy_jobs()
        # Assert
        expected_message = 'Unexpected response from Kubernetes API when trying to get list of spark jobs: K8s Reason'
        self.assertDictEqual(result, {'status': 999, 'message': expected_message})
        get_jobs.assert_called_once_with(label=None)

    @patch('PiezoWebApp.src.services.spark_job.spark_job_service.SparkJobService.delete_job',
           side_effect=[{'status': 200, 'message': 'pass for job4'},
                        {'status': 999, 'message': 'FAILED TO DELETE JOB8'}])
    @patch('PiezoWebApp.src.services.spark_job.spark_job_service.SparkJobService.write_logs_to_file',
           side_effect=[{'status': 200, 'message': 'pass for job4'},
                        {'status': 999, 'message': 'FAILED TO WRITE LOGS FOR JOB7'},
                        {'status': 200, 'message': 'pass for job8'}])
    @patch('PiezoWebApp.src.services.spark_job.spark_job_service.SparkJobService.get_jobs',
           return_value={"spark_jobs": {"job1": "RUNNING",
                                        "job2": "PENDING",
                                        "job3": "SUCCEEDED",
                                        "job4": "COMPLETED",
                                        "job5": "CrashLoopBackOff",
                                        "job6": "UNKNOWN",
                                        "job7": "FAILED",
                                        "job8": "COMPLETED"},
                         "status": 200})
    def test_tidy_jobs_skips_jobs_that_fail_to_process(self, get_jobs, write_logs, delete_job):
        # Act
        result = self.test_service.tidy_jobs()
        # Assert
        self.assertDictEqual(result, {'status': 200,
                                      'message': '8 Spark jobs found',
                                      'jobs_tidied': {'job4': 'COMPLETED'},
                                      'jobs_untouched': {'job1': 'RUNNING',
                                                         'job2': 'PENDING',
                                                         'job3': 'SUCCEEDED',
                                                         'job5': 'CrashLoopBackOff',
                                                         'job6': 'UNKNOWN'},
                                      'jobs_failed_to_process': {'job7': 'FAILED TO WRITE LOGS FOR JOB7',
                                                                 'job8': 'FAILED TO DELETE JOB8'}})
        get_jobs.assert_called_once_with(label=None)
        assert write_logs.call_count == 3
        write_logs.assert_any_call('job4')
        write_logs.assert_any_call('job7')  # Call where logs fail to be written
        write_logs.assert_any_call('job8')
        assert delete_job.call_count == 2
        delete_job.assert_any_call('job4')
        delete_job.assert_any_call('job8')
