import os
import subprocess
import shutil

# We now use the /tmp/ location which is guaranteed to be writable
SSH_KEY_PATH = "/tmp/id_ed25519"
REPO_URL = "git@gist.github.com:8b44dc1fca767767acc448045c9025b7.git"
REPO_DIR = os.path.join(os.getcwd(), "gist_repo")

def run_git_command(args, cwd):
    ssh_command = f"ssh -i {SSH_KEY_PATH} -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no"
    env = os.environ.copy()
    env["GIT_SSH_COMMAND"] = ssh_command
    
    return subprocess.run(["git"] + args, cwd=cwd, env=env, capture_output=True, text=True)

def bootstrap():
    print("--- Bootstrapping Node ---")
    
    if not os.path.exists(SSH_KEY_PATH):
        print(f"ERROR: Generate key using: ssh-keygen -t ed25519 -f {SSH_KEY_PATH} -N ''")
        return

    if os.path.exists(REPO_DIR):
        shutil.rmtree(REPO_DIR)
    os.makedirs(REPO_DIR)

    print("Cloning...")
    run_git_command(["clone", REPO_URL, "."], REPO_DIR)
    run_git_command(["config", "user.email", "eddiepholo@gmail.com"], REPO_DIR)
    run_git_command(["config", "user.name", "Sepengpholo"], REPO_DIR)
    
    with open(os.path.join(REPO_DIR, "nodes.txt"), "w") as f:
        f.write("Node active")
        
    run_git_command(["add", "nodes.txt"], REPO_DIR)
    run_git_command(["commit", "-m", "update"], REPO_DIR)
    
    push_res = run_git_command(["push", "origin", "main"], REPO_DIR)
    
    if push_res.returncode == 0:
        print("SUCCESS: Pushed to GitHub!")
    else:
        print(f"PUSH FAILED: {push_res.stderr}")

if __name__ == "__main__":
    bootstrap()
