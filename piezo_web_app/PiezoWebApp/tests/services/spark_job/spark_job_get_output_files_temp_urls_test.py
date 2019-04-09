from PiezoWebApp.tests.services.spark_job.spark_job_service_test import TestSparkJobService


class SparkJobServiceGetOutputFilesTempUrlsTest(TestSparkJobService):
    def test_get_output_files_temp_urls_returns_single_file_temp_url(self):
        # Arrange
        self.mock_storage_adapter.get_temp_url_for_each_file.return_value = {
            'log.txt': 's3://log.txt.temp.url'
        }
        # Act
        result = self.test_service.get_output_files_temp_urls('test-job-abc12')
        # Assert
        self.assertDictEqual(result, {
            'status': 200,
            'message': 'Got temporary URLs for 1 output files for job "test-job-abc12"',
            'files': {'log.txt': 's3://log.txt.temp.url'}
        })
        self.mock_logger.debug.assert_called_once_with('Got temporary URLs for 1 output files for job "test-job-abc12"')
        self.mock_storage_adapter.get_temp_url_for_each_file.assert_called_once_with(
            'kubernetes',
            'outputs/test-job-abc12/'
        )

    def test_get_output_files_temp_urls_returns_empty_dictionary_when_no_files(self):
        # Arrange
        self.mock_storage_adapter.get_temp_url_for_each_file.return_value = {}
        # Act
        result = self.test_service.get_output_files_temp_urls('test-job-abc12')
        # Assert
        self.assertDictEqual(result, {
            'status': 404,
            'message': 'Got temporary URLs for 0 output files for job "test-job-abc12"',
            'files': {}
        })
        self.mock_logger.debug.assert_called_once_with('Got temporary URLs for 0 output files for job "test-job-abc12"')
        self.mock_storage_adapter.get_temp_url_for_each_file.assert_called_once_with(
            'kubernetes',
            'outputs/test-job-abc12/'
        )

    def test_get_output_files_temp_urls_returns_multiple_files_temp_urls(self):
        # Arrange
        self.mock_storage_adapter.get_temp_url_for_each_file.return_value = {
            'log.txt': 's3://log.txt.temp.url',
            'output1.csv': 's3://output1.csv.temp.url',
            'output2.csv': 's3://output2.csv.temp.url'
        }
        # Act
        result = self.test_service.get_output_files_temp_urls('test-job-abc12')
        # Assert
        self.assertDictEqual(result, {
            'status': 200,
            'message': 'Got temporary URLs for 3 output files for job "test-job-abc12"',
            'files': {
                'log.txt': 's3://log.txt.temp.url',
                'output1.csv': 's3://output1.csv.temp.url',
                'output2.csv': 's3://output2.csv.temp.url'
            }
        })
        self.mock_logger.debug.assert_called_once_with('Got temporary URLs for 3 output files for job "test-job-abc12"')
        self.mock_storage_adapter.get_temp_url_for_each_file.assert_called_once_with(
            'kubernetes',
            'outputs/test-job-abc12/'
        )
