import requests
import json

# Replace with your GitHub API endpoint and authentication token
api_endpoint = "https://api.github.com"
org_name = "golemfactory"
with open("../github_admin.key", "r") as f:
    token = f.read().strip()

headers = {
    "Authorization": f"token {token}"
}

url = f"{api_endpoint}/orgs/{org_name}/actions/runners"
response = requests.get(url, headers=headers)

if response.status_code == 200:
    runners = response.json()
    print(json.dumps(runners, indent=4))
    for runner in runners["runners"]:
        runner_name = runner['name']
        runner_status = runner['status']
        runner_busy = runner['busy']

        print(f"Runner: {runner_name}\n  Status: {runner_status}\n  Busy: {runner_busy}")
        
else:
    print(f"Failed to retrieve runner status. Status code: {response.status_code}")


