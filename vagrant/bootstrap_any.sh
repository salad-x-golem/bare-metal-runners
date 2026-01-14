#!/bin/bash

NODE_NAME=$1

set -x
./copy_selected.sh 0 "${NODE_NAME}"
./copy_selected.sh 1 "${NODE_NAME}"
./copy_selected.sh 2 "${NODE_NAME}"
./copy_selected.sh 3 "${NODE_NAME}"
./copy_selected.sh 4 "${NODE_NAME}"
./copy_selected.sh 5 "${NODE_NAME}"
./copy_selected.sh 6 "${NODE_NAME}"
./copy_selected.sh 7 "${NODE_NAME}"
./copy_selected.sh 8 "${NODE_NAME}"
./copy_selected.sh 9 "${NODE_NAME}"

(cd "${NODE_NAME}_0" && /bin/bash host_bootstrap.sh)
(cd "${NODE_NAME}_1" && /bin/bash host_bootstrap.sh)
(cd "${NODE_NAME}_2" && /bin/bash host_bootstrap.sh)
(cd "${NODE_NAME}_3" && /bin/bash host_bootstrap.sh)
(cd "${NODE_NAME}_4" && /bin/bash host_bootstrap.sh)
(cd "${NODE_NAME}_5" && /bin/bash host_bootstrap.sh)
(cd "${NODE_NAME}_6" && /bin/bash host_bootstrap.sh)
(cd "${NODE_NAME}_7" && /bin/bash host_bootstrap.sh)
(cd "${NODE_NAME}_8" && /bin/bash host_bootstrap.sh)
(cd "${NODE_NAME}_9" && /bin/bash host_bootstrap.sh)


