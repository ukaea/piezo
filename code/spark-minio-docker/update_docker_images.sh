sudo docker build -t spark-minio:latest . 
sudo docker tag spark-minio:latest 172.28.128.10/library/spark-minio:latest
sudo docker push 172.28.128.10/library/spark-minio:latest