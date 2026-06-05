import os
import git # Ensure you have 'gitpython' installed, or we use subprocess safely
import subprocess

def run_git(args, cwd):
    # This captures everything and forces it to your screen
    result = subprocess.run(["git"] + args, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"GIT ERROR: {result.stderr}")
    return result

def bootstrap():
    print("--- Bootstrapping Node ---")
    repo_dir = os.path.abspath("gist_repo")
    
    # Ensure directory exists
    if not os.path.exists(repo_dir):
        print(f"Creating {repo_dir}...")
        os.makedirs(repo_dir, exist_ok=True)
        # Initialize as a fresh repo if clone fails
        run_git(["init"], repo_dir)
        run_git(["remote", "add", "origin", "git@gist.github.com:8b44dc1fca767767acc448045c9025b7.git"], repo_dir)

    # Force Identity
    run_git(["config", "user.email", "eddiepholo@gmail.com"], repo_dir)
    run_git(["config", "user.name", "Sepengpholo"], repo_dir)

    # Update file
    with open(os.path.join(repo_dir, "nodes.txt"), "w") as f:
        f.write("Node active via Bootstrap")
    
    # Commit and Push
    run_git(["add", "nodes.txt"], repo_dir)
    run_git(["commit", "-m", "Bootstrap update"], repo_dir)
    
    print("Pushing...")
    push_res = run_git(["push", "origin", "main"], repo_dir)
    print(f"Final Result: {push_res.stdout}")

if __name__ == "__main__":
    bootstrap()
