from PiezoWebApp.src.services.application_builder.argument_splitter import ArgumentSplitter


class ApplicationConstructor:

    def __init__(self):
        self._argument_splitter = ArgumentSplitter()

    def construct_application(self, application_arguments):
        metadata_arguments = self._argument_splitter.get_metadata_arguments(application_arguments)
        specs_arguments = self._argument_splitter.get_spec_arguments(application_arguments)

        metadata = self._construct_metadata(metadata_arguments)
        spec = self._construct_specs(specs_arguments)
        return {"apiVersion": "sparkoperator.k8s.io/v1beta1",
                "kind": "SparkApplication",
                "metadata": metadata,
                "spec": spec}

    @staticmethod
    def _construct_metadata(metadata_arguments):
        return {"name": metadata_arguments["name"],
                "namespace": metadata_arguments["namespace"]}

    def _construct_specs(self, specs_arguments):
        driver_arguments = self._argument_splitter.get_driver_arguments(specs_arguments)
        executor_arguments = self._argument_splitter.get_executor_arguments(specs_arguments)

        driver_specs = self._construct_driver_specs(driver_arguments)
        executor_specs = self._construct_executor_specs(executor_arguments)

        return {"some specs": "some_response",
                "driver": driver_specs,
                "executor": executor_specs}

    def _construct_driver_specs(self, driver_arguments):
        pass

    def _construct_executor_specs(self, executor_arguments):
        pass

