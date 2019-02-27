sudo docker build -t web_app:latest .
sudo docker tag web_app:latest host-172-16-113-64.nubes.stfc.ac.uk/piezo-resources/web_app:latest
sudo docker push host-172-16-113-64.nubes.stfc.ac.uk/piezo-resources/web_app:latest