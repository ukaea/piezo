from PiezoWebApp.src.utils.dict_argument_helper import set_value_in_nested_dict


class ManifestPopulator:

    def __init__(self):
        self._api_version = "sparkoperator.k8s.io/v1beta1"
        self._kind = "SparkApplication"
        self._metadata_name = None
        self._metadata_namespace = "default"
        self._spec_type = None
        self._spec_mode = "cluster"
        self._spec_type = "Python"
        self._spec_python_version = "2"
        self._spec_image = "gcr.io/spark-operator/spark:v2.4.0"
        self._spec_image_pull_policy = "Always"
        self._spec_main_app_file = None
        self._spec_main_class = None
        self._spec_spark_version = "2.4.0"
        self._spec_restart_policy_type = "Never"
        self._spec_driver_cores = 0.1
        self._spec_driver_core_limit = "200m"
        self._spec_driver_memory = "512m"
        self._spec_driver_label_version = "2.4.0"
        self._spec_driver_service_account = "spark"
        self._spec_executor_instances = 1
        self._spec_executor_cores = 1
        self._spec_executor_memory = "512m"
        self._spec_executor_label_version = "2.4.0"

    @staticmethod
    def add_value_to_manifest(array_of_path, manifest, value):
        return set_value_in_nested_dict(nested_dict=manifest, path=array_of_path, value=value)

    def build_manifest(self, validated_parameters_dict):
        manifest = self.default_spark_application_manifest()
        for key in validated_parameters_dict:
            value = validated_parameters_dict[key]
            array_of_path = ManifestPopulator.variable_to_manifest_path(key)
            ManifestPopulator.add_value_to_manifest(array_of_path, manifest, value)
        return manifest

    def default_spark_application_manifest(self):
        return {"apiVersion": self._api_version,
                "kind": self._kind,
                "metadata":
                    {"name": self._metadata_name,
                     "namespace": self._metadata_namespace},
                "spec": {
                    "mode": self._spec_mode,
                    "image": self._spec_image,
                    "imagePullPolicy": self._spec_image_pull_policy,
                    "mainApplicationFile": self._spec_main_app_file,
                    "sparkVersion": self._spec_spark_version,
                    "restartPolicy": {
                        "type": self._spec_restart_policy_type},
                    "driver": {
                        "cores": self._spec_driver_cores,
                        "coreLimit": self._spec_driver_core_limit,
                        "memory": self._spec_driver_memory,
                        "labels": {
                            "version": self._spec_driver_label_version},
                        "serviceAccount": self._spec_driver_service_account},
                    "executor": {
                        "cores": self._spec_executor_cores,
                        "instances": self._spec_executor_instances,
                        "memory": self._spec_executor_memory,
                        "labels": {
                            "version": self._spec_executor_label_version}}}}

    @staticmethod
    def variable_to_manifest_path(var):
        var_to_path_dict = {"name": ["metadata", "name"],
                            "language": ["spec", "type"],
                            "python_version": ["spec", "pythonVersion"],
                            "main_class": ["spec", "mainClass"],
                            "path_to_main_app_file": ["spec", "mainApplicationFile"],
                            "driver_cores": ["spec", "driver", "cores"],
                            "driver_core_limit": ["spec", "driver", "coreLimit"],
                            "driver_memory": ["spec", "driver", "memory"],
                            "executors": ["spec", "executor", "instances"],
                            "executor_cores": ["spec", "executor", "cores"],
                            "executor_memory": ["spec", "executor", "memory"]
                            }
        return var_to_path_dict[var]
