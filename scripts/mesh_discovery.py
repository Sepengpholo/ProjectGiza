import subprocess
import time
import sys

def deploy_nodes():
    print("--- Starting Deployment ---")
    for i in range(10):
        print(f"Triggering Node {i}...")
        cmd = [sys.executable, "scripts/mesh_discovery.py", str(i)]
        
        # We capture stdout and stderr to see EXACTLY what is failing
        proc = subprocess.run(cmd, capture_output=True, text=True)
        
        if proc.stdout:
            print(f"STDOUT: {proc.stdout.strip()}")
        if proc.stderr:
            print(f"STDERR: {proc.stderr.strip()}")
            
        time.sleep(2)
    print("--- Deployment Finished ---")

if __name__ == "__main__":
    deploy_nodes()
