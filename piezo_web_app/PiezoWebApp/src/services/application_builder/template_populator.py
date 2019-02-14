class TemplatePopulator:

    def build_template(self, validated_parameters_dict):
        template = self.default_template()
        template["metadata"]["name"] = validated_parameters_dict["name"]
        template["spec"]["mainApplicationFile"] = validated_parameters_dict["path_to_main_application_file"]
        template["spec"]["driver"]["cores"] = validated_parameters_dict["driver_cores"]
        template["spec"]["driver"]["coreLimit"] = validated_parameters_dict["driver_core_limit"]
        template["spec"]["driver"]["memory"] = validated_parameters_dict["driver_memory"]
        template["spec"]["executor"]["instances"] = validated_parameters_dict["executors"]
        template["spec"]["executor"]["cores"] = validated_parameters_dict["executor_cores"]
        template["spec"]["executor"]["memory"] = validated_parameters_dict["executor_memory"]

        if validated_parameters_dict["language"].lower() == "python":
            return self._populate_python_job_template(template, validated_parameters_dict)
        if validated_parameters_dict["language"].lower() == "scala"
            return self._populate_scala_job_template(template, validated_parameters_dict)
        else:
            raise ValueError(
                f"Invalid language {validated_parameters_dict['language']} chosen, please use one of [Python, Scala]")

    @staticmethod
    def _populate_python_job_template(template, validated_parameters_dict):
        template["spec"]["type"] = "Python"
        template["spec"]["pythonVersion"] = validated_parameters_dict["pythonVersion"]
        return template

    @staticmethod
    def _populate_scala_job_template(template, validated_parameters_dict):
        template["spec"]["type"] = "Scala"
        template["spec"]["mainClass"] = validated_parameters_dict["main_class"]
        return template

    @staticmethod
    def default_template():
        return {"apiVersion": "sparkoperator.k8s.io/v1beta1",
                "kind": "SparkApplication",
                "metadata":
                    {"name": None,
                     "namespace": "default"},
                "spec": {
                    "type": None,
                    "mode": "cluster",
                    "image": "gcr.io/spark-operator/spark:v2.4.0",
                    "imagePullPolicy": "Always",
                    "mainApplicationFile": None,
                    "sparkVersion": "2.4.0",
                    "restartPolicy": {
                        "type": "Never"},
                    "driver": {
                        "cores": 0.1,
                        "coreLimit": "200m",
                        "memory": "512m",
                        "labels": {
                            "version": "2.4.0"},
                        "serviceAccount": "spark"},
                    "executor": {
                        "cores": 1,
                        "instances": 1,
                        "memory": "512m",
                        "labels": {
                            "version": "2.4.0"}}}}
