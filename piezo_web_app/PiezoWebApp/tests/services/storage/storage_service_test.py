from logging import Logger
from unittest import TestCase

import mock
import pytest

from PiezoWebApp.src.services.storage.adapters.i_storage_adapter import IStorageAdapter
from PiezoWebApp.src.services.storage.storage_service import StorageService
from PiezoWebApp.src.utils.configurations import Configuration


class TestStorageService(TestCase):
    @pytest.fixture(autouse=True)
    def setup(self):
        self.mock_logger = mock.create_autospec(Logger)
        self.mock_storage_adapter = mock.create_autospec(IStorageAdapter)

    def get_test_service(self):
        configuration = mock.create_autospec(Configuration)
        configuration.s3_bucket_name = 'test-bucket'
        configuration.temp_url_expiry_seconds = 10
        test_service = StorageService(
            configuration,
            self.mock_logger,
            self.mock_storage_adapter
        )
        return test_service

    def set_bucket_exists(self):
        self.mock_storage_adapter.does_bucket_exist.return_value = True

    def test_init_checks_bucket_exists(self):
        # Arrange
        self.set_bucket_exists()
        # Act
        self.get_test_service()
        # Assert
        self.mock_storage_adapter.does_bucket_exist.assert_called_once_with('test-bucket')
        self.mock_storage_adapter.create_bucket.assert_not_called()
        self.mock_logger.info.assert_called_once_with(
            'Bucket "test-bucket" already exists: no need to change')

    def test_init_creates_bucket_if_non_existent(self):
        # Arrange
        self.mock_storage_adapter.does_bucket_exist.return_value = False
        # Act
        self.get_test_service()
        # Assert
        self.mock_storage_adapter.does_bucket_exist.assert_called_once_with('test-bucket')
        self.mock_storage_adapter.create_bucket.assert_called_once_with('test-bucket')
        self.mock_logger.info.assert_called_once_with('Created new bucket "test-bucket"')

    def test_protocol_route_to_bucket_returns_expected_result(self):
        # Arrange
        self.mock_storage_adapter.access_protocol.return_value = 's3a'
        self.set_bucket_exists()
        test_service = self.get_test_service()
        # Act
        result = test_service.protocol_route_to_bucket()
        # Assert
        assert result == 's3a://test-bucket'

    def test_get_temp_url_for_each_file_returns_empty_dict_if_no_files(self):
        # Arrange
        self.set_bucket_exists()
        test_service = self.get_test_service()
        self.mock_storage_adapter.get_all_files.return_value = []
        # Act
        result = test_service.get_temp_url_for_each_file('outputs/test-job-abc12/')
        # Assert
        self.mock_storage_adapter.get_all_files.assert_called_once_with('test-bucket', 'outputs/test-job-abc12/')
        self.mock_storage_adapter.generate_temp_url.assert_not_called()
        assert result == {}

    def test_get_temp_url_for_each_file_returns_file_path_and_url_for_single_file(self):
        # Arrange
        self.set_bucket_exists()
        test_service = self.get_test_service()
        self.mock_storage_adapter.get_all_files.return_value = ['outputs/test-job-abc12/file1.txt']
        self.mock_storage_adapter.generate_temp_url.return_value = \
            'http://s3.com/test-bucket/outputs/test-job-abc12/file1.txt'
        # Act
        result = test_service.get_temp_url_for_each_file('outputs/test-job-abc12/')
        # Assert
        self.mock_storage_adapter.get_all_files.assert_called_once_with('test-bucket', 'outputs/test-job-abc12/')
        self.mock_storage_adapter.generate_temp_url.assert_called_once_with(
            'test-bucket', 'outputs/test-job-abc12/file1.txt', 10, 'GET')
        self.assertDictEqual(result, {
            'outputs/test-job-abc12/file1.txt': 'http://s3.com/test-bucket/outputs/test-job-abc12/file1.txt'
        })

    def test_get_temp_url_for_each_file_returns_file_path_and_url_for_multiple_files(self):
        # Arrange
        self.set_bucket_exists()
        test_service = self.get_test_service()
        self.mock_storage_adapter.get_all_files.return_value = [
            'outputs/test-job-abc12/file1.txt',
            'outputs/test-job-abc12/file2.txt',
            'outputs/test-job-abc12/file3.txt'
        ]
        self.mock_storage_adapter.generate_temp_url.side_effect = [
            'http://s3.com/test-bucket/outputs/test-job-abc12/file1.txt',
            'http://s3.com/test-bucket/outputs/test-job-abc12/file2.txt',
            'http://s3.com/test-bucket/outputs/test-job-abc12/file3.txt'
        ]
        # Act
        result = test_service.get_temp_url_for_each_file('outputs/test-job-abc12/')
        # Assert
        self.mock_storage_adapter.get_all_files.assert_called_once_with('test-bucket', 'outputs/test-job-abc12/')
        self.mock_storage_adapter.generate_temp_url.assert_has_calls([
            mock.call('test-bucket', 'outputs/test-job-abc12/file1.txt', 10, 'GET'),
            mock.call('test-bucket', 'outputs/test-job-abc12/file2.txt', 10, 'GET'),
            mock.call('test-bucket', 'outputs/test-job-abc12/file3.txt', 10, 'GET')
        ])
        self.assertDictEqual(result, {
            'outputs/test-job-abc12/file1.txt': 'http://s3.com/test-bucket/outputs/test-job-abc12/file1.txt',
            'outputs/test-job-abc12/file2.txt': 'http://s3.com/test-bucket/outputs/test-job-abc12/file2.txt',
            'outputs/test-job-abc12/file3.txt': 'http://s3.com/test-bucket/outputs/test-job-abc12/file3.txt'
        })

    def test_set_contents_from_string_calls_adapter_and_logs_size(self):
        # Arrange
        self.set_bucket_exists()
        test_service = self.get_test_service()
        self.mock_storage_adapter.set_contents_from_string.return_value = 12345
        # Act
        test_service.set_contents_from_string('outputs/test-job-abc12/log.txt', 'Message')
        # Assert
        self.mock_storage_adapter.set_contents_from_string.assert_called_once_with(
            'test-bucket', 'outputs/test-job-abc12/log.txt', 'Message'
        )
        self.mock_logger.debug.assert_called_once_with('Wrote 12345 bytes to "outputs/test-job-abc12/log.txt"')
