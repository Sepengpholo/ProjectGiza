import os
import subprocess
import json

REPO_DIR = os.path.join(os.getcwd(), "gist_repo")
SSH_KEY_PATH = "/tmp/id_ed25519"

def run_git(args):
    ssh_cmd = f"ssh -i {SSH_KEY_PATH} -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no"
    env = os.environ.copy()
    env["GIT_SSH_COMMAND"] = ssh_cmd
    return subprocess.run(["git"] + args, cwd=REPO_DIR, env=env, capture_output=True, text=True)

def wake_swarm(command):
    print(f"--- Broadcasting Command: {command} ---")
    
    # Update tasks.json
    with open(os.path.join(REPO_DIR, "tasks.json"), "w") as f:
        json.dump({"task": command, "status": "active"}, f)
        
    run_git(["add", "tasks.json"])
    run_git(["commit", "-m", f"Swarm Command: {command}"])
    run_git(["push", "origin", "main"])

if __name__ == "__main__":
    wake_swarm("PING_ALL_NODES")
