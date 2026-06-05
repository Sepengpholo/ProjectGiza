import subprocess
import os
import sys

def register_node(node_id):
    # Using SSH URL for Git
    gist_ssh = "git@gist.github.com:8b44dc1fca767767acc448045c9025b7.git"
    repo_dir = "gist_repo"
    
    # 1. Clone if it doesn't exist
    if not os.path.exists(repo_dir):
        subprocess.run(["git", "clone", gist_ssh, repo_dir], check=True)
    
    # 2. Update the file
    with open(f"{repo_dir}/nodes.txt", "w") as f:
        f.write(f"Node {node_id} is active")
    
    # 3. Commit and push using SSH (no token needed!)
    try:
        subprocess.run(["git", "-C", repo_dir, "add", "nodes.txt"], check=True)
        subprocess.run(["git", "-C", repo_dir, "commit", "-m", f"update node {node_id}"], check=True)
        subprocess.run(["git", "-C", repo_dir, "push"], check=True)
        print(f"Node {node_id}: SUCCESS via SSH")
    except subprocess.CalledProcessError as e:
        print(f"Node {node_id}: FAILED during Git operation")

if __name__ == "__main__":
    node_id = sys.argv[1] if len(sys.argv) > 1 else "Unknown"
    register_node(node_id)
