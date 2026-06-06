import os
import subprocess
import shutil

def run_git(args, cwd):
    env = os.environ.copy()
    env["GIT_SSH_COMMAND"] = "ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no"
    result = subprocess.run(["git"] + args, cwd=cwd, env=env, capture_output=True, text=True)
    return result

def bootstrap():
    print("--- Bootstrapping Node ---")
    repo_dir = os.path.join(os.getcwd(), "gist_repo")
    
    # 1. Nuke the folder if it's broken (doesn't have a proper .git folder)
    if os.path.exists(repo_dir) and not os.path.exists(os.path.join(repo_dir, ".git")):
        print("Cleaning up corrupted directory...")
        shutil.rmtree(repo_dir)

    # 2. Clone fresh if missing
    if not os.path.exists(repo_dir):
        print("Cloning fresh...")
        os.makedirs(repo_dir)
        run_git(["clone", "git@gist.github.com:8b44dc1fca767767acc448045c9025b7.git", "."], repo_dir)

    # 3. Force Remote (Fixes 'origin' error)
    run_git(["remote", "set-url", "origin", "git@gist.github.com:8b44dc1fca767767acc448045c9025b7.git"], repo_dir)
    
    # 4. Identity & Push
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
