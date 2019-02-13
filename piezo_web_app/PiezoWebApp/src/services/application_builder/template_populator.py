class TemplatePopulator:

    def build_template(self, validated_arguments):
        if validated_arguments["language"] == "Python":
            return self.populate_python_job_template(validated_arguments)
        return self.populate_scala_job_template(validated_arguments)

    @staticmethod
    def populate_python_job_template(validated_arguments):
        template = {"apiVersion": "sparkoperator.k8s.io/v1beta1",
                    "kind": "SparkApplication",
                    "metadata":
                        {"name": validated_arguments["name"],
                         "namespace": "default"},
                    "spec": {
                        "type": "Python",
                        "pythonVersion": validated_arguments["pythonVersion"],
                        "mode": "cluster",
                        "image": "gcr.io/spark-operator/spark:v2.4.0",
                        "imagePullPolicy": "Always",
                        "mainApplicationFile": validated_arguments["path_to_main_application_file"],
                        "sparkVersion": "2.4.0",
                        "restartPolicy": {
                            "type": "Never"},
                        "driver": {
                            "cores": validated_arguments["driver_cores"],
                            "coreLimit": validated_arguments["driver_core_limit"],
                            "memory": validated_arguments["driver_memory"],
                            "labels": {
                                "version": "2.4.0"},
                            "serviceAccount": "spark"},
                        "executor": {
                            "cores": validated_arguments["executor_cores"],
                            "instances": validated_arguments["executors"],
                            "memory": validated_arguments["executor_memory"],
                            "labels": {
                                "version": "2.4.0"}}}}
        return template

    @staticmethod
    def populate_scala_job_template(validated_arguments):
        template = {"apiVersion": "sparkoperator.k8s.io/v1beta1",
                    "kind": "SparkApplication",
                    "metadata":
                        {"name": validated_arguments["name"],
                         "namespace": "default"},
                    "spec": {
                        "type": "Scala",
                        "mode": "cluster",
                        "image": "gcr.io/spark-operator/spark:v2.4.0",
                        "imagePullPolicy": "Always",
                        "mainApplicationFile": validated_arguments["path_to_main_application_file"],
                        "mainClass": validated_arguments["main_class"],
                        "sparkVersion": "2.4.0",
                        "restartPolicy": {
                            "type": "Never"},
                        "driver": {
                            "cores": validated_arguments["driver_cores"],
                            "coreLimit": validated_arguments["driver_core_limit"],
                            "memory": validated_arguments["driver_memory"],
                            "labels": {
                                "version": "2.4.0"},
                            "serviceAccount": "spark"},
                        "executor": {
                            "cores": validated_arguments["executor_cores"],
                            "instances": validated_arguments["executors"],
                            "memory": validated_arguments["executor_memory"],
                            "labels": {
                                "version": "2.4.0"}}}}
        return template
