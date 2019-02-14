class ManifestPopulator:

    def build_manifest(self, validated_parameters_dict):
        manifest = self.default_spark_application_manifest()
        manifest["metadata"]["name"] = validated_parameters_dict["name"]
        manifest["spec"]["mainApplicationFile"] = validated_parameters_dict["path_to_main_application_file"]
        manifest["spec"]["driver"]["cores"] = validated_parameters_dict["driver_cores"]
        manifest["spec"]["driver"]["coreLimit"] = validated_parameters_dict["driver_core_limit"]
        manifest["spec"]["driver"]["memory"] = validated_parameters_dict["driver_memory"]
        manifest["spec"]["executor"]["instances"] = validated_parameters_dict["executors"]
        manifest["spec"]["executor"]["cores"] = validated_parameters_dict["executor_cores"]
        manifest["spec"]["executor"]["memory"] = validated_parameters_dict["executor_memory"]

        if validated_parameters_dict["language"].lower() == "python":
            return self._populate_python_job_manifest(manifest, validated_parameters_dict)
        if validated_parameters_dict["language"].lower() == "scala":
            return self._populate_scala_job_manifest(manifest, validated_parameters_dict)
        else:
            raise ValueError(
                f"Invalid language {validated_parameters_dict['language']} chosen, please use one of [Python, Scala]")

    @staticmethod
    def _populate_python_job_manifest(manifest, validated_parameters_dict):
        manifest["spec"]["type"] = "Python"
        manifest["spec"]["pythonVersion"] = validated_parameters_dict["pythonVersion"]
        return manifest

    @staticmethod
    def _populate_scala_job_manifest(manifest, validated_parameters_dict):
        manifest["spec"]["type"] = "Scala"
        manifest["spec"]["mainClass"] = validated_parameters_dict["main_class"]
        return manifest

    @staticmethod
    def default_spark_application_manifest():
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
