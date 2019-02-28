HARBOR_URL=host-172-16-113-64.nubes.stfc.ac.uk

sudo docker build -t web_app:latest .
sudo docker tag web_app:latest $HARBOR_URL/piezo-resources/web_app:latest
sudo docker push $HARBOR_URL/piezo-resources/web_app:latest