import subprocess
import os
import sys

def register_node(node_id):
    # Standardize the directory and URL
    repo_dir = os.path.abspath("gist_repo")
    gist_ssh = "git@gist.github.com:8b44dc1fca767767acc448045c9025b7.git"
    
    print(f"--- Node {node_id} starting ---")

    # 1. Clone if the directory doesn't exist
    if not os.path.exists(repo_dir):
        print("Cloning repository...")
        subprocess.run(["git", "clone", gist_ssh, repo_dir], check=True)
    
    # 2. Update the file
    file_path = os.path.join(repo_dir, "nodes.txt")
    with open(file_path, "w") as f:
        f.write(f"Node {node_id} is active")
    
    # 3. Perform Git operations with explicit paths
    try:
        subprocess.run(["git", "-C", repo_dir, "add", "nodes.txt"], check=True)
        subprocess.run(["git", "-C", repo_dir, "commit", "-m", f"update node {node_id}"], check=True)
        
        # Push and capture output to see why it might be "empty"
        result = subprocess.run(
            ["git", "-C", repo_dir, "push"], 
            capture_output=True, text=True
        )
        
        if result.returncode == 0:
            print(f"Node {node_id}: SUCCESS (Pushed to GitHub)")
        else:
            print(f"Node {node_id}: FAILED")
            print(f"Git Error Details: {result.stderr}")
            
    except subprocess.CalledProcessError as e:
        print(f"Node {node_id}: Git command error: {e}")

if __name__ == "__main__":
    node_id = sys.argv[1] if len(sys.argv) > 1 else "Unknown"
    register_node(node_id)
