class ValidationRules:

    def __init__(self):
        """
        Validation rules are provided in a dictionary where each key maps to an array of validation values
        in the format:
        [min, max, default, format]
        format takes the following values: [base, optional, required, conditional]:
            * base: required in all application and set by default, can't be declared by user
            * required: Required in all application, no default value and must be declared by user
            * optional: Either optional to application or default value exists, optionally declared by user
            * conditional: Not used unless other properties match specific criteria
        """
        self._validation_dict = {"apiVersion": [None, None, "sparkoperator.k8s.io/v1beta1", "base"],
                                 "kind": [None, None, "SparkApplication", "base"],
                                 "namespace": [None, None, "default", "base"],
                                 "mode": [None, None, "cluster", "base"],
                                 "image": [None, None, "gcr.io/spark-operator/spark:v2.4.0", "base"],
                                 "image_pull_policy": [None, None, "Always", "base"],
                                 "spark_version": [None, None, "2.4.0", "base"],
                                 "restart_policy": [None, None, "Never", "base"],
                                 "service_account": [None, None, "spark", "base"],
                                 "name": [None, None, None, "required"],
                                 "language": [None, None, None, "required"],
                                 "path_to_main_app_file": [None, None, None, "optional"],
                                 "driver_cores": [0.1, 1, 0.1, "optional"],
                                 "driver_core_limit": [0.2, 1.2, 0.2, "optional"],
                                 "driver_memory": [512, 2048, 512, "optional"],
                                 "executors": [1, 10, 1, "optional"],
                                 "executor_cores": [1, 4, 1, "optional"],
                                 "executor_memory": [512, 4096, 512, "optional"],
                                 "main_class": [None, None, None, "conditional"],
                                 "python_version": [None, None, None, "conditional"]
                                 }

    def get_property_array_for_key(self, key):
        return self._validation_dict[key]

    def get_keys_of_required_args(self):
        return [key for key in self._validation_dict if self._validation_dict[key][3] == "required"]

    def get_keys_of_optional_args(self):
        return [key for key in self._validation_dict if self._validation_dict[key][3] == "optional"]

    def get_default_value_for_key(self, key):
        return self._validation_dict[key][2]
