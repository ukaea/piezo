FROM openjdk:8-alpine

ARG spark_uid=185


RUN set -ex && \
    apk upgrade --no-cache && \
    apk add --no-cache bash tini libc6-compat linux-pam krb5 krb5-libs && \
    mkdir -p /opt/spark && \
    mkdir -p /opt/spark/examples && \
    mkdir -p /opt/spark/work-dir && \
    touch /opt/spark/RELEASE && \
    rm /bin/sh && \
    ln -sv /bin/bash /bin/sh && \
    echo "auth required pam_wheel.so use_uid" >> /etc/pam.d/su && \
    chgrp root /etc/passwd && chmod ug+rw /etc/passwd

# HADOOP
ENV HADOOP_VERSION 3.0.3
ENV HADOOP_HOME /usr/hadoop-$HADOOP_VERSION
ENV HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop
ENV PATH $PATH:$HADOOP_HOME/bin
ADD http://archive.apache.org/dist/hadoop/common/hadoop-$HADOOP_VERSION/hadoop-$HADOOP_VERSION.tar.gz /usr/
RUN bash -c "ls /usr/"
RUN cd /usr/ && tar -xzf hadoop-$HADOOP_VERSION.tar.gz && rm -rf hadoop-$HADOOP_VERSION/share/doc && chown -R root:root hadoop-$HADOOP_VERSION




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
    <value>http://172.28.128.10:9000/</value>\n\
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
</configuration>' > $HADOOP_HOME/etc/hadoop/core-site.xml
RUN bash -c "cat $HADOOP_HOME/etc/hadoop/core-site.xml"
# SPARK
ENV SPARK_VERSION 2.4.0
ENV SPARK_PACKAGE spark-${SPARK_VERSION}-bin-without-hadoop
ENV SPARK_HOME /usr/spark-${SPARK_VERSION}-bin-without-hadoop
ENV SPARK_DIST_CLASSPATH="$HADOOP_HOME/etc/hadoop/*:$HADOOP_HOME/share/hadoop/common/lib/*:$HADOOP_HOME/share/hadoop/common/*:$HADOOP_HOME/share/hadoop/hdfs/*:$HADOOP_HOME/share/hadoop/hdfs/lib/*:$HADOOP_HOME/share/hadoop/hdfs/*:$HADOOP_HOME/share/hadoop/yarn/lib/*:$HADOOP_HOME/share/hadoop/yarn/*:$HADOOP_HOME/share/hadoop/mapreduce/lib/*:$HADOOP_HOME/share/hadoop/mapreduce/*:$HADOOP_HOME/share/hadoop/tools/lib/*"
ENV PATH $PATH:${SPARK_HOME}/bin
ADD https://archive.apache.org/dist/spark/spark-2.4.0/spark-2.4.0-bin-without-hadoop.tgz /usr/
RUN cd /usr/ && tar xzf spark-2.4.0-bin-without-hadoop.tgz && rm spark-2.4.0-bin-without-hadoop.tgz && chown -R root:root $SPARK_HOME


ADD http://central.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.0.3/hadoop-aws-3.0.3.jar $SPARK_HOME/jars
ADD http://central.maven.org/maven2/org/apache/httpcomponents/httpclient/4.5.3/httpclient-4.5.3.jar $SPARK_HOME/jars
ADD http://central.maven.org/maven2/joda-time/joda-time/2.9.9/joda-time-2.9.9.jar $SPARK_HOME/jars
ADD http://central.maven.org/maven2/com/amazonaws/aws-java-sdk-core/1.11.234/aws-java-sdk-core-1.11.234.jar $SPARK_HOME/jars
ADD http://central.maven.org/maven2/com/amazonaws/aws-java-sdk/1.11.234/aws-java-sdk-1.11.234.jar $SPARK_HOME/jars
ADD http://central.maven.org/maven2/com/amazonaws/aws-java-sdk-kms/1.11.234/aws-java-sdk-kms-1.11.234.jar $SPARK_HOME/jars
ADD http://central.maven.org/maven2/com/amazonaws/aws-java-sdk-s3/1.11.234/aws-java-sdk-s3-1.11.234.jar $SPARK_HOME/jars

ADD http://central.maven.org/maven2/org/slf4j/slf4j-api/1.7.21/slf4j-api-1.7.21.jar $SPARK_HOME/jars

ENV AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE 
ENV AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY

RUN bash -c  'export PATH=$PATH:$HADOOP_HOME/bin && export SPARK_DIST_CLASSPATH=$(hadoop classpath)'

RUN echo $'#!/bin/bash\n\
#\n\
# Licensed to the Apache Software Foundation (ASF) under one or more\n\
# contributor license agreements.  See the NOTICE file distributed with\n\
# this work for additional information regarding copyright ownership.\n\
# The ASF licenses this file to You under the Apache License, Version 2.0\n\
# (the "License"); you may not use this file except in compliance with\n\
# the License.  You may obtain a copy of the License at\n\
#\n\
#    http://www.apache.org/licenses/LICENSE-2.0\n\
#\n\
# Unless required by applicable law or agreed to in writing, software\n\
# distributed under the License is distributed on an "AS IS" BASIS,\n\
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n\
# See the License for the specific language governing permissions and\n\
# limitations under the License.\n\
#\n\
\n\
# echo commands to the terminal output\n\
set -ex\n\
\n\
# Check whether there is a passwd entry for the container UID\n\
myuid=$(id -u)\n\
mygid=$(id -g)\n\
# turn off -e for getent because it will return error code in anonymous uid case\n\
set +e\n\
uidentry=$(getent passwd $myuid)\n\
set -e\n\
\n\
# If there is no passwd entry for the container UID, attempt to create one\n\
if [ -z "$uidentry" ] ; then\n\
    if [ -w /etc/passwd ] ; then\n\
        echo "$myuid:x:$myuid:$mygid:anonymous uid:$SPARK_HOME:/bin/false" >> /etc/passwd\n\
    else\n\
        echo "Container ENTRYPOINT failed to add passwd entry for anonymous UID"\n\
    fi\n\
fi\n\
\n\
SPARK_K8S_CMD="$1"\n\
case "$SPARK_K8S_CMD" in\n\
    driver | driver-py | driver-r | executor)\n\
      shift 1\n\
      ;;\n\
    "")\n\
      ;;\n\
    *)\n\
      echo "Non-spark-on-k8s command provided, proceeding in pass-through mode..."\n\
      exec /sbin/tini -s -- "$@"\n\
      ;;\n\
esac\n\
\n\
SPARK_CLASSPATH="$SPARK_CLASSPATH:${SPARK_HOME}/jars/*"\n\
env | grep SPARK_JAVA_OPT_ | sort -t_ -k4 -n | sed "s/[^=]*=\(.*\)/\1/g" > /tmp/java_opts.txt\n\
readarray -t SPARK_EXECUTOR_JAVA_OPTS < /tmp/java_opts.txt\n\
\n\
if [ -n "$SPARK_EXTRA_CLASSPATH" ]; then\n\
  SPARK_CLASSPATH="$SPARK_CLASSPATH:$SPARK_EXTRA_CLASSPATH"\n\
fi\n\
\n\
if [ -n "$PYSPARK_FILES" ]; then\n\
    PYTHONPATH="$PYTHONPATH:$PYSPARK_FILES"\n\
fi\n\
\n\
PYSPARK_ARGS=""\n\
if [ -n "$PYSPARK_APP_ARGS" ]; then\n\
    PYSPARK_ARGS="$PYSPARK_APP_ARGS"\n\
fi\n\
\n\
R_ARGS=""\n\
if [ -n "$R_APP_ARGS" ]; then\n\
    R_ARGS="$R_APP_ARGS"\n\
fi\n\
\n\
if [ "$PYSPARK_MAJOR_PYTHON_VERSION" == "2" ]; then\n\
    pyv="$(python -V 2>&1)"\n\
    export PYTHON_VERSION="${pyv:7}"\n\
    export PYSPARK_PYTHON="python"\n\
    export PYSPARK_DRIVER_PYTHON="python"\n\
elif [ "$PYSPARK_MAJOR_PYTHON_VERSION" == "3" ]; then\n\
    pyv3="$(python3 -V 2>&1)"\n\
    export PYTHON_VERSION="${pyv3:7}"\n\
    export PYSPARK_PYTHON="python3"\n\
    export PYSPARK_DRIVER_PYTHON="python3"\n\
fi\n\
\n\
case "$SPARK_K8S_CMD" in\n\
  driver)\n\
    CMD=(\n\
      "$SPARK_HOME/bin/spark-submit"\n\
      --conf "spark.driver.bindAddress=$SPARK_DRIVER_BIND_ADDRESS"\n\
      --deploy-mode client\n\
      "$@"\n\
    )\n\
    ;;\n\
  driver-py)\n\
    CMD=(\n\
      "$SPARK_HOME/bin/spark-submit"\n\
      --conf "spark.driver.bindAddress=$SPARK_DRIVER_BIND_ADDRESS"\n\
      --deploy-mode client\n\
      "$@" $PYSPARK_PRIMARY $PYSPARK_ARGS\n\
    )\n\
    ;;\n\
    driver-r)\n\
    CMD=(\n\
      "$SPARK_HOME/bin/spark-submit"\n\
      --conf "spark.driver.bindAddress=$SPARK_DRIVER_BIND_ADDRESS"\n\
      --deploy-mode client\n\
      "$@" $R_PRIMARY $R_ARGS\n\
    )\n\
    ;;\n\
  executor)\n\
    CMD=(\n\
      ${JAVA_HOME}/bin/java\n\
      "${SPARK_EXECUTOR_JAVA_OPTS[@]}"\n\
      -Xms$SPARK_EXECUTOR_MEMORY\n\
      -Xmx$SPARK_EXECUTOR_MEMORY\n\
      -cp "$SPARK_CLASSPATH"\n\
      org.apache.spark.executor.CoarseGrainedExecutorBackend\n\
      --driver-url $SPARK_DRIVER_URL\n\
      --executor-id $SPARK_EXECUTOR_ID\n\
      --cores $SPARK_EXECUTOR_CORES\n\
      --app-id $SPARK_APPLICATION_ID\n\
      --hostname $SPARK_EXECUTOR_POD_IP\n\
    )\n\
    ;;\n\
\n\
  *)\n\
    echo "Unknown command: $SPARK_K8S_CMD" 1>&2\n\
    exit 1\n\
esac\n\
\n\
# Execute the container CMD under tini for better hygiene\n\
exec /sbin/tini -s -- "${CMD[@]}"' > /opt/entrypoint.sh


WORKDIR $SPARK_HOME
CMD ["bin/spark-class", "org.apache.spark.deploy.master.Master"]
RUN chmod +x /opt/entrypoint.sh
RUN chmod 777 /opt/entrypoint.sh
ENTRYPOINT ["/opt/entrypoint.sh"]