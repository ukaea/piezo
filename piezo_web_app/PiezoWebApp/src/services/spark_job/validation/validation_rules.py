from PiezoWebApp.src.models.spark_job_argument_classification import ArgumentClassification
from PiezoWebApp.src.models.validation_rule import ValidationRule


class ValidationRules:
    def __init__(self):
        self._validation_dict = {
            "apiVersion": ValidationRule("apiVersion", ArgumentClassification.Fixed, "sparkoperator.k8s.io/v1beta1"),
            "kind": ValidationRule("kind", ArgumentClassification.Fixed, "SparkApplication"),
            "namespace": ValidationRule("namespace", ArgumentClassification.Fixed, "default"),
            "mode": ValidationRule("mode", ArgumentClassification.Fixed, "cluster"),
            "image": ValidationRule("image", ArgumentClassification.Fixed, "gcr.io/spark-operator/spark:v2.4.0"),
            "image_pull_policy": ValidationRule("image_pull_policy", ArgumentClassification.Fixed, "Always"),
            "spark_version": ValidationRule("spark_version", ArgumentClassification.Fixed, "2.4.0"),
            "restart_policy": ValidationRule("restart_policy", ArgumentClassification.Fixed, "Never"),
            "service_account": ValidationRule("service_account", ArgumentClassification.Fixed, "spark"),
            "name": ValidationRule("name", ArgumentClassification.Required, None),
            "language": ValidationRule("language", ArgumentClassification.Required, None),
            "path_to_main_app_file": ValidationRule("path_to_main_app_file", ArgumentClassification.Required, None),
            "driver_cores": ValidationRule("driver_cores", ArgumentClassification.Optional, 0.1, 0.1, 0.1),
            "driver_core_limit": ValidationRule("driver_core_limit", ArgumentClassification.Optional, 0.2, 0.2, 1.2),
            "driver_memory": ValidationRule("driver_memory", ArgumentClassification.Optional, "512m", 512, 2048),
            "executors": ValidationRule("executors", ArgumentClassification.Optional, 1, 1, 10),
            "executor_cores": ValidationRule("executor_cores", ArgumentClassification.Optional, 1, 1, 4),
            "executor_memory": ValidationRule("executor_memory", ArgumentClassification.Optional, "512m", 512, 4096),
            "main_class": ValidationRule("main_class", ArgumentClassification.Conditional, None),
            "python_version": ValidationRule("python_version", ArgumentClassification.Conditional, None)
        }

    def get_validation_rule_for_key(self, key):
        return self._validation_dict[key]

    def get_keys_of_required_args(self):
        return [
            key for key in self._validation_dict
            if self._validation_dict[key].classification is ArgumentClassification.Required
        ]

    def get_keys_of_optional_args(self):
        return [
            key for key in self._validation_dict
            if self._validation_dict[key].classification is ArgumentClassification.Optional
        ]

    def get_default_value_for_key(self, key):
        validation_rule = self._validation_dict[key]
        return validation_rule.default
