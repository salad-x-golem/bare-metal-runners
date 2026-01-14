#!/bin/bash
set -x
vagrant destroy -f
/bin/bash host_bootstrap.sh
vagrant up --no-provision
vagrant halt 
vagrant up --provision
