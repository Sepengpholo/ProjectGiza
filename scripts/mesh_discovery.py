import subprocess
import os
import sys

def register_node(node_id):
    repo_dir = os.path.abspath("gist_repo")
    gist_ssh = "git@gist.github.com:8b44dc1fca767767acc448045c9025b7.git"
    
    # 1. Clone if missing
    if not os.path.exists(repo_dir):
        subprocess.run(["git", "clone", gist_ssh, repo_dir], check=True)
    
    # 2. Force Git Identity (The Fix for 128 Error)
    subprocess.run(["git", "-C", repo_dir, "config", "user.email", "eddiepholo@gmail.com"], check=True)
    subprocess.run(["git", "-C", repo_dir, "config", "user.name", "Sepengpholo"], check=True)
    
    # 3. Update file
    file_path = os.path.join(repo_dir, "nodes.txt")
    with open(file_path, "w") as f:
        f.write(f"Node {node_id} is active")
    
    # 4. Commit and Push
    try:
        subprocess.run(["git", "-C", repo_dir, "add", "nodes.txt"], check=True)
        subprocess.run(["git", "-C", repo_dir, "commit", "-m", f"update node {node_id}"], check=True)
        subprocess.run(["git", "-C", repo_dir, "push"], check=True)
        print(f"Node {node_id}: SUCCESS")
    except subprocess.CalledProcessError as e:
        print(f"Node {node_id}: FAILED - {e}")

if __name__ == "__main__":
    node_id = sys.argv[1] if len(sys.argv) > 1 else "Unknown"
    register_node(node_id)
