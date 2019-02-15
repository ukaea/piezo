import pytest

from PiezoWebApp.src.services.application_builder.builder import ApplicationBuilder


@pytest.fixture(autouse=True)
class TestApplicationBuilder:

    def setup(self):
        self.test_builder = ApplicationBuilder()


    def test_given_correctly_formed_body_builder_
