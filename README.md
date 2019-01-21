# ALC Kubernetes Spark
A kubernetes cluster configured to run spark jobs

## Initialising the cluster
The following instructions will initiate a 3 node kubernetes cluster with all component needed for running spark installed.

#### Requirments
* `Vagrant`
* `VirtualBox`

#### Vagrant
In a console on your local machine, navigate to this directory and run:
```vagrant up``` 
This will initiate 3 VMs running centos 7. These will be be called `master-k8s` (configured as the kubernetes master node), `node1-k8s` and `node2-k8s` (configured as the kubernetes worker nodes). The machines will be provisioned with ansible and connected to produce a running kubernetes cluster. 

#### Install spark operator
Log into the kubernetes master node `vagrant ssh master-k8s` and run `kubectl get pods --all-namespaces`. Wait for the `tiller` pod to have the status of running and then run:
```./install_spark_operator.sh```

At this stage kubernetes is running and you have the spark operator installed. This can then be used to initate spark jobs by specifying the spark operators api in an applications yaml file. (See `spark-pi.yaml` for an example)


## Running a spark job
To run a spark job you need to insert the code and data into the kubernetes cluster. There are a few ways this can be done. Once onto the cluster you can specify the location of the data in the applications yaml file and it will then be included in the spark job.

### Getting code onto the cluster
There are three main routes by which this can be achieved 

#### Using a shared folder
As the kubernetes cluster is provisioned on virtual machines we have included a shared folder which can be used to share data from your local machine to the virtual machine. This can be used directly to add data and code files onto the kubernetes cluster. In the spark application's yaml file you can then mount the corresponding directory directly into the spark pods by using a hostPath volume mount or create a kubernetes persistent volume claim and include this mounted into the spark application.

##### Using host path

To make a directory accessible from the virtual machine in the spark pods you can mount it by including the following in the application's yaml file.

```
specs:
  volumes:
    - name: "test-volume"
      hostPath:
        path: "/tmp"  # path on VM to directory you want to mount
        type: Directory
  driver:
    volumeMounts:
      - name: "test-volume" # must match the name given to he volume listed above
        mountPath: "/tmp" # Place for the volume to be mounted within the image in the spark driver pod
  executor:
    volumeMounts:
      - name: "test-volume"
        mountPath: "/tmp" # Place for the volume to be mounted within the image in the spark executor pods
```

##### Using persistent volume claims
To create a persistent volume claim a persistent volume must first be initiated in the kubernetes cluster. This can be defined in a yaml file as below:
``` 
kind: PersistentVolume
apiVersion: v1
metadata:
  name: pv-volume # name o define volume by
  labels:
    type: local
spec:
  storageClassName: manual
  capacity:
    storage: 2Gi # Max capacity put aside for this volume
  accessModes:
    - ReadWriteMany # See below *
  hostPath:
    path: "/tmp" # Location on VM to replicate in the volume
```
   \* Volumes can be ReadWriteOnce (read write accessible from a single node), ReadOnlyOnce (read only from a single node) or ReadWriteMany (read write accessible from multiple nodes)

This volume can be create by running `kubectl apply -f persistent_volume_file_name.yaml`. Using this persistent volume, you must then fix it to a persistent volume claim which will then exist almost like a pod within the kubernetes cluster. This can be created using a yaml file as below. Note persistent volumes and persistent volume claims are strictly one to one and even if the claim only uses a small amount of the persistent volume the rest won't be available for other claims until the fist claim is destroyed. 

```
kind: PersistentVolumeClaim
apiVersion: v1
metadata:
  name: pv-claim # Name for claim, will be referenced in spark application files
spec:
  storageClassName: manual
  accessModes:
    - ReadWriteMany # As above
  resources:
    requests:
      storage: 2Gi # Max amount of persistent volume requested
```
The persistent volume can then be linked into the spark application in a similar fashion as using a hostPath by including the following lines.

```
spec:
  volumes:   # what volume to mount
    - name: "pv-storage" # local definition for the mounted volume
      persistentVolumeClaim:
        claimName: pv-claim # Name spaecified in the persistent vvolume claim yaml file
  driver:
    volumeMounts:
      - name: "pv-storage" # Name mentioned above
        mountPath: "/mnt/data" # Where to mount it on the spark driver
  executor:
    volumeMounts:
      - name: "pv-storage" # Name mentioned above
        mountPath: "/mnt/data" # Where to mount it on the spark executor
```
Persistent volume claims are more robust than hostPath mounts as if the application pods crash then when new pods are spun up in their place the persistent volume claim is reassigned rather then crashing with the pod as with what happens when hostPath is used

#### Including extra folders in the docker image
Each spark application runs a specified docker image in the driver and each of it's pods. this is specified in the application's yaml file with the code:
```
spec:
  image: "gcr.io/spark-operator/spark:v2.4.0"
  imagePullPolicy: Always
```
Certain requirments are needed in this docker image for spark to run, however, it also be customised to include additional requirements and folders. To do this you first need to build a custom docker image and upload this to a repository accessible to the kubernetes cluster. 
It's reccommended you set up a local harbor registery using the instructions [here](link to Rob's harbor stuff). 
With this registory set up, it is then possible to build your custom docker images, push them to this registory and then pull then for the spark application. 
When building your custom docker images it is reccomended to start with the base Spark image (gcr.io/spark-operator/spark:v2.4.0) and then include additional requirments as layers above this image. This will help ensure that all requirments are met for running the base spark jobs. Additional folders from the machine where you build the docker image can be included by using the `COPY` command

#### Connecting to external storage (e.g. S3)
Spark applications can also be configured so that they can communicate with external storage systems directly. 