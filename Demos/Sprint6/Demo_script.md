## Included iteams:
* Connecting to S3 
* Docker image for S3
* config for S3
* Reading and writing from S3
* Writing custom spark job
* Arguments for spark jobs
* Spark UI
* mointoring with prometheus and grafana

# Pre demo
1. `vagrant up`
2. `vagrant ssh master-k8s`
3. `cd code`
    - `./install_spark_operator.sh`
4. Install harbor followign instuctions in `Docs/Setting_up_a_docker_registory.md`
5. `cd ~/code/prometheus`
6. `sudo docker build -t  spark-prom:latest .`
7. `sudo docker tag spark-prom:latest 172.28.128.10/library/spark-prom:latest`
8. `sudo docker push 172.28.128.10/library/spark-prom:latest`

# Connecting to S3
0. In browser show minio instance `172.28.128.10:9000` and explain how set up same way as for ditto
1. Open up `spark-word-count.yaml` in VScode
2. Show script `~/code/spark-jobs/word-count/wordcount.py` and explain basics of RDD format
2. Talk about hadoop configuration (how alone this didn't work)
3. Go to `spark-pi.yaml` and show original spark image
4. Explain how contains spark 2.4 wih hadoop 2.7 but need hadoop > 2.7, difficult to build over the top as too many things that clash/ need removing/ dependencies/ connecting configs
5. Explain how tried building our own image and then came across cern image. `https://gitlab.cern.ch/db/spark-service/docker-registry` (spark 2.4 and hadoop 3.1)
6. Show our docker file `~/code/prometheus/Dockerfile` and how we are building over this cern image with requirments for S3
7. Explain using local harbor registery as in 5.3 to push and pull images
8. Back in `spark-word-count.yaml` show how to specify files in s3 including arguments
9. `kubectl apply -f ~/code/spark-word-count.yaml`
10. While running move on to Spark UI

# Spark UI
1. In powershell on local machine run `kubectl proxy`
2. In new powershell window on local machine run `kubectl port-forward py-wordcount-driver 4040:4040`
3. In browser navigate to `localhost:4040`

# Prometheus
1. Explain what prometheus is and how it should be able to work
2. In VM run `kubectl get pods --all-namespaces` show pods, say used helm 
3. Pwershell: `kubectl port-forward py-wordcount-driver 9090`
4. Browser `127.28.128.10:9090`

# Grafana
1. Explain concept of Grafana
2. powershell `kubectl port-forward $(kubectl get  pods --selector=app=grafana -n  monitoring --output=jsonpath="{.items..metadata.name}") -n monitoring  3000`
3. login: username: 'admin' password: 'prom-operator'
4. Browser `127.28.128.10:3000`


# Check results
1. Once job has finished return to `172.28.128.10:9000` and show output
