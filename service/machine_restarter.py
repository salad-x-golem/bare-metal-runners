import os
import threading
import time

import requests
import logging

from run_in_background import run_process_in_bkg

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)

#set env variables
os.environ('MONITORING_PATTERNS') = ('goth-')

# Replace with your GitHub API endpoint and authentication token
api_endpoint = "https://api.github.com"
org_name = "golemfactory"
with open("../github_admin.key", "r") as f:
    token = f.read().strip()

headers = {
    "Authorization": f"token {token}"
}

TIMEOUT = 700
API_UPDATE_INTERVAL = 120
RECREATE_RUNNER_TIMEOUT = 600


def restart_runner(runner_name):
    runner_dir = runner_name.replace('-', '_')
    working_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), f"../vagrant/{runner_dir}"))
    run_process_in_bkg(["/bin/bash", "recreate_runner.sh"],
                       label="recreate_runner",
                       working_directory=working_directory,
                       timeout=RECREATE_RUNNER_TIMEOUT)


def check_runner_status():
    last_status = {}
    last_offline_times = {}
    while True:
        try:
            url = f"{api_endpoint}/orgs/{org_name}/actions/runners"
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                runners = response.json()
                for runner in runners["runners"]:
                    runner_name = runner['name']
                    runner_status = runner['status']

                    if not runner_name.startswith(os.environ.get('MONITORING_PATTERNS')):
                        continue

                    if runner_name not in last_status:
                        last_status[runner_name] = runner_status

                    if last_status[runner_name] != runner_status and runner_status == "offline":
                        last_offline_times[runner_name] = time.time()
                    elif runner_status != "offline":
                        last_offline_times.pop(runner_name, None)
                    else:
                        if runner_name in last_offline_times:
                            offline_for = time.time() - last_offline_times[runner_name]
                            logger.debug(f"Runner: {runner_name} is offline for: {offline_for}")
                            if offline_for > TIMEOUT:
                                last_offline_times[runner_name] = time.time()
                                restart_runner(runner_name)
                        else:
                            last_offline_times[runner_name] = time.time()

                    logger.info(f"Runner: {runner_name} - Previous status: {last_status[runner_name]} - Status: {runner_status}")
                    last_status[runner_name] = runner_status
            else:
                logger.error(f"Failed to retrieve runner status. Status code: {response.status_code}")

            logger.info(f"Waiting {API_UPDATE_INTERVAL} seconds...")
            time.sleep(API_UPDATE_INTERVAL)
        except Exception as ex:
            print(f"Exception: {ex}")
            time.sleep(API_UPDATE_INTERVAL)


check_runner_status()
