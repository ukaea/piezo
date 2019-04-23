from logging import Logger
from unittest import TestCase

import mock
import pytest

from PiezoWebApp.src.services.kubernetes.i_kubernetes_adapter import IKubernetesAdapter
from PiezoWebApp.src.services.spark_job.i_spark_job_namer import ISparkJobNamer
from PiezoWebApp.src.services.spark_job.i_spark_ui_adapter import ISparkUiAdapter
from PiezoWebApp.src.services.spark_job.spark_ui_service import SparkUiService
from PiezoWebApp.src.services.spark_job.spark_job_service import SparkJobService
from PiezoWebApp.src.services.spark_job.validation.i_manifest_populator import IManifestPopulator
from PiezoWebApp.src.services.spark_job.validation.i_validation_service import IValidationService
from PiezoWebApp.src.services.storage.i_storage_service import IStorageService

NAMESPACE = 'default'


class TestSparkJobService(TestCase):
    # pylint: disable=attribute-defined-outside-init
    @pytest.fixture(autouse=True)
    def setup(self):
        self.mock_kubernetes_adapter = mock.create_autospec(IKubernetesAdapter)
        self.mock_logger = mock.create_autospec(Logger)
        self.mock_manifest_populator = mock.create_autospec(IManifestPopulator)
        self.mock_spark_job_namer = mock.create_autospec(ISparkJobNamer)
        self.mock_spark_ui_adapter = mock.create_autospec(ISparkUiAdapter)
        self.mock_spark_ui_service = SparkUiService(self.mock_kubernetes_adapter,
                                                    self.mock_spark_ui_adapter,
                                                    self.mock_logger)
        self.mock_storage_service = mock.create_autospec(IStorageService)
        self.mock_validation_service = mock.create_autospec(IValidationService)
        self.test_service = SparkJobService(
            self.mock_kubernetes_adapter,
            self.mock_logger,
            self.mock_manifest_populator,
            self.mock_spark_job_namer,
            self.mock_spark_ui_service,
            self.mock_storage_service,
            self.mock_validation_service
        )
