from PiezoWebApp.src.services.spark_job.validation.i_manifest_populator import IManifestPopulator
from PiezoWebApp.src.utils.dict_argument_helper import set_value_in_nested_dict


class ManifestPopulator(IManifestPopulator):
    def __init__(self, validation_rules):
        self._validation_rules = validation_rules
        self._api_version = self._validation_rules.get_default_value_for_key("apiVersion")
        self._kind = self._validation_rules.get_default_value_for_key("kind")
        self._metadata_name = self._validation_rules.get_default_value_for_key("name")
        self._metadata_namespace = self._validation_rules.get_default_value_for_key("namespace")
        self._spec_type = self._validation_rules.get_default_value_for_key("language")
        self._spec_mode = self._validation_rules.get_default_value_for_key("mode")
        self._spec_python_version = self._validation_rules.get_default_value_for_key("python_version")
        self._spec_image = self._validation_rules.get_default_value_for_key("image")
        self._spec_image_pull_policy = self._validation_rules.get_default_value_for_key("image_pull_policy")
        self._spec_main_app_file = self._validation_rules.get_default_value_for_key("path_to_main_app_file")
        self._spec_main_class = self._validation_rules.get_default_value_for_key("main_class")
        self._spec_spark_version = self._validation_rules.get_default_value_for_key("spark_version")
        self._spec_restart_policy_type = self._validation_rules.get_default_value_for_key("restart_policy")
        self._spec_driver_cores = self._validation_rules.get_default_value_for_key("driver_cores")
        self._spec_driver_core_limit = self._validation_rules.get_default_value_for_key("driver_core_limit")
        self._spec_driver_memory = self._validation_rules.get_default_value_for_key("driver_memory")
        self._spec_driver_label_version = self._validation_rules.get_default_value_for_key("spark_version")
        self._spec_driver_service_account = self._validation_rules.get_default_value_for_key("service_account")
        self._spec_executor_instances = self._validation_rules.get_default_value_for_key("executors")
        self._spec_executor_cores = self._validation_rules.get_default_value_for_key("executor_cores")
        self._spec_executor_memory = self._validation_rules.get_default_value_for_key("executor_memory")
        self._spec_executor_label_version = self._validation_rules.get_default_value_for_key("spark_version")

    def build_manifest(self, validated_parameters_dict):
        manifest = self._default_spark_application_manifest()
        for key in validated_parameters_dict:
            value = validated_parameters_dict[key]
            array_of_path = self._variable_to_manifest_path(key)
            self._add_value_to_manifest(array_of_path, manifest, value)
        return manifest

    @staticmethod
    def _add_value_to_manifest(array_of_path, manifest, value):
        return set_value_in_nested_dict(nested_dict=manifest, path=array_of_path, value=value)

    def _default_spark_application_manifest(self):
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
    def _variable_to_manifest_path(var):
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
