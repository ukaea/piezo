kubectl create configmap validation-rules --from-file=validation_rules.json -o yaml --dry-run | kubectl replace -f -
kubectl create configmap piezo-web-app-config --from-file=configuration.ini -o yaml --dry-run | kubectl replace -f -
kubectl scale deployment piezo-web-app --replicas=0
kubectl scale deployment piezo-web-app --replicas=1
