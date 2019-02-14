class TemplatePopulator:

    def build_template(self, validated_parameters_dict):
        if validated_parameters_dict["language"].lower() == "python":
            return self.populate_python_job_template(validated_parameters_dict)
        return self.populate_scala_job_template(validated_parameters_dict)

    @staticmethod
    def _populate_python_job_template(validated_parameters_dict):
        template = {"apiVersion": "sparkoperator.k8s.io/v1beta1",
                    "kind": "SparkApplication",
                    "metadata":
                        {"name": validated_parameters_dict["name"],
                         "namespace": "default"},
                    "spec": {
                        "type": "Python",
                        "pythonVersion": validated_parameters_dict["pythonVersion"],
                        "mode": "cluster",
                        "image": "gcr.io/spark-operator/spark:v2.4.0",
                        "imagePullPolicy": "Always",
                        "mainApplicationFile": validated_parameters_dict["path_to_main_application_file"],
                        "sparkVersion": "2.4.0",
                        "restartPolicy": {
                            "type": "Never"},
                        "driver": {
                            "cores": validated_parameters_dict["driver_cores"],
                            "coreLimit": validated_parameters_dict["driver_core_limit"],
                            "memory": validated_parameters_dict["driver_memory"],
                            "labels": {
                                "version": "2.4.0"},
                            "serviceAccount": "spark"},
                        "executor": {
                            "cores": validated_parameters_dict["executor_cores"],
                            "instances": validated_parameters_dict["executors"],
                            "memory": validated_parameters_dict["executor_memory"],
                            "labels": {
                                "version": "2.4.0"}}}}
        return template

    @staticmethod
    def _populate_scala_job_template(validated_paramters_dict):
        template = {"apiVersion": "sparkoperator.k8s.io/v1beta1",
                    "kind": "SparkApplication",
                    "metadata":
                        {"name": validated_paramters_dict["name"],
                         "namespace": "default"},
                    "spec": {
                        "type": "Scala",
                        "mode": "cluster",
                        "image": "gcr.io/spark-operator/spark:v2.4.0",
                        "imagePullPolicy": "Always",
                        "mainApplicationFile": validated_paramters_dict["path_to_main_application_file"],
                        "mainClass": validated_paramters_dict["main_class"],
                        "sparkVersion": "2.4.0",
                        "restartPolicy": {
                            "type": "Never"},
                        "driver": {
                            "cores": validated_paramters_dict["driver_cores"],
                            "coreLimit": validated_paramters_dict["driver_core_limit"],
                            "memory": validated_paramters_dict["driver_memory"],
                            "labels": {
                                "version": "2.4.0"},
                            "serviceAccount": "spark"},
                        "executor": {
                            "cores": validated_paramters_dict["executor_cores"],
                            "instances": validated_paramters_dict["executors"],
                            "memory": validated_paramters_dict["executor_memory"],
                            "labels": {
                                "version": "2.4.0"}}}}
        return template
