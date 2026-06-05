import subprocess

def deploy_nodes():
    for i in range(10):
        # We call the script and pass the node ID as an argument
        cmd = ["python3", "scripts/mesh_discovery.py", str(i)]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        print(result.stdout.strip())

if __name__ == "__main__":
    deploy_nodes()
