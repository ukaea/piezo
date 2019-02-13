from PiezoWebApp.src.services.application_constructor.argument_splitter import get_metadata_arguments
from PiezoWebApp.src.services.application_constructor.argument_splitter import get_spec_arguments


def construct_application(application_arguments):
    metadata_arguments = get_metadata_arguments(application_arguments)
    specs_arguments = get_spec_arguments(application_arguments)

    metadata = _construct_metadata(metadata_arguments)
    spec = _construct_specs(specs_arguments)
    return {"apiVersion": "sparkoperator.k8s.io/v1beta1",
            "kind": "SparkApplication",
            "metadata": metadata,
            "spec": spec}


def _construct_metadata(metadata_arguments):
    return {"name": metadata_arguments["name"],
            "namespace": metadata_arguments["namespace"]}

def _construct_specs(specs_arguments):
    pass

def _construct_driver_specs(specs_arguments):
    pass

def _construct_executor_specs(specs_arguments):
    pass
