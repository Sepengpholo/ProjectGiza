import os
import subprocess

def run_git(args, cwd):
    env = os.environ.copy()
    env["GIT_SSH_COMMAND"] = "ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no"
    
    # Ensure cwd exists before running git
    if not os.path.exists(cwd):
        os.makedirs(cwd, exist_ok=True)
        
    result = subprocess.run(["git"] + args, cwd=cwd, env=env, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"GIT ERROR: {result.stderr}")
    return result

def bootstrap():
    print("--- Bootstrapping Node ---")
    # Use a path relative to the current script location to avoid absolute path issues
    repo_dir = os.path.join(os.getcwd(), "gist_repo")
    print(f"Working in: {repo_dir}")
    
    # 1. Clone only if .git doesn't exist
    if not os.path.exists(os.path.join(repo_dir, ".git")):
        print("Cloning...")
        run_git(["clone", "git@gist.github.com:8b44dc1fca767767acc448045c9025b7.git", "."], repo_dir)
    
    # 2. Configure
    run_git(["config", "user.email", "eddiepholo@gmail.com"], repo_dir)
    run_git(["config", "user.name", "Sepengpholo"], repo_dir)

    # 3. Write file
    with open(os.path.join(repo_dir, "nodes.txt"), "w") as f:
        f.write("Node active via Bootstrap")
    
    # 4. Commit and Push
    run_git(["add", "nodes.txt"], repo_dir)
    run_git(["commit", "-m", "Bootstrap update"], repo_dir)
    
    print("Pushing...")
    push_res = run_git(["push", "origin", "main"], repo_dir)
    print(f"Push Result: {push_res.stdout}")

if __name__ == "__main__":
    bootstrap()
