import os
import subprocess
import shutil
import sys

# Paths - ensuring we use the exact location of your key
SSH_KEY_PATH = os.path.expanduser("~/.ssh/id_ed25519")
REPO_URL = "git@gist.github.com:8b44dc1fca767767acc448045c9025b7.git"
REPO_DIR = os.path.join(os.getcwd(), "gist_repo")

def run_git_command(args, cwd):
    # This uses the -i flag to explicitly load your key and ignores all host checks
    ssh_command = f"ssh -i {SSH_KEY_PATH} -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no"
    
    env = os.environ.copy()
    env["GIT_SSH_COMMAND"] = ssh_command
    
    result = subprocess.run(
        ["git"] + args, 
        cwd=cwd, 
        env=env, 
        capture_output=True, 
        text=True
    )
    return result

def bootstrap():
    print("--- Bootstrapping Node ---")
    
    # Verify the key exists before starting
    if not os.path.exists(SSH_KEY_PATH):
        print(f"ERROR: SSH Key not found at {SSH_KEY_PATH}")
        return

    # Clean and setup directory
    if os.path.exists(REPO_DIR):
        shutil.rmtree(REPO_DIR)
    os.makedirs(REPO_DIR)

    # 1. Clone
    print("Cloning...")
    clone_res = run_git_command(["clone", REPO_URL, "."], REPO_DIR)
    
    if clone_res.returncode != 0:
        print(f"CLONE FAILED: {clone_res.stderr}")
        return

    # 2. Configure Identity
    run_git_command(["config", "user.email", "eddiepholo@gmail.com"], REPO_DIR)
    run_git_command(["config", "user.name", "Sepengpholo"], REPO_DIR)
    
    # 3. Update File
    with open(os.path.join(REPO_DIR, "nodes.txt"), "w") as f:
        f.write("Node active via Bootstrap")
        
    # 4. Commit and Push
    run_git_command(["add", "nodes.txt"], REPO_DIR)
    run_git_command(["commit", "-m", "Bootstrap update"], REPO_DIR)
    
    print("Pushing...")
    push_res = run_git_command(["push", "origin", "main"], REPO_DIR)
    
    if push_res.returncode == 0:
        print("SUCCESS: Pushed to GitHub!")
    else:
        print(f"PUSH FAILED: {push_res.stderr}")

if __name__ == "__main__":
    bootstrap()
