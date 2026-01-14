#!/bin/bash

set -x

NODE_NAME=$1

(cd "${NODE_NAME}_0" && vagrant destroy)
(cd "${NODE_NAME}_1" && vagrant destroy)
(cd "${NODE_NAME}_2" && vagrant destroy)
(cd "${NODE_NAME}_3" && vagrant destroy)
(cd "${NODE_NAME}_4" && vagrant destroy)
(cd "${NODE_NAME}_5" && vagrant destroy)
(cd "${NODE_NAME}_6" && vagrant destroy)
(cd "${NODE_NAME}_7" && vagrant destroy)
(cd "${NODE_NAME}_8" && vagrant destroy)
(cd "${NODE_NAME}_9" && vagrant destroy)

