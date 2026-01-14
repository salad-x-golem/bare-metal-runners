#!/bin/bash

set -x

NODE_NAME=$1

(cd "${NODE_NAME}_0" && /bin/bash recreate_runner.sh)
(cd "${NODE_NAME}_1" && /bin/bash recreate_runner.sh)
(cd "${NODE_NAME}_2" && /bin/bash recreate_runner.sh)
(cd "${NODE_NAME}_3" && /bin/bash recreate_runner.sh)
(cd "${NODE_NAME}_4" && /bin/bash recreate_runner.sh)
(cd "${NODE_NAME}_5" && /bin/bash recreate_runner.sh)
(cd "${NODE_NAME}_6" && /bin/bash recreate_runner.sh)
(cd "${NODE_NAME}_7" && /bin/bash recreate_runner.sh)
(cd "${NODE_NAME}_8" && /bin/bash recreate_runner.sh)
(cd "${NODE_NAME}_9" && /bin/bash recreate_runner.sh)


