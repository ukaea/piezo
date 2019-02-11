# Examples

Included in the shared code folder a couple of spark application yaml files designed to demonstrate some of the possible use cases.
All examples currently run the same example spark job found in `spark-examples_2.11-2.4.0.jar` however access the code using different methods.

All jobs are run by using the command: `kubectl apply -f {spark-applications-name.yaml}`


### spark-pi.yaml
`spark-pi.yaml` demonstrates running the spark-pi job from a mounted persistent volume using the base docker image from the spark operator. 
To run this job you must have first copy the spark pi example jar from `/code` to `/tmp` by running: `cp ~/code/spark-examples_2.11-2.4.0.jar /tmp/`. This needs to be perfomed on the node where the persistent volume claim is made as it is set to use a hostPath to create the persistent volume. As it is not known which node the volume will be made on it is suggested to copy the file on both of the kubernetes worker nodes. With the data in the right place return to the master node and run `persistent_volume.sh` which will generate the persistent volume and persistent volume claim required by this job.

### spark-pi-host-path.yaml
`spark-pi-host-path.yaml` demonstrates running the spark-pi job from a mounted host path using the base docker image from the spark operator.
Note to run this job you must first log into each node and copy the `spark-examples_2.11-2.4.0.jar` to the `/tmp` folder

### spark-pi-minio.yaml
`spark-pi-minio.yaml` demonstrates puilling the spark pi job off a S3 minio instance and using the `gitlab-registry.cern.ch/db/spark-service/docker-registry/spark:v2.4.0-hadoop3.1` docker image. Note to run this job you have a minio instance running. In your minio browser create a bucket named `kubernetes` and copy across your `spark-examples_2.11-2.4.0.jar` into your bucket.


### spark-word-count.yaml
`spark-word-count.yaml` demonstrates a python spark application and how to connect the data file stored in s3 to the spark application. To run first copy the file `~/code/spark-jobs/word-count/wordcount.py` to the minio instance in the bucket `kubernetes/wordcount/` Also create a text file called `big.txt` in the minio instance at `/kubernetes/`. These files are configurable in the yaml file under the arguments parameter.

