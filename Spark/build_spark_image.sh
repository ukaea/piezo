HARBOR_URL=$1

sudo docker build --no-cache -t piezo-spark-image:latest .
sudo docker tag piezo-spark-image:latest ${HARBOR_URL}/piezo-resources/piezo-spark-image:latest
sudo docker push ${HARBOR_URL}/piezo-resources/piezo-spark-image:latest
