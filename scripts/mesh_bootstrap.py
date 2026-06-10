import os
import subprocess
import time
import json

REPO_DIR = os.path.join(os.getcwd(), "gist_repo")
SSH_KEY_PATH = "/tmp/id_ed25519"

def run_git(args):
    ssh_cmd = f"ssh -i {SSH_KEY_PATH} -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no"
    env = os.environ.copy()
    env["GIT_SSH_COMMAND"] = ssh_cmd
    return subprocess.run(["git"] + args, cwd=REPO_DIR, env=env, capture_output=True, text=True)

def worker_loop():
    print("--- Worker Active: Listening for tasks ---")
    while True:
        # 1. Update local repo from Gist
        run_git(["pull", "origin", "main"])
        
        # 2. Check for tasks
        task_path = os.path.join(REPO_DIR, "tasks.json")
        if os.path.exists(task_path):
            with open(task_path, "r") as f:
                task = json.load(f)
            
            if task.get("status") == "active":
                print(f"Task Received: {task.get('task')}")
                # Execute logic here
                # ...
                
        time.sleep(30) # Poll every 30 seconds

if __name__ == "__main__":
    worker_loop()
