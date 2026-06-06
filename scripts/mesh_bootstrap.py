import os
import subprocess
import shutil
import sys

# The target Gist
REPO_URL = "git@gist.github.com:8b44dc1fca767767acc448045c9025b7.git"
REPO_DIR = os.path.join(os.getcwd(), "gist_repo")
# Local file to store host keys (no system access needed)
SSH_KNOWN_HOSTS = os.path.join(os.getcwd(), "temp_known_hosts")

def run_git_command(args, cwd):
    # This configuration forces SSH to use a local file for host keys
    env = os.environ.copy()
    env["GIT_SSH_COMMAND"] = (
        f"ssh -o UserKnownHostsFile={SSH_KNOWN_HOSTS} "
        "-o StrictHostKeyChecking=yes "
        "-o BatchMode=yes"
    )
    
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
    
    # 1. Manually add GitHub to our local temp file so SSH trusts it
    # We use ssh-keyscan to grab the fingerprint safely
    subprocess.run(["ssh-keyscan", "-t", "ed25519", "gist.github.com"], stdout=open(SSH_KNOWN_HOSTS, "w"))

    # 2. Clean and setup directory
    if os.path.exists(REPO_DIR):
        shutil.rmtree(REPO_DIR)
    os.makedirs(REPO_DIR)

    # 3. Clone
    print("Cloning...")
    clone_res = run_git_command(["clone", REPO_URL, "."], REPO_DIR)
    
    if clone_res.returncode != 0:
        print(f"CLONE FAILED: {clone_res.stderr}")
        return

    # 4. Configure and Update
    run_git_command(["config", "user.email", "eddiepholo@gmail.com"], REPO_DIR)
    run_git_command(["config", "user.name", "Sepengpholo"], REPO_DIR)
    
    with open(os.path.join(REPO_DIR, "nodes.txt"), "w") as f:
        f.write("Node active via Bootstrap")
        
    run_git_command(["add", "nodes.txt"], REPO_DIR)
    run_git_command(["commit", "-m", "Bootstrap update"], REPO_DIR)
    
    print("Pushing...")
    push_res = run_git_command(["push", "origin", "main"], REPO_DIR)
    
    if push_res.returncode == 0:
        print("SUCCESS: Pushed to GitHub!")
    else:
        print(f"PUSH FAILED: {push_res.stderr}")

if __name__ == "__main__":
    bootstrap()        print(f"Node {node_id} successfully deployed.")
    else:
        print(f"Push failed: {push_res.stderr}")

if __name__ == "__main__":
    node_id = sys.argv[1] if len(sys.argv) > 1 else "0"
    deploy_node(node_id)
