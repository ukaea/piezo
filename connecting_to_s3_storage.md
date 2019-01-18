# Investigation
* Seem to need to configure hadoop in spark application yaml file this require extra jars
* Jars can be imported seperately by specifying specs.deps but doesn't guarentee their dependecies are met
* deps.packages would solve this but is currently in PR stage to get it implemented
* Look to adding extra jars in docker image
* Need a registery that can pull image from
* Trying with Harbor from 5.3

## Building a custom docker image and running it for the spark application

* Install `Harbor` as in 5.3 and create a public repository
* In browser (firefox) navigate to ip of harbor host as in config of harbor (in this case 172.28.128.10)
* Login as usr:`admin` pass:`Harbor12345` default (changed to Harbor123)
* Add a user that can push and pull to the repository
* To deal with certificate issues run (on each node):
    - `sudo echo '{"insecure-registries": ["172.28.128.10"]}' > ~/daemon.json`
    - `sudo mv ~/daemon.json /etc/docker/`
    - `sudo systemctl stop docker`
    - `sudo systemctl start docker`
* On local machine `sudo docker login 172.28.128.10`
* Enter credentials of user created
* Create a docker file and put it in a directory (use the template [here](https://github.com/GoogleCloudPlatform/spark-on-k8s-operator/blob/master/spark-docker/Dockerfile))
* Once docker image is ready navigate to directory of docker image and run `docker build -t name-for-image:tag .`
* Check image shows up `sudo docker image ls`
* Tag the image `sudo docker tag name-for-image:tag 172.28.128.10/library/name-for-image:tag`
* Push the image `sudo docker push 172.28.128.10/library/name-for-image:tag`
* Can check image is in the browser
* when writing the spark application's yaml file now use the argument `image: 172.28.128.10/library/name-for-image:tag`

## Progress
* Was getting error of missing class with base image even with deps included as jars weren't being added to the spark application
* Got around this by adding jars higher up in the docker image and pulling this new docker image into the pods as above
* Then get error as ` Unable to load AWS credentials from any provider in the chain` even though explicitly stated in the specs.spark.hadoop
* May be due to hadoop global conf being different rather than just the spark hadoop conf
* Fixed issue by setting environment variables in the docker image `ENV AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE` and `ENV AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY`

## Can connect outside of the spark operator using: 
`https://github.com/nitisht/cookbook/blob/4de9806db1916142781ba1df1bbdbcd00b6464e2/docs/apache-spark-with-minio.md`
* Need to set JAVA_HOME `export JAVA_HOME=/usr/lib/jvm/jre-1.8.0-openjdk`

* With hadoop2.7.3 extra jar needed `http://central.maven.org/maven2/org/apache/httpcomponents/httpcore/4.3/httpcore-4.3.jar`
* But still get error `java.lang.NoSuchFieldError: INSTANCE` (Both with 4.3 and 4.4, no 4.5 version available). Think it could be a compatability issue with httpclient4.5.3

Tried: 
HTTPClient HTTPCore                  Result
4.5.3       4.4     java.lang.NoSuchFieldError: INSTANCE
4.5.3       4.3     java.lang.NoSuchFieldError: INSTANCE
4.5.3       4.2     java.lang.NoClassDefFoundError: org/apache/http/config/Lookup (this is class we installed HTTPCorejar for)
4.3.4       4.4     java.lang.NoSuchMethodError: org.apache.http.conn.ssl.SSLConnectionSocketFactory.<init>(Ljavax/net/ssl/SSLContext;Ljavax/net/ssl/HostnameVerifier;)V
4.5.2       4.4     java.lang.NoSuchFieldError: INSTANCE
4.4.1       4.4     java.lang.NoSuchFieldError: INSTANCE

