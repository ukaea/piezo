FROM gitlab-registry.cern.ch/db/spark-service/docker-registry/spark:v2.4.0-hadoop3-0.7

# Setup for the Prometheus JMX exporter.
RUN mkdir -p /etc/metrics/conf
# Add the Prometheus JMX exporter Java agent jar for exposing metrics sent to the JmxSink to Prometheus.
ADD https://repo1.maven.org/maven2/io/prometheus/jmx/jmx_prometheus_javaagent/0.3.1/jmx_prometheus_javaagent-0.3.1.jar /prometheus/

COPY conf/prometheus.yaml /etc/metrics/conf/
COPY conf/metrics.properties /etc/metrics/conf/

ENTRYPOINT ["/opt/entrypoint.sh"]
