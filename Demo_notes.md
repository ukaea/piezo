# Objecteive 5.2
## Items investigated:
    * 5.2.A
    * 5.2.B
    * 5.2.C

# Spark on kubernetes

1. Recap what trying to achieve:
    * Investigating means of spinning up a spark cluster and make running jobs easier

2. What we had last time:
    * Investigated the different means of spinning up a spark cluster
    * Assessed options mainly kubernetes
    * Trialled running example spark applications on minikube

# What has now changed

1. Look at the differences of setting up kubernetes cluster vs minikube
2. Developed a means of setting up a mutli-node kubernetes cluster and run spark jobs stored externally to be run on it

## Issues encountered and processes
    1. Networking: Nodes need to talk to each other using an overlay network
        - Many to choose from
        - Weave and Flannel
        - Weave and Ubuntu don't work, Flannel and Centos don't work,
        Not convinced Flannel and Ubuntu do either
        - Weave and Centos do work
    2. Permissions: Kubernetes uses RBAC security
        - Need to set up service account with correct access for spark
        - Need to create cluster roll binding account
    3. Even with kubernetes cluster fully set up properly so that can deploy nginx image across pods and with spark installed unable to run spark applications due to permissions and networking issues.
        - docker not having permissions acorss nodes
        - Even with image installed on each node spark driver fails to set up workers due to permissions 
    4. Resolve with Helm:
        - Kubernetes package manager
        - Requires cluster role binding account to install
    5. Using helm to install spark operator (alpha release):
        - Needs to be configured to have webhooks enabled to allow for manipulation of pods e.g storage mounts
    6. Can now run spark job using spark operator. Spark operator acts as a proxy and deals with permission issues on your behalf. 

    7. Trying to deal with connecting stoage to the cluster to store data and outputs:
        - Can do a host path mount to mount a directory from the host machine
        - Can use persistent volumes which creates the storage on the cluster which is more robust but still need access to external storage. Failed to set up an nfs connected to the system due to networking issues with IP tables. Now trying S3 storage. Idea is to use docker to connect the two. https://icicimov.github.io/blog/virtualization/Kubernetes-shared-storage-with-S3-backend/
