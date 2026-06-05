import os
import subprocess

def deploy_nodes():
    for i in range(10):
        # We redirect stdout and stderr to a log file for each node
        log_file = f"node_{i}.log"
        cmd = f"python3 scripts/mesh_discovery.py"
        
        # Open the log file for writing
        with open(log_file, "w") as f:
            subprocess.Popen(cmd.split(), stdout=f, stderr=f)
            
        print(f"Node_{i} launched. Log: {log_file}")

if __name__ == "__main__":
    deploy_nodes()
