import threading
import time
import os
import time
import requests
import json
import asyncio
from aiohttp import web

# Replace with your GitHub API endpoint and authentication token
api_endpoint = "https://api.github.com"
org_name = "golemfactory"
with open("../github_admin.key", "r") as f:
    token = f.read().strip()

headers = {
    "Authorization": f"token {token}"
}

metrics_global = ""



def restart_goth(name: str)-> None:
    # script_loc = os.path.dirname(__file__) 
    # script_dir = os.path.join(script_loc, f'../vagrant/{name}/restart_runner.sh')
    os.system('bash ../vagrant/{name}/restart_runner.sh')
    time.sleep(15)
    

def check_runner_status():

    runners_stats = {}  

    while True:
        try:
            url = f"{api_endpoint}/orgs/{org_name}/actions/runners"
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                runners = response.json()
                print(json.dumps(runners, indent=4))
                for runner in runners["runners"]:
                    runner_name = runner['name'].replace('-', '_')
                    runner_status = runner['status']
                    runner_busy = runner['busy']

                    print(f"Runner: {runner_name}\n  Status: {runner_status}\n  Busy: {runner_busy}")

                    if not (runner_name in runners_stats.keys()):
                        runners_stats[runner_name] = []
                    else:
                        runners_stats[runner_name].append(runner_status)

                    
                    if(len(runners_stats[runner_name]) == 3):
                        if(len(set(runners_stats)) == 1 and 'offline' in runners_stats):
                            restart_goth(runner_name)
                            
                        runners_stats[runner_name] = []


                metric_str = ""
                metric_str += """# HELP runner_is_busy Runner is busy
# TYPE runner_is_busy gauge
"""
                for runner in runners["runners"]:
                    runner_name = runner['name']
                    runner_busy = runner['busy']
                    metric_str += f"""runner_is_busy{"{"}runner="{runner_name}"{"}"} {1 if runner_busy else 0}\n"""

                metric_str += f"""# HELP runner_is_online Runner is online
# TYPE runner_is_online gauge
"""
                for runner in runners["runners"]:
                    runner_name = runner['name']
                    runner_status = runner['status']
                    metric_str += f"""runner_is_online{"{"}runner="{runner_name}"{"}"} {1 if runner_status == "online" else 0}\n"""
                global metrics_global
                metrics_global = metric_str
            else:
                print(f"Failed to retrieve runner status. Status code: {response.status_code}")

            print("Waiting 30 seconds...")
            time.sleep(30)
        except Exception as ex:
            print(f"Exception: {ex}")
            time.sleep(30)


routes = web.RouteTableDef()


@routes.get('/metrics')
async def metrics(request):
    return web.Response(text=metrics_global, content_type="text/plain")


threading.Thread(target=check_runner_status).start()

app = web.Application()
app.add_routes(routes)
web.run_app(app, port=8080, host="127.0.0.1")
