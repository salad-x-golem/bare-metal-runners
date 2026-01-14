#!/bin/bash
set -x

GITHUB_ADMIN_KEY=`cat ../../github_admin.key`
GITHUB_TOKEN=`curl -L -X POST -H "Authorization: Bearer $GITHUB_ADMIN_KEY" -H 'X-GitHub-Api-Version: 2022-11-28' https://api.github.com/orgs/salad-x-golem/actions/runners/registration-token | jq '.token'`

rm -rf quest_data
mkdir -p guest_data
cp ../../node_bootstrap/* guest_data
echo GITHUB_RUNNER_NAME=salad-prov-01 > guest_data/.env
echo GITHUB_RUNNER_TOKEN=$GITHUB_TOKEN >> guest_data/.env
echo GITHUB_RUNNER_LABELS=salad-prov >> guest_data/.env

