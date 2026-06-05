import os
import subprocess
import time

def deploy_nodes():
    for i in range(10):
        print(f"Attempting to launch Node_{i}...")
        
        # Trigger the script directly using python3
        # The '&' runs it as a background process
        cmd = "python3 scripts/mesh_discovery.py"
        subprocess.Popen(cmd.split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Give it a tiny moment to spin up
        time.sleep(1)
        
        # Verify the process exists
        check = os.popen("pgrep -f 'mesh_discovery.py'").read().strip()
        if check:
            print(f"Node_{i} confirmed running (PID: {check})")
        else:
            print(f"Node_{i} FAILED to start.")

if __name__ == "__main__":
    deploy_nodes()
