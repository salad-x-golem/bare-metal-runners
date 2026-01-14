#!/bin/bash

set -x

NODE_NAME=$1

(cd "${NODE_NAME}_0" && vagrant halt)
(cd "${NODE_NAME}_1" && vagrant halt)
(cd "${NODE_NAME}_2" && vagrant halt)
(cd "${NODE_NAME}_3" && vagrant halt)
(cd "${NODE_NAME}_4" && vagrant halt)
(cd "${NODE_NAME}_5" && vagrant halt)
(cd "${NODE_NAME}_6" && vagrant halt)
(cd "${NODE_NAME}_7" && vagrant halt)
(cd "${NODE_NAME}_8" && vagrant halt)
(cd "${NODE_NAME}_9" && vagrant halt)