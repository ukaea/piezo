from PiezoWebApp.src.models.validation_rule import ValidationRule

LANGUAGE_SPECIFIC_KEYS = {
    "Python": ["python_version"],
    "Scala": ["main_class"]
}

VALIDATION_RULES = {
    "apiVersion": ValidationRule({"classification": "Fixed", "default": "sparkoperator.k8s.io/v1beta1"}),
    "kind": ValidationRule({"classification": "Fixed", "default": "SparkApplication"}),
    "namespace": ValidationRule({"classification": "Fixed", "default": "default"}),
    "mode": ValidationRule({"classification": "Fixed", "default": "cluster"}),
    "image": ValidationRule({"classification": "Fixed", "default": "gcr.io/spark-operator/spark:v2.4.0"}),
    "image_pull_policy": ValidationRule({"classification": "Fixed", "default": "Always"}),
    "spark_version": ValidationRule({"classification": "Fixed", "default": "2.4.0"}),
    "restart_policy": ValidationRule({"classification": "Fixed", "default": "Never"}),
    "service_account": ValidationRule({"classification": "Fixed", "default": "spark"}),
    "name": ValidationRule({"classification": "Required"}),
    "language": ValidationRule({"classification": "Required", "options": list(LANGUAGE_SPECIFIC_KEYS.keys())}),
    "path_to_main_app_file": ValidationRule({"classification": "Required"}),
    "driver_cores": ValidationRule({"classification": "Optional", "default": 0.1, "minimum": 0.1, "maximum": 1}),
    "driver_memory": ValidationRule({"classification": "Optional", "default": "512m", "minimum": 512, "maximum": 2048}),
    "executors": ValidationRule({"classification": "Optional", "default": 1, "minimum": 1, "maximum": 10}),
    "executor_cores": ValidationRule({"classification": "Optional", "default": 1, "minimum": 1, "maximum": 4}),
    "executor_memory": ValidationRule({"classification": "Optional", "default": "512m", "minimum": 512, "maximum": 4096}),
    "main_class": ValidationRule({"classification": "Conditional"}),
    "python_version": ValidationRule({"classification": "Conditional", "options": ["2", "3"]})
}
