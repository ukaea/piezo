from PiezoWebApp.src.services.application_builder.manifest_populator import ManifestPopulator


class ApplicationBuilder:
    def __init__(self):
        self._manifest_populator = ManifestPopulator()

    def build_application_definition(self, request_body):
        return self._manifest_populator.build_manifest(request_body)
