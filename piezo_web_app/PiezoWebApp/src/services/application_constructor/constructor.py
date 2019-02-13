class Constructor:

    def __init__(self, template):
        self._manifest = template

    def construct_application(self, application_arguments):
        pass

    def construct_metadata(self, metadata_arguments):
        pass

    def construct_specs(self, specs_arguments):
        pass

    def configure_driver_specs(self, specs_arguments):
        pass

    def configure_executor_specs(self, specs_arguments):
        pass
