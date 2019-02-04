./containerise.sh
kubectl run test-app --image=172.28.128.10/library/web_app:latest --port 8888
kubectl expose deployment test-app --type=LoadBalancer --port 80 --target-port 8888