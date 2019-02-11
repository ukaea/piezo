sudo docker build -t web_app:latest . 
sudo docker tag web_app:latest 172.28.128.10/library/web_app:latest
sudo docker push 172.28.128.10/library/web_app:latest