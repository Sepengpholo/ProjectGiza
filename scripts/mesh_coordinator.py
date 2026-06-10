import os
import subprocess
import json

REPO_DIR = os.path.join(os.getcwd(), "gist_repo")

def run_git(args):
    return subprocess.run(["git"] + args, cwd=REPO_DIR, capture_output=True, text=True)

def wake_swarm(task_payload):
    print("--- Waking the Swarm ---")
    
    # 1. Pull the latest state from nodes
    run_git(["pull", "origin", "main"])
    
    # 2. Write the broadcast task
    task_file = os.path.join(REPO_DIR, "tasks.json")
    with open(task_file, "w") as f:
        json.dump({"task": task_payload, "status": "active"}, f)
    
    # 3. Broadcast
    run_git(["add", "tasks.json"])
    run_git(["commit", "-m", "Broadcast: Wake command"])
    run_git(["push", "origin", "main"])
    
    print("Swarm notified. Nodes will poll for this task shortly.")

if __name__ == "__main__":
    wake_swarm("INIT_MESH_SYNC")
