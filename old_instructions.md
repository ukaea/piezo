# Installing a Kubernetes cluster

1. Run `./setup.sh`
1. Run kubeadm init

    ```
    kubeadm init --apiserver-advertise-address=172.28.128.10 --apiserver-cert-extra-sans=172.28.128.10  --node-name master-k8s
    ```

1. Add the env variable `export KUBECONFIG=/etc/kubernetes/admin.conf`
1. run set up on worker nodes
1. run 
    ```
    kubeadm join 172.28.128.10:6443 --token 2czcbl.w3v89kzx1pyn78zw --discovery-token-ca-cert-hash sha256:4cc9473f3565be2df1dfa25038bedbdcc5376a067dd6f587e7c246cfeeba33b5
    ```
    on the workers
   (this may require a restart of `kubelet` on master: `systemctl restart kubelet`)
1. `kubectl apply -f "https://cloud.weave.works/k8s/net?k8s-version=$(kubectl version | base64 | tr -d '\n')"`


1. Fix the workers
    ```
    route add 10.96.0.1 gw 172.28.128.10
    ```



## Helm

1. Follow instructions
1. `sudo iptables -P FORWARD ACCEPT`

Fix the release not found problem
1. `kubectl create clusterrolebinding permissive-binding --clusterrole=cluster-admin --user=admin --user=kubelet --group=system:serviceaccounts`

## Add the rbac role for spark

1. `kubectl apply -f manifest/spark-rbac.yaml` from Spark Operator github page

OR

1. `kubectl create serviceaccount spark`
1. `kubectl create clusterrolebinding spark-role --clusterrole=edit --serviceaccount=default:spark --namespace=default`


## Run an example

`kubectl apply -f spark-pi.yaml`

`kubectl get sparkapplications spark-pi -o=yaml`

`kubectl log spark-pi-driver`



## Sparkctl

`go get k8s.io/client-go/...`



