#!/bin/bash

set -x

NODE_NAME=$1

(cd "${NODE_NAME}_0" && vagrant up)
(cd "${NODE_NAME}_1" && vagrant up)
(cd "${NODE_NAME}_2" && vagrant up)
(cd "${NODE_NAME}_3" && vagrant up)
(cd "${NODE_NAME}_4" && vagrant up)
(cd "${NODE_NAME}_5" && vagrant up)
(cd "${NODE_NAME}_6" && vagrant up)
(cd "${NODE_NAME}_7" && vagrant up)
(cd "${NODE_NAME}_8" && vagrant up)
(cd "${NODE_NAME}_9" && vagrant up)