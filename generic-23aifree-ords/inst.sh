#!/bin/bash

#######    S T A R T      S C R I P T    ######
#######   (this is for Oracle Linux 9)   ######

## update
sudo dnf update -y

## set firewall rules
sudo firewall-cmd --permanent --add-port=1521/tcp #Database
sudo firewall-cmd --permanent --add-port=1522/tcp #Database
sudo firewall-cmd --permanent --add-port=8888/tcp #JupyterLabs
sudo firewall-cmd --permanent --add-port=8181/tcp #ORDS
sudo firewall-cmd --permanent --add-port=8282/tcp #ORDS
sudo firewall-cmd --permanent --add-port=8501/tcp #Streamlit
sudo firewall-cmd --permanent --add-port=5000/tcp #Flask
sudo firewall-cmd --permanent --add-port=5500/tcp #EM
sudo firewall-cmd --permanent --add-port=5501/tcp #EM
sudo firewall-cmd --permanent --add-port=7000/tcp #Django
sudo firewall-cmd --permanent --add-port=27017/tcp #Mongo
sudo firewall-cmd --permanent --add-port=8085/tcp #Sping1
sudo firewall-cmd --permanent --add-port=8086/tcp #Sprin2
sudo firewall-cmd --permanent --add-port=8087/tcp #Sprin3
sudo firewall-cmd --permanent --add-port=8088/tcp #Sprin4
sudo firewall-cmd --permanent --add-rich-rule='rule family="ipv4" destination address="10.0.0.0/24" service name="ssh" accept'
sudo firewall-cmd --reload

#expand boot volume (https://docs.oracle.com/en-us/iaas/oracle-linux/oci-utils/index.htm#oci-growfs)
sudo /usr/libexec/oci-growfs -y

#podman and utensils - https://docs.oracle.com/en/operating-systems/oracle-linux/podman/podman-InstallingPodmanandRelatedUtilities.html
sudo dnf module enable nodejs:20 -y
sudo dnf install -y oracle-epel-release-el9
sudo dnf config-manager --enable ol9_developer_EPEL
sudo dnf install -y container-tools sqlcl jdk21 wget git 
# sudo dnf install -y podman-compose
sudo dnf -y install oraclelinux-developer-release-el9
sudo dnf -y install python39-oci-cli python3.9-pip
sudo dnf -y install maven

sudo pip install oracledb dotenv podman-compose

sudo pip install --upgrade podman-compose


#set up user and group for podman
sudo loginctl enable-linger 'opc'
sudo setsebool -P container_manage_cgroup on

#aliases (source manually for now)
mkdir -p ~/.config/jambo
chmod +x /home/opc/compose2cloud/init/*.sh
cp /home/opc/compose2cloud/init/alias.sh ~/.config/jambo/.

## some LiveLabs config
sudo bash /home/opc/compose2cloud/init/firstboot.sh
sudo ln -sf /home/opc/compose2cloud/init/firstboot.sh /var/lib/cloud/scripts/per-instance/firstboot.sh
sudo /var/lib/cloud/scripts/per-instance/firstboot.sh

## load variables (scripts, passwords, etc)
source /home/opc/compose2cloud/init/variable.sh


## create the compose script folder and files
mkdir -p /home/opc/compose2cloud/composescript/envvar

mkdir -p /home/opc/.config/systemd/user

chmod 777 /home/opc/compose2cloud/composescript/envvar/

touch /home/opc/compose2cloud/composescript/envvar/readme.md

## copy the compose script files to the folder
cp /home/opc/compose2cloud/composescript/scripts/user-podman.service /home/opc/.config/systemd/user/.
cp /home/opc/compose2cloud/composescript/scripts/db-podman.service /home/opc/.config/systemd/user/.

#gettting oci cl config sorted out
mkdir -p /home/opc/.oci


mkdir -p /home/opc/compose2cloud/composescript/ords_config
chmod 777 /home/opc/compose2cloud/composescript/ords_config


sudo systemctl daemon-reload
export XDG_RUNTIME_DIR=/run/user/$UID
systemctl --user daemon-reload
systemctl --user enable user-podman
systemctl --user enable db-podman
systemctl --user start user-podman
systemctl --user start db-podman

#######    E N D      S C R I P T    ######
