kubectl create configmap validation-rules --from-file=validation_rules.json -o yaml --dry-run | kubectl replace -f -
