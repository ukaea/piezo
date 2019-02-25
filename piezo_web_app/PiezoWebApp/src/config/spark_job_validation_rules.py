from PiezoWebApp.src.models.spark_job_argument_classification import ArgumentClassification
from PiezoWebApp.src.models.validation_rule import ValidationRule

LANGUAGE_SPECIFIC_KEYS = {
    "Python": ["python_version"],
    "Scala": ["main_class"]
}

VALIDATION_RULES = {
    "apiVersion": ValidationRule(ArgumentClassification.Fixed, "sparkoperator.k8s.io/v1beta1"),
    "kind": ValidationRule(ArgumentClassification.Fixed, "SparkApplication"),
    "namespace": ValidationRule(ArgumentClassification.Fixed, "default"),
    "mode": ValidationRule(ArgumentClassification.Fixed, "cluster"),
    "image": ValidationRule(ArgumentClassification.Fixed, "gcr.io/spark-operator/spark:v2.4.0"),
    "image_pull_policy": ValidationRule(ArgumentClassification.Fixed, "Always"),
    "spark_version": ValidationRule(ArgumentClassification.Fixed, "2.4.0"),
    "restart_policy": ValidationRule(ArgumentClassification.Fixed, "Never"),
    "service_account": ValidationRule(ArgumentClassification.Fixed, "spark"),
    "name": ValidationRule(ArgumentClassification.Required, None),
    "language": ValidationRule(ArgumentClassification.Required, None, options=list(LANGUAGE_SPECIFIC_KEYS.keys())),
    "path_to_main_app_file": ValidationRule(ArgumentClassification.Required, None),
    "driver_cores": ValidationRule(ArgumentClassification.Optional, "0.1", minimum=0.1, maximum=1),
    "driver_core_limit": ValidationRule(ArgumentClassification.Optional, "0.2", minimum=0.2, maximum=1.2),
    "driver_memory": ValidationRule(ArgumentClassification.Optional, "512m", minimum=512, maximum=2048),
    "executors": ValidationRule(ArgumentClassification.Optional, "1", minimum=1, maximum=10),
    "executor_cores": ValidationRule(ArgumentClassification.Optional, "1", minimum=1, maximum=4),
    "executor_memory": ValidationRule(ArgumentClassification.Optional, "512m", minimum=512, maximum=4096),
    "main_class": ValidationRule(ArgumentClassification.Conditional, None),
    "python_version": ValidationRule(ArgumentClassification.Conditional, None)
}
