from tornado_json import schema

from PiezoWebApp.src.handlers.base_handler import BaseHandler
from PiezoWebApp.src.handlers.schema.schema_helpers import create_object_schema_with_string_properties


# pylint: disable=abstract-method
class GetLogsHandler(BaseHandler):
    @schema.validate(
        input_schema=create_object_schema_with_string_properties(
            ['driver_name', 'namespace'], required=['driver_name', 'namespace']),
        input_example={
            'driver_name': 'example-driver',
            'namespace': 'default'
        }
    )
    def get(self, *args, **kwargs):
        driver_name = self.get_body_attribute('driver_name', required=True)
        namespace = self.get_body_attribute('namespace', required=True)
        self._logger.debug(f'Trying to delete driver "{driver_name}" in namespace "{namespace}".')
        result = self._kubernetes_service.get_logs(driver_name, namespace)
        self._logger.debug(f'Getting logs from driver "{driver_name}" in namespace "{namespace}" '
                           f'returned result "{result}".')
        return result
