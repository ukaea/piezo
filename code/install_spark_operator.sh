helm repo add incubator http://storage.googleapis.com/kubernetes-charts-incubator
helm install incubator/sparkoperator --namespace spark-operator --set enableWebhook=true

kubectl apply -f spark-rbac.yaml
kubectl create clusterrolebinding spark-role --clusterrole=edit --serviceaccount=default:spark --namespace=default

# If need to delete use kubectl delete deployment -n spark-operator {name of operator}