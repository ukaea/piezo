# ALC Harbor

## Before deployment

Sub-directories of the `roles` directory each contain a `settings` subdirectory (e.g. `roles/docker/settings/`). Public files in each of these directories need to be configured before deployment. The values in these files are not sensitive and so can be committed to git.

In addition, you must add a file named `secret.yml` to the directory `roles/harbor/settings/`. The content of this file must follow this structure:
```
harbor_db_password: ExamplePassword1

s3_access_key: ExampleKey1
s3_secret_key: ExampleKey2
```
This file must not me committed to git (it is ignored via the file `roles/harbor/settings/.gitignore`).

### Production environment

If deploying to a production environment, values in `harbor-deployment.yml` must be changed:
* set the value of `hosts` to `localhost`
* set the value of `hostname` to the production DNS (e.g. `ccfe-harbor.stfc.ac.uk`)
* set the value of `generate_ssl` to `false`

## Deployment

### Vagrant

In a console on your local machine, navigate to this directory and run
```
vagrant up
```

Note that you must have Vagrant and VirtualBox installed.

## Production environment

Zip the `roles` directory and transfer this .zip file (e.g. via SFTP) to the target machine. Also upload the `harbor-deployment.yml` to the same directory.

SSH into the target machine and navigate to the directory where the transferred files are. Unzip the roles, then
```
ansible-playbook harbor-deployment.yml
```

## After deployment

In a web browser, navigate to the machine's IP address (e.g. `172.28.128.170`) or the application DNS (e.g. `ccfe-harbor.stfc.ac.uk`).

Log in as `admin` user with the default password `Harbor12345`. Immediately change the password using the user settings in the top-right corner.


## Troubleshooting

### Reading the log files

Running `docker logs {container ID}` on Harbor containers identified via `docker container ls` does not produce anything useful.

Instead, navigate to `/var/log/harbor/` and browse the `.log` files in that directory.

### I can't login after installation

It's quite possible that Harbor has not installed quite correctly: the browser error messages are not very helpful here. For example, try to register a new user - you will be told that a perfectly reasonable email address is not valid.

To check that Harbor is in fact installed correctly, SSH into the machine and run `docker container ls` a few times. If the status of some "goharbor/..." containers is consistently "Restarting" then Harbor has not quite installed correctly.

Read the log files (see section above) to bug-fix your configuration and re-install.

It may also be worth restarting the system (see below) to see if this resolves the issue.

### I can't login after a system reboot

If the Docker containers that Harbor runs in were in an intermediate state when the machine went down, then they may not have restarted correctly upon machine reboot.

SSH into the machine and run the following commands:
```
cd /usr/local/harbor/
sudo docker-compose restart
```
