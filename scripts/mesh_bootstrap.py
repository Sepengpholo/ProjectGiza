import os
import subprocess
import time
import json
import shutil

REPO_DIR = os.path.join(os.getcwd(), "gist_repo")
REPO_URL = "git@gist.github.com:8b44dc1fca767767acc448045c9025b7.git"
SSH_KEY_PATH = "/tmp/id_ed25519"

def run_git(args, cwd=REPO_DIR):
    ssh_cmd = f"ssh -i {SSH_KEY_PATH} -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no"
    env = os.environ.copy()
    env["GIT_SSH_COMMAND"] = ssh_cmd
    return subprocess.run(["git"] + args, cwd=cwd, env=env, capture_output=True, text=True)

def ensure_repo():
    # If the folder is missing or not a git repo, clone it fresh
    if not os.path.exists(os.path.join(REPO_DIR, ".git")):
        print("Repo missing or corrupted. Re-cloning...")
        if os.path.exists(REPO_DIR):
            shutil.rmtree(REPO_DIR)
        os.makedirs(REPO_DIR)
        run_git(["clone", REPO_URL, "."], cwd=REPO_DIR)
        run_git(["config", "user.email", "eddiepholo@gmail.com"])
        run_git(["config", "user.name", "Sepengpholo"])

def worker_loop():
    print("--- Worker Active: Listening for tasks ---")
    while True:
        try:
            ensure_repo()
            
            # Pull updates
            run_git(["pull", "origin", "main"])
            
            # Check tasks
            task_path = os.path.join(REPO_DIR, "tasks.json")
            if os.path.exists(task_path):
                with open(task_path, "r") as f:
                    task = json.load(f)
                
                if task.get("status") == "active":
                    print(f"Task Received: {task.get('task')}")
                    # Reset status to avoid infinite loops
                    task["status"] = "completed"
                    with open(task_path, "w") as f:
                        json.dump(task, f)
                    run_git(["add", "tasks.json"])
                    run_git(["commit", "-m", "Task completed"])
                    run_git(["push", "origin", "main"])
                    
        except Exception as e:
            print(f"Loop error: {e}")
            
        time.sleep(30)

if __name__ == "__main__":
    worker_loop()
