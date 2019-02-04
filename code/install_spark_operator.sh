helm repo add incubator http://storage.googleapis.com/kubernetes-charts-incubator
helm install incubator/sparkoperator --namespace spark-operator --set enableWebhook=true --set metrics-labels=app_type

kubectl apply -f spark-rbac.yaml
kubectl create clusterrolebinding spark-role --clusterrole=edit --serviceaccount=default:spark --namespace=default
