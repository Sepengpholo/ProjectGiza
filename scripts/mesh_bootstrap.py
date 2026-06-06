import os
import subprocess
import shutil

def run_git(args, cwd):
    env = os.environ.copy()
    env["GIT_SSH_COMMAND"] = "ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no"
    return subprocess.run(["git"] + args, cwd=cwd, env=env, capture_output=True, text=True)

def bootstrap():
    print("--- Bootstrapping Node ---")
    base_dir = os.getcwd()
    repo_dir = os.path.join(base_dir, "gist_repo")
    
    # 1. Start fresh: Nuke everything
    if os.path.exists(repo_dir):
        shutil.rmtree(repo_dir)
    
    # 2. Clone into a clean state (No dot, let git create the folder)
    print("Cloning fresh...")
    clone_res = run_git(["clone", "git@gist.github.com:8b44dc1fca767767acc448045c9025b7.git"], base_dir)
    
    if clone_res.returncode != 0:
        print(f"CLONE FAILED: {clone_res.stderr}")
        return

    # 3. Configure and Update
    run_git(["config", "user.email", "eddiepholo@gmail.com"], repo_dir)
    run_git(["config", "user.name", "Sepengpholo"], repo_dir)
    
    with open(os.path.join(repo_dir, "nodes.txt"), "w") as f:
        f.write("Node active via Bootstrap")
        
    run_git(["add", "nodes.txt"], repo_dir)
    run_git(["commit", "-m", "Bootstrap update"], repo_dir)
    
    print("Pushing...")
    push_res = run_git(["push", "origin", "main"], repo_dir)
    
    if push_res.returncode == 0:
        print("SUCCESS: Pushed to GitHub!")
    else:
        print(f"FAILED: {push_res.stderr}")

if __name__ == "__main__":
    bootstrap()
