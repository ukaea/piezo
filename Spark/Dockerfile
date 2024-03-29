FROM gitlab-registry.cern.ch/db/spark-service/docker-registry/spark:v2.4.0-hadoop3-0.7

# Install python 3
RUN yum install -y centos-release-scl-rh && \
    yum-config-manager --enable centos-sclo-rh-testing && \
    INSTALL_PKGS="rh-python36 rh-python36-python-pip" &&\
    yum install -y --setopt=tsflags=nodocs --enablerepo=centosplus $INSTALL_PKGS && \
    rpm -V $INSTALL_PKGS && \
    yum clean all -y
    
# Add python3 to path
ENV PATH="/opt/rh/rh-python36/root/usr/bin:${PATH}"

# Setup for the Prometheus JMX exporter.
RUN mkdir -p /etc/metrics/conf

# Add the Prometheus JMX exporter Java agent jar for exposing metrics sent to the JmxSink to Prometheus.
ADD https://repo1.maven.org/maven2/io/prometheus/jmx/jmx_prometheus_javaagent/0.3.1/jmx_prometheus_javaagent-0.3.1.jar /prometheus/

COPY conf/prometheus.yaml /etc/metrics/conf/
COPY conf/metrics.properties /etc/metrics/conf/

ENTRYPOINT ["/opt/entrypoint.sh"]
