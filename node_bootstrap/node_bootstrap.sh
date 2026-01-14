#!/bin/bash

# load environmental variables from .env file
if [ -f .env ]; then
  export $(echo $(cat .env | sed 's/#.*//g'| xargs) | envsubst)
fi

set -x

GITHUB_RUNNER_TAR=actions-runner-linux-x64-2.330.0.tar.gz
GITHUB_RUNNER_TOKEN=$GITHUB_RUNNER_TOKEN
GITHUB_RUNNER_NAME=$GITHUB_RUNNER_NAME

# fixes degraded state of systemctl (reboot fixes that issue)
# sudo systemctl start systemd-networkd-wait-online.service

# expand partition (specific to machine) to fit to virtual disk
sudo growpart /dev/vda 3
sudo lvextend -l +100%FREE /dev/ubuntu-vg/ubuntu-lv
sudo resize2fs /dev/mapper/ubuntu--vg-ubuntu--lv

# expand swap from default to 16GB
sudo swapoff -a
sudo rm swap.img
# sudo fallocate -l 16G /swap.img
# sudo chmod 600 /swap.img
# sudo mkswap /swap.img
# sudo swapon /swap.img

# setup machine
sudo apt update
#sudo apt upgrade -y
sudo apt install -y net-tools mc cmake musl musl-tools libssl-dev pkg-config build-essential bzip2 curl g++ gcc make jq tar unzip wget python-is-python3 python3-dev python3-pip

# configure python
sudo pip install requests eth-account dotenv

# setup github runner
echo "Setup Github Runner"
sudo su -m vagrant -c "mkdir -p /home/vagrant/actions-runner && curl -L https://github.com/actions/runner/releases/download/v2.330.0/actions-runner-linux-x64-2.330.0.tar.gz | tar -xzf - -C /home/vagrant/actions-runner"

cd /home/vagrant/actions-runner
echo "Configuring Github Runner"
sudo su -m vagrant -c "./config.sh --unattended --url https://github.com/salad-x-golem --token $GITHUB_RUNNER_TOKEN --replace --name $GITHUB_RUNNER_NAME --labels $GITHUB_RUNNER_LABELS"
sudo ./svc.sh install
sudo ./svc.sh start

# cleanup
sudo rm .env
sudo rm *.tar.gz
history -c
sudo su -m vagrant -c "history -c"

