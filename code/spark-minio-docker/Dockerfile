#
# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

# Download base image
ARG SPARK_IMAGE=gcr.io/spark-operator/spark:v2.4.0
FROM ${SPARK_IMAGE}

# Setup dependencies for Google Cloud Storage access.
#RUN rm $SPARK_HOME/jars/guava-14.0.1.jar
#ADD http://central.maven.org/maven2/com/google/guava/guava/23.0/guava-23.0.jar $SPARK_HOME/jars


RUN mkdir /Hadoop
ADD http://ftp.jaist.ac.jp/pub/apache/hadoop/common/hadoop-3.0.3/hadoop-3.0.3.tar.gz /Hadoop
RUN cd /Hadoop/ && tar -xzf hadoop-3.0.3.tar.gz && rm hadoop-3.0.3.tar.gz
RUN bash -c "ls /Hadoop/"
RUN bash -c "ls /Hadoop/hadoop-3.0.3/"
RUN bash -c "ls /Hadoop/hadoop-3.0.3/etc/"
RUN bash -c "ls /Hadoop/hadoop-3.0.3/etc/hadoop/"
ENV HADOOP_HOME=/Hadoop/hadoop-3.0.3/
# Update hadoop
RUN rm $SPARK_HOME/jars/hadoop-auth-2.7.3.jar
RUN rm $SPARK_HOME/jars/hadoop-client-2.7.3.jar
RUN rm $SPARK_HOME/jars/hadoop-common-2.7.3.jar
RUN rm $SPARK_HOME/jars/hadoop-hdfs-2.7.3.jar
RUN rm $SPARK_HOME/jars/hadoop-mapreduce-client-app-2.7.3.jar
RUN rm $SPARK_HOME/jars/hadoop-mapreduce-client-common-2.7.3.jar
RUN rm $SPARK_HOME/jars/hadoop-mapreduce-client-core-2.7.3.jar
RUN rm $SPARK_HOME/jars/hadoop-mapreduce-client-jobclient-2.7.3.jar
RUN rm $SPARK_HOME/jars/hadoop-mapreduce-client-shuffle-2.7.3.jar
RUN rm $SPARK_HOME/jars/hadoop-yarn-api-2.7.3.jar
RUN rm $SPARK_HOME/jars/hadoop-yarn-client-2.7.3.jar
RUN rm $SPARK_HOME/jars/hadoop-yarn-common-2.7.3.jar
RUN rm $SPARK_HOME/jars/hadoop-yarn-server-common-2.7.3.jar
RUN rm $SPARK_HOME/jars/hadoop-yarn-server-web-proxy-2.7.3.jar

ADD http://central.maven.org/maven2/org/apache/hadoop/hadoop-auth/3.0.3/hadoop-auth-3.0.3.jar $SPARK_HOME/jars
ADD http://central.maven.org/maven2/org/apache/hadoop/hadoop-client/3.0.3/hadoop-client-3.0.3.jar $SPARK_HOME/jars
ADD http://central.maven.org/maven2/org/apache/hadoop/hadoop-common/3.0.3/hadoop-common-3.0.3.jar $SPARK_HOME/jars
ADD http://central.maven.org/maven2/org/apache/hadoop/hadoop-hdfs/3.0.3/hadoop-hdfs-3.0.3.jar $SPARK_HOME/jars
ADD http://central.maven.org/maven2/org/apache/hadoop/hadoop-mapreduce-client-app/3.0.3/hadoop-mapreduce-client-app-3.0.3.jar $SPARK_HOME/jars
ADD http://central.maven.org/maven2/org/apache/hadoop/hadoop-mapreduce-client-common/3.0.3/hadoop-mapreduce-client-common-3.0.3.jar $SPARK_HOME/jars
ADD http://central.maven.org/maven2/org/apache/hadoop/hadoop-mapreduce-client-core/3.0.3/hadoop-mapreduce-client-core-3.0.3.jar $SPARK_HOME/jars
ADD http://central.maven.org/maven2/org/apache/hadoop/hadoop-mapreduce-client-jobclient/3.0.3/hadoop-mapreduce-client-jobclient-3.0.3.jar $SPARK_HOME/jars
ADD http://central.maven.org/maven2/org/apache/hadoop/hadoop-mapreduce-client-shuffle/3.0.3/hadoop-mapreduce-client-shuffle-3.0.3.jar $SPARK_HOME/jars
ADD http://central.maven.org/maven2/org/apache/hadoop/hadoop-yarn-api/3.0.3/hadoop-yarn-api-3.0.3.jar $SPARK_HOME/jars
ADD http://central.maven.org/maven2/org/apache/hadoop/hadoop-yarn-client/3.0.3/hadoop-yarn-client-3.0.3.jar $SPARK_HOME/jars
ADD http://central.maven.org/maven2/org/apache/hadoop/hadoop-yarn-common/3.0.3/hadoop-yarn-common-3.0.3.jar $SPARK_HOME/jars
ADD http://central.maven.org/maven2/org/apache/hadoop/hadoop-yarn-server-common/3.0.3/hadoop-yarn-server-common-3.0.3.jar $SPARK_HOME/jars
ADD http://central.maven.org/maven2/org/apache/hadoop/hadoop-yarn-server-web-proxy/3.0.3/hadoop-yarn-server-web-proxy-3.0.3.jar $SPARK_HOME/jars

ADD http://central.maven.org/maven2/com/fasterxml/woodstox/woodstox-core/5.2.0/woodstox-core-5.2.0.jar $SPARK_HOME/jars
ADD http://central.maven.org/maven2/org/codehaus/woodstox/stax2-api/3.0.1/stax2-api-3.0.1.jar $SPARK_HOME/jars

ADD http://central.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.0.3/hadoop-aws-3.0.3.jar $SPARK_HOME/jars
ADD http://central.maven.org/maven2/org/apache/httpcomponents/httpclient/4.5.3/httpclient-4.5.3.jar $SPARK_HOME/jars
ADD http://central.maven.org/maven2/joda-time/joda-time/2.9.9/joda-time-2.9.9.jar $SPARK_HOME/jars
ADD http://central.maven.org/maven2/com/amazonaws/aws-java-sdk-core/1.11.234/aws-java-sdk-core-1.11.234.jar $SPARK_HOME/jars
ADD http://central.maven.org/maven2/com/amazonaws/aws-java-sdk/1.11.234/aws-java-sdk-1.11.234.jar $SPARK_HOME/jars
ADD http://central.maven.org/maven2/com/amazonaws/aws-java-sdk-kms/1.11.234/aws-java-sdk-kms-1.11.234.jar $SPARK_HOME/jars
ADD http://central.maven.org/maven2/com/amazonaws/aws-java-sdk-s3/1.11.234/aws-java-sdk-s3-1.11.234.jar $SPARK_HOME/jars




# Install hadoop 3.0.3

RUN echo $'<?xml version="1.0" encoding="UTF-8"?>\n\
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>\n\
\n\
<configuration>\n\
  <property>\n\
    <name>fs.s3a.endpoint</name>\n\
    <description>AWS S3 endpoint to connect to. An up-to-date list is\n\
      provided in the AWS Documentation: regions and endpoints. Without this\n\
      property, the standard region (s3.amazonaws.com) is assumed.\n\
    </description>\n\
    <value>http://127.0.0.1:9000</value>\n\
  </property>\n\
\n\
  <property>\n\
    <name>fs.s3a.access.key</name>\n\
    <description>AWS access key ID.</description>\n\
    <value>AKIAIOSFODNN7EXAMPLE</value>\n\
  </property>\n\
\n\
  <property>\n\
    <name>fs.s3a.secret.key</name>\n\
    <description>AWS secret key.</description>\n\
    <value>wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY</value>\n\
  </property>\n\
\n\
  <property>\n\
    <name>fs.s3a.path.style.access</name>\n\
    <value>true</value>\n\
    <description>Enable S3 path style access ie disabling the default virtual hosting behaviour.\n\
      Useful for S3A-compliant storage providers as it removes the need to set up DNS for virtual hosting.\n\
    </description>\n\
  </property>\n\
\n\
  <property>\n\
    <name>fs.s3a.impl</name>\n\
    <value>org.apache.hadoop.fs.s3a.S3AFileSystem</value>\n\
    <description>The implementation class of the S3A Filesystem</description>\n\
  </property>\n\
</configuration>' > /Hadoop/hadoop-3.0.3/etc/hadoop/core-site.xml


ENV PATH=$PATH:$HADOOP_HOME/bin
RUN SPARK_DIST_CLASSPATH=$(hadoop classpath)

# Copy across aws credentials
# RUN mkdir ~/.aws/
# COPY minio/credentials ~/.aws/

ENV AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE 
ENV AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
# ENV AWS_ENDPOINT=http://127.0.0.1:9000

# # Add the connector jar needed to access Google Cloud Storage using the Hadoop FileSystem API.
# ADD https://storage.googleapis.com/hadoop-lib/gcs/gcs-connector-latest-hadoop2.jar $SPARK_HOME/jars

# Setup for the Prometheus JMX exporter.
# RUN mkdir -p /etc/metrics/conf
# # Add the Prometheus JMX exporter Java agent jar for exposing metrics sent to the JmxSink to Prometheus.
# ADD https://repo1.maven.org/maven2/io/prometheus/jmx/jmx_prometheus_javaagent/0.3.1/jmx_prometheus_javaagent-0.3.1.jar /prometheus/
# #COPY conf/metrics.properties /etc/metrics/conf
# #COPY conf/prometheus.yaml /etc/metrics/conf

ENTRYPOINT ["/opt/entrypoint.sh"]