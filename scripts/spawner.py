import subprocess
import time

def deploy_nodes():
    for i in range(10):
        cmd = ["python3", "scripts/mesh_discovery.py", str(i)]
        subprocess.run(cmd)
        time.sleep(2)  # Wait 2 seconds between nodes to prevent Git collisions
