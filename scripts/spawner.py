import subprocess
import sys

def deploy_nodes():
    for i in range(10):
        print(f"--- Triggering Node_{i} ---")
        cmd = ["python3", "scripts/mesh_discovery.py"]
        
        # This will pipe the output of the node directly to your dashboard screen
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        stdout, _ = process.communicate()
        
        if stdout:
            print(f"OUTPUT from Node_{i}: {stdout}")
        else:
            print(f"Node_{i} produced no output.")

if __name__ == "__main__":
    deploy_nodes()
