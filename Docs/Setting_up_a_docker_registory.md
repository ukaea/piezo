## Building a custom docker image and running it for the spark application

* Install `Harbor` by with ansible by running: `ansible-playbook ~/code/harbor/alc-harbor/harbor-deployment.yml`
* In browser (firefox) navigate to ip of harbor host as in config of harbor (in this case 172.28.128.10)
* Login as usr:`admin` pass:`Harbor12345` default (changed to Harbor123)
* Add a user that can push and pull to the repository
* To deal with certificate issues run (on each node):
    - `sudo echo '{"insecure-registries": ["172.28.128.10"]}' > ~/daemon.json`
    - `sudo mv ~/daemon.json /etc/docker/`
    - `sudo systemctl restart docker`
* On local machine `sudo docker login 172.28.128.10`
* Enter credentials of user created
* Create a docker file and put it in a directory (use the template [here](https://github.com/GoogleCloudPlatform/spark-on-k8s-operator/blob/master/spark-docker/Dockerfile))
* Once docker image is ready navigate to directory of docker image and run `docker build -t name-for-image:tag .`
* Check image shows up `sudo docker image ls`
* Tag the image `sudo docker tag name-for-image:tag 172.28.128.10/library/name-for-image:tag`
* Push the image `sudo docker push 172.28.128.10/library/name-for-image:tag`
* Can check image is in the browser
* when writing the spark application's yaml file now use the argument `image: 172.28.128.10/library/name-for-image:tag`
