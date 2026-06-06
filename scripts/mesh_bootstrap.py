import os
import subprocess
import shutil
import sys

# The target Gist
REPO_URL = "git@gist.github.com:8b44dc1fca767767acc448045c9025b7.git"
REPO_DIR = os.path.join(os.getcwd(), "gist_repo")

def run_git_command(args, cwd):
    """Executes a git command with enforced environment variables."""
    # Force Git to ignore system-wide SSH issues and use our memory-only config
    env = os.environ.copy()
    env["GIT_SSH_COMMAND"] = (
        "ssh -o StrictHostKeyChecking=no "
        "-o UserKnownHostsFile=/dev/null "
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

def deploy_node(node_id):
    print(f"--- Node {node_id} Deployment Started ---")
    
    # 1. Clean environment
    if os.path.exists(REPO_DIR):
        shutil.rmtree(REPO_DIR)
    os.makedirs(REPO_DIR)

    # 2. Initialize and Clone
    print("Initializing repository...")
    run_git_command(["init"], REPO_DIR)
    run_git_command(["remote", "add", "origin", REPO_URL], REPO_DIR)
    
    # 3. Pull latest (fetch)
    print("Fetching data...")
    fetch_res = run_git_command(["fetch", "origin"], REPO_DIR)
    if fetch_res.returncode != 0:
        print(f"Fetch failed: {fetch_res.stderr}")
        return

    run_git_command(["checkout", "-b", "main"], REPO_DIR)
    run_git_command(["pull", "origin", "main"], REPO_DIR)

    # 4. Identity
    run_git_command(["config", "user.email", "eddiepholo@gmail.com"], REPO_DIR)
    run_git_command(["config", "user.name", "Sepengpholo"], REPO_DIR)

    # 5. Update
    with open(os.path.join(REPO_DIR, "nodes.txt"), "w") as f:
        f.write(f"Node {node_id} is active")
    
    # 6. Commit and Push
    run_git_command(["add", "nodes.txt"], REPO_DIR)
    run_git_command(["commit", "-m", f"update node {node_id}"], REPO_DIR)
    
    print("Pushing to GitHub...")
    push_res = run_git_command(["push", "origin", "main"], REPO_DIR)
    
    if push_res.returncode == 0:
        print(f"Node {node_id} successfully deployed.")
    else:
        print(f"Push failed: {push_res.stderr}")

if __name__ == "__main__":
    node_id = sys.argv[1] if len(sys.argv) > 1 else "0"
    deploy_node(node_id)
