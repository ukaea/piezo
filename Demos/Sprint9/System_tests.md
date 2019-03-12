# Running system tests

[Wiki page](https://github.com/ukaea/piezo/wiki/SystemTests)

Connect to the SFTC VPN.

In MobaXTerm, open sessions to the system test controller (`172.16.113.201`):
* SSH
* SFTP

Open the system tests scripts directory (`SystemTests/roles/robot/files`). The Atom editor is recommended for viewing `.robot` files, once the `language-robot-framework` package is installed.

Open Powershell for running `kubectl` commands and navigate to the appropriate directory. Delete any existing spark applications:
```
.\src\kubectl.exe delete sparkapplications -l userLabel=systemTest
```

In the SSH session of MobaXTerm
```
cd /home/robot/
source SystemTests/venv/bin/activate
robot test_scripts
```
