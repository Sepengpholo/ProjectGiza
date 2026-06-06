import os
import subprocess

def run_git(args, cwd):
    # This environment points Git to a local 'ssh_config' 
    # and forces it to accept keys without needing to write to /opt/render
    env = os.environ.copy()
    env["GIT_SSH_COMMAND"] = "ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no"
    
    result = subprocess.run(["git"] + args, cwd=cwd, env=env, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"GIT ERROR: {result.stderr}")
    return result

def bootstrap():
    print("--- Bootstrapping Node ---")
    repo_dir = os.path.abspath("gist_repo")
    
    # Force clean start if directory exists
    if os.path.exists(os.path.join(repo_dir, ".git")):
        print("Repo exists, skipping clone.")
    else:
        print(f"Cloning into {repo_dir}...")
        run_git(["clone", "git@gist.github.com:8b44dc1fca767767acc448045c9025b7.git", "."], repo_dir)

    run_git(["config", "user.email", "eddiepholo@gmail.com"], repo_dir)
    run_git(["config", "user.name", "Sepengpholo"], repo_dir)

    with open(os.path.join(repo_dir, "nodes.txt"), "w") as f:
        f.write("Node active via Bootstrap")
    
    run_git(["add", "nodes.txt"], repo_dir)
    run_git(["commit", "-m", "Bootstrap update"], repo_dir)
    
    print("Pushing to GitHub...")
    push_res = run_git(["push", "origin", "main"], repo_dir)
    print(f"Push Result: {push_res.stdout}")

if __name__ == "__main__":
    bootstrap()
