import subprocess
import sys

def deploy_nodes():
    # Loop through 10 nodes
    for i in range(10):
        # Explicitly call the mesh_discovery script
        cmd = [sys.executable, "scripts/mesh_discovery.py", str(i)]
        
        try:
            # We run with shell=False for security and stability
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            # Print whatever the discovery script says to the main console
            if result.stdout:
                print(result.stdout.strip())
            if result.stderr:
                print(f"Error in Node {i}: {result.stderr.strip()}")
                
        except Exception as e:
            print(f"Spawner failed to start Node {i}: {e}")

if __name__ == "__main__":
    deploy_nodes()
