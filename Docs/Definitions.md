# Definitions

## Ambassador pattern

The ambassador pattern is a useful way to connect containers with the outside world. An ambassador container is essentially a proxy that allows other containers to connect to a port on localhost while the ambassador container can proxy these connections to different environments depending on the cluster's needs. The ambassador pattern is an example of the **Sidecar pattern**.

One of the best use-cases for the ambassador pattern is for providing access to a database. When developing locally, you probably want to use your local database, while your test and production deployments want different databases again.

Managing which database you connect to could be done through environment variables, but will mean your application changes connection URLs depending on the environment. A better solution is for the application to always connect to localhost, and let the responsibility of mapping this connecting to the right database fall to an ambassador container. Alternatively, the ambassador could be sending requests to different shards of the database—the application itself doesn't need to worry.

## AppArmour
AppArmor is a Linux kernel security module that supplements the standard Linux user and group based permissions to confine programs to a limited set of resources. AppArmor can help you to run a more secure deployment by restricting what containers are allowed to do, and/or provide better auditing through system logs.

## CNI
CNI (Container Network Interface), a Cloud Native Computing Foundation project, consists of a specification and libraries for writing plugins to configure network interfaces in Linux containers, along with a number of supported plugins. CNI concerns itself only with network connectivity of containers and removing allocated resources when the container is deleted.

## DNS
The Domain Name System (DNS) is a hierarchical decentralized naming system for computers, services, or other resources connected to the Internet or a private network. It associates various information with domain names assigned to each of the participating entities. Most prominently, it translates more readily memorized domain names to the numerical IP addresses needed for locating and identifying computer services and devices with the underlying network protocols.

## Helm
Helm enables a Kubernetes operator to have greater control over the Kubernetes cluster. If you are familiar with apt/yum/brew and their role in different Operating Systems then you should already know the importance of a package manager.  Helm is the package manager for the Kubernetes (in this approach, Kubernetes could be considered as an operating system).

Helm is the client to a **Tiller** server.

## Kubeadm
Kubeadm is a tool built to provide `kubeadm init` and `kubeadm join` as best-practice “fast paths” for creating Kubernetes clusters.

kubeadm performs the actions necessary to get a minimum viable cluster up and running. By design, it cares only about bootstrapping, not about provisioning machines.

## Kubectl
Kubectl is the controller to kubernetes. Using kubectl, you can inspect cluster resources; create, delete, and update components; look at your new cluster; and bring up example apps.

## Kubelet
The kubelet is the primary “node agent” that runs on each node. The kubelet works in terms of a PodSpec. A PodSpec is a YAML or JSON object that describes a pod. The kubelet takes a set of PodSpecs that are provided through various mechanisms (primarily through the apiserver) and ensures that the containers described in those PodSpecs are running and healthy. The kubelet doesn’t manage containers which were not created by Kubernetes.

## Kubernetes API
The REST API is the fundamental fabric of Kubernetes. All operations and communications between components, and external user commands are REST API calls that the API Server handles. Consequently, everything in the Kubernetes platform is treated as an API object and has a corresponding entry in the API.

## kubernetes operator (e.g. Helm)
Enables developers to extend and add new functionalities, replace existent ones (like replacing kube-proxy for instance), and of course, automate administration tasks as if they were a native Kubernetes component.

An Operator is nothing more than a set of application-specific custom controllers.

## Sidecar pattern

Extends the functionality of the main container with a strong coupling to a sidecar container. A sidecar is a utility container in a pod with the purpose to support the main container. Standalone sidecars don't serve any purpose, must be paired with one or more containers. Generally are reusable and can be paired with numerous types of main containers.

A useful example of the sidecar pattern is the **Ambassador pattern**.

## Tiller
Tiller is the in-cluster component of **Helm**. It interacts directly with the Kubernetes API server to install, upgrade, query, and remove Kubernetes resources. It also stores the objects that represent releases.

## Volume Mount
The different types are:
* hostPath: A hostPath volume mounts a file or directory from the host node’s filesystem into your Pod.
* emptyDir: Loads an empty directory for storage onto a pod when it is created.
* Persistent volume: PersistentVolumes are a way for users to “claim” durable storage (such as a GCE PersistentDisk or an iSCSI volume) without knowing the details of the particular cloud environment.
* Volumes can be ReadWriteOnce (read write accessible from a single node), ReadOnlyOnce (read only from a single node) or ReadWriteMany (read write accessible from multiple nodes).

## Weave (an example of a CNI plugin)
Weave Net creates a virtual network that connects Docker containers deployed across multiple hosts. To application containers, the network established by Weave resembles a giant Ethernet switch, where all containers are connected and can easily access services from one another.

## Types of volume mounts
    * hostPath: A hostPath volume mounts a file or directory from the host node’s filesystem into your Pod.
    * emptyDir: Loads an empty directory for storage onto a pod when it is created
    * Persistent volume: PersistentVolumes are a way for users to “claim” durable storage (such as a GCE PersistentDisk or an iSCSI volume) without knowing the details of the particular cloud environment.
    * Volumes can be ReadWriteOnce (read write accessible from a single node), ReadOnlyOnce (read only from a single node) or ReadWriteMany (read write accessible from multiple nodes)

## RDD (Resilient distributed dataset)
A collection of elements partitioned across the nodes of the cluster that can be operated on in parallel. RDDs are distributed data sets that can stay in memory and fallback to disk gracefully. RDDs if lost can be easily rebuilt using a graph that says how to reconstruct.

## DAG (Directed Acyclic Graph)
DAG (Directed Acyclic Graph) is a programming style for distributed systems - You can think of it as an alternative to Map Reduce. While MR has just two steps (map and reduce), DAG can have multiple levels that can form a tree structure. Say if you want to execute a SQL query, DAG is more flexible with more functions like map, filter, union etc.
