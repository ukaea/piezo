import os


string = str('apiVersion: \"sparkoperator.k8s.io/v1alpha1\"\n\
kind: SparkApplication\nmetadata:\n\
  name: spark-pi\n\
  namespace: default\n\
spec:\n\
  type: Scala\n\
  mode: cluster\n\
  image: \"gcr.io/spark-operator/spark:v2.4.0\"\n\
  imagePullPolicy: Always\n\
  mainClass: org.apache.spark.examples.SparkPi\n\
  mainApplicationFile: \"local:///opt/spark/examples/jars/spark-examples_2.11-2.4.0.jar\"\n\
  restartPolicy:\n\
    type: Never\n\
  driver:\n\
    cores: 0.1\n\
    coreLimit: \"200m\"\n\
    memory: \"512m\"\n\
    labels:\n\
      version: 2.4.0\n\
    serviceAccount: spark\n\
  executor:\n\
    cores: 1\n\
    instances: 1\n\
    memory: \"512m\"\n\
    labels:\n\
      version: 2.4.0')


def run_job():
  #print(f'{string} | kubectl apply -f -')
  os.system("echo '{}' | kubectl apply -f -".format(string))
