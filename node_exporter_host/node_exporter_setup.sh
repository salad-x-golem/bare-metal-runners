#!/bin/bash
set -x
NODE_EXPORTER_VERSION=1.10.2
NODE_EXPORTER_NAME=node_exporter-$NODE_EXPORTER_VERSION.linux-amd64
sudo curl -L --output $NODE_EXPORTER_NAME.tar.gz https://github.com/prometheus/node_exporter/releases/download/v$NODE_EXPORTER_VERSION/$NODE_EXPORTER_NAME.tar.gz
sudo tar -xf $NODE_EXPORTER_NAME.tar.gz
sudo cp $NODE_EXPORTER_NAME/node_exporter /usr/local/bin
sudo cp node_exporter.service /etc/systemd/system/node_exporter.service
sudo rm $NODE_EXPORTER_NAME -r
sudo rm $NODE_EXPORTER_NAME.tar.gz
sudo useradd -rs /bin/false node_exporter
sudo systemctl daemon-reload
sudo systemctl start node_exporter
sudo systemctl enable node_exporter
