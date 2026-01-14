#!/bin/bash
set -euo pipefail
set -x

ID="$1"

RUNNER_GROUP=$2

rm -rf "${RUNNER_GROUP}_$ID"
cp -r salad_01 "${RUNNER_GROUP}_$ID"

grep -rl "salad-prov-01" "${RUNNER_GROUP}"_$ID | xargs sed -i "s/salad-prov-01/${RUNNER_GROUP}-prov-$ID/g"

# ---- IP calculation ----
# 192.168.(10 + ID - 1).(10 + ID - 1)
OCTET=$((10 + ID - 1))
IP="192.168.$OCTET.$OCTET"

sed -i -E \
  "s|(config\.vm\.network \"private_network\", ip: \").*(\")|\1$IP\2|" \
  "${RUNNER_GROUP}_$ID/Vagrantfile"