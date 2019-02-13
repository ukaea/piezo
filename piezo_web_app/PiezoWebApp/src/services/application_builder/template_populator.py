class TemplatePopulator:

    @staticmethod
    def populate_python_job_template(validated_arguments):
        return {"apiVersion": "sparkoperator.k8s.io/v1beta1", \
                "kind": "SparkApplication", \
                "metadata": \
                    {"name": "spark-pi", \
                     "namespace": "default"}, \
                "spec": { \
                    "type": "Scala", \
                    "mode": "cluster", \
                    "image": "gcr.io/spark-operator/spark:v2.4.0", \
                    "imagePullPolicy": "Always", \
                    "mainClass": "org.apache.spark.examples.SparkPi", \
                    "mainApplicationFile": "local:///opt/spark/examples/jars/spark-examples_2.11-2.4.0.jar", \
                    "sparkVersion": "2.4.0", \
                    "restartPolicy": { \
                        "type": "Never"}, \
                    "driver": { \
                        "cores": 0.1, \
                        "coreLimit": "200m", \
                        "memory": "512m", \
                        "labels": { \
                            "version": "2.4.0"}, \
                        "serviceAccount": "spark"}, \
                    "executor": { \
                        "cores": 1, \
                        "instances": 2, \
                        "memory": "512m", \
                        "labels": { \
                            "version": "2.4.0"}}}}

    @staticmethod
    def populate_scala_job_template(validated_arguments):
        return {"apiVersion": "sparkoperator.k8s.io/v1beta1", \
                "kind": "SparkApplication", \
                "metadata": \
                    {"name": "spark-pi", \
                     "namespace": "default"}, \
                "spec": { \
                    "type": "Scala", \
                    "mode": "cluster", \
                    "image": "gcr.io/spark-operator/spark:v2.4.0", \
                    "imagePullPolicy": "Always", \
                    "mainClass": "org.apache.spark.examples.SparkPi", \
                    "mainApplicationFile": "local:///opt/spark/examples/jars/spark-examples_2.11-2.4.0.jar", \
                    "sparkVersion": "2.4.0", \
                    "restartPolicy": { \
                        "type": "Never"}, \
                    "driver": { \
                        "cores": 0.1, \
                        "coreLimit": "200m", \
                        "memory": "512m", \
                        "labels": { \
                            "version": "2.4.0"}, \
                        "serviceAccount": "spark"}, \
                    "executor": { \
                        "cores": 1, \
                        "instances": 2, \
                        "memory": "512m", \
                        "labels": { \
                            "version": "2.4.0"}}}}