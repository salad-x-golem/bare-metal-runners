import os
import sys
import logging
import datetime
import requests
import dotenv

dotenv.load_dotenv()

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Replace with your GitHub API endpoint and authentication token
api_endpoint = "https://api.github.com"
org_name = "salad-x-golem"
repo_name = "yagna-arkiv-market-matcher"

# Get from environment
token = os.environ.get("GITHUB_TOKEN")
if not token:
    logger.error("GITHUB_TOKEN environment variable not set")
    sys.exit(1)

headers = {
    "Authorization": f"token {token}"
}

filter_name = None
filter_branch = None
filter_user = None
filter_status = None
older_than = None

# filter_name = "Goth integration tests (hybrid-net)"
# filter_branch = "master"
filter_status = "queued"
# older_than = datetime.datetime.now() - datetime.timedelta(days=365)


for page in range(0, 10):
    url = f"{api_endpoint}/repos/{org_name}/{repo_name}/actions/runs?page={page}&per_page=100"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        workflow_runs = response.json()
        number_of_workflow_runs = workflow_runs["total_count"]
        print(f"Number of workflow runs: {number_of_workflow_runs}")
        for workflow_run in workflow_runs["workflow_runs"]:
            if filter_name and workflow_run['name'] != filter_name:
                logger.debug(f"Skipping workflow run because of not filter_name match {workflow_run['name']}")
                continue
            if filter_branch and workflow_run['head_branch'] != filter_branch:
                logger.debug(f"Skipping workflow run because of not filter_branch match {workflow_run['head_branch']}")
                continue
            if filter_user and workflow_run['actor']['login'] != filter_user:
                logger.debug(f"Skipping workflow run because of not filter_user match {workflow_run['actor']['login']}")
                continue
            if filter_status and workflow_run['status'] != filter_status:
                logger.debug(f"Skipping workflow run because of not filter_status match {workflow_run['status']}")
                continue
            if older_than:
                if datetime.datetime.fromisoformat(workflow_run['created_at'].replace('Z', '')) >= older_than:
                    logger.debug(f"Skipping workflow run because of not older_than match {workflow_run['created_at']}")
                    continue

            logger.info(f"Processing workflow run: {workflow_run['name']}")

            print(f"Workflow run: {workflow_run['name']}")
            print(f"  Status: {workflow_run['status']}")
            print(workflow_run)
    else:
        print(f"Failed to retrieve workflows. Status code: {response.status_code} {response.text}")
