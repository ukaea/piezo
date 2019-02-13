# System Tests

The System Test framework is intended for use on a cloud computing environment (e.g. OpenStack) where there is also a cluster of the main system provisioned on separate VMs.

## Test environment

An instance of [Minio](https://www.minio.io/) is running on the VM that hosts the system test environment. The test Spark jobs that are submitted to the Kubernetes cluster are configured to use this Minio instance for their S3 storage, allowing easy inspection of the files generated.

```
hadoopConf:
    fs.s3a.endpoint: http://172.16.113.201:9000
    fs.s3a.access.key: AKIAIOSFODNN7EXAMPLE
    fs.s3a.secret.key: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
```

## Setup

Setup requires a Unix OS (tested with Scientific Linux 7). If your local machine runs Windows, it is recommended that you set up a Linux VM.

Create a VM on the cloud with an SSH key pair. Scientific Linux 7 (without GUI) is recommended. You will need the IP address this is assigned and the username used to create it.

Copy the public and private keys to `~/.ssh/`. Add the public key to the authorized keys and set the permissions of the private key:
```
cd ~/.ssh/
sudo echo {public key name} >>> authorized_keys
sudo chmod 0600 {private key name}
```

Check that you can SSH into the cloud VM (you will likely need to confirm that you trust the host):
```
ssh-add ~/.ssh/{private key name}
ssh {user name}@{ip address}
```

Create a file named `hosts` in this directory (i.e. `SystemTests/hosts`) with content as follows:
```
default ansible_host={IP address} ansible_user={user name} ansible_ssh_private_key_file=~/.ssh/{private key name}

[webservers]
default
```

Navigate back to this directory, then run the Ansible playbook to install all the necessary packages on the System Test VM:
```
ansible-playbook --inventory=hosts playbook.yml
```

## Running tests

SSH into the VM and navigate to `/home/robot/`.

Source the Python virtual environments:
```
source SystemTests/venv/bin/activate
```

Run the system test scripts:
```
robot test_scripts/piezo.robot
```
