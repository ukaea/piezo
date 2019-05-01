Example manifests demonstrating how to create additional Kuberenetes features. These could be used to extend the Piezo web app in the future. 

### Ingress

The `example-prometheus-ingress.yaml` file shows a manifest that when applied would create an ingress rule providing access to prometheus at `host-172-16-113-146.nubes.stfc.ac.uk:{ingress-port}/prometheus/` and grafana at `host-172-16-113-146.nubes.stfc.ac.uk:{ingress-port}`. The manifest could be edited to set up new ingress rules for any new services deployed onto the cluster. Note the `serviceName` argument must match the service you are trying to expose and `servicePort` should match the name or number of the port where the service is internally exposed within the cluster. Finally, `path` sets which route the service will be made available on. For more information on writing ingress rules use the [kubernetes documentation](https://kubernetes.io/docs/concepts/services-networking/ingress/).


### Persistent Volumes

Kubernetes persistent volumes could be used to mount storage from the Kubernetes cluster to the spark jobs while they are running. These can be set as empty storage or can be used to mount directories located on the cluster. Using volumes requires two components. A persistent volume (PV) which is provisioned by a cluster administrator and sets aside resources on the cluster and a persistent volume claim (PVC). This is a request from the user to be allocated a PV. A PVC will remain pending unttl a suitable PV is available. To be used, the PVC must be referrenced in the manifest for a spark application which is passed to the spark operator. For full information on persistent volumes please see the [kubernetes documentation](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)

### Secrets

Kubernetes secrets provide a secure way to hold sensitive information on a Kubernetes cluster. We already use these in Piezo to store the keys required for access to S3 storage. To be used within a spark application the secret must either be mounted as a volume where it can be accessed as a file or it can be used to set environment variables that are in effect across a spark application's pods. For full information on secrets please see the [kubernetes documentation](https://kubernetes.io/docs/concepts/configuration/secret/)
