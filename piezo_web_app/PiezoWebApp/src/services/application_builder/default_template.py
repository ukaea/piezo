class DefaultTemplate:

    def __init__(self):
        self._driver_cores = 0.1
        self._driver_core_limit = "200m"
        self._driver_memory = "512m"
        self._executors = 1
        self._executor_cores = 1
        self._executor_memory = "512m"

    def create_template(self):
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
                        "cores": self._driver_cores,
                        "coreLimit": self._driver_core_limit,
                        "memory": self._driver_memory,
                        "labels": {
                            "version": "2.4.0"},
                        "serviceAccount": "spark"},
                    "executor": {
                        "cores": self._executor_cores,
                        "instances": self._executors,
                        "memory": self._executor_memory,
                        "labels": {
                            "version": "2.4.0"}}}}
