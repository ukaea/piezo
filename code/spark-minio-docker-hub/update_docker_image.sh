sudo docker build -t spark-minio-docker:latest . 
sudo docker tag spark-minio-docker:latest 172.28.128.10/library/spark-minio-docker:latest
sudo docker push 172.28.128.10/library/spark-minio-docker:latest