sudo docker build -t spark-prom:latest . 
sudo docker tag spark-prom:latest 172.28.128.10/library/spark-prom:latest
sudo docker push 172.28.128.10/library/spark-prom:latest