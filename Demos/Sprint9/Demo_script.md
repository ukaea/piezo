### Items included
* Validation rules as config
* Getting job Status
* Getting job Logs
* Deleting a job
* Submitting job against S3
* Passing arguments to the spark job
* Adding labels to jobs
* System tests


### Pre demo
1. Connect to the STFC VPN
2. Ensure that you have kubectl installed and the config file for the cluster on STFC (in slack channel) saved in your `C:Users/{username}/.kube` directory as `config`
3. Run `kubectl get nodes` to ensure that `kubectl` is correctly configured to the openstack cluster. Expect to see the 3 nodes all running and ready. If don't get a response then manually set the environment variable for `KUBECONFIG` to the config file you have for the STFC cluster and retry. If experiencing issues use the config file for a local kubernetes cluster
(`set KUBECONFIG=C:\Users\taro\.kube\config`)
4. Pre build the docker image containing the `PiezoWebApp` by following the deployment instructions on the wiki. In particular running `package_piezo.sh` and `deploy_piezo.sh`


### Validation rules
1. Explain used to have argument validation hard coded.
2. Open up `example_validation_rules.json` to show new improved method
3. Explain how passed to web app and read. Can be updated when web app is redeployed

### Getting job Status
##### POSTMAN
1. Check web app is runnimng `Get to http://host-172-16-113-146.nubes.stfc.ac.uk:31924/piezo/`
2. 
