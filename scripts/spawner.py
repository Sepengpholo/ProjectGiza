import subprocess

def deploy_nodes():
    for i in range(10):
        # We run it and capture output to print it right here
        cmd = ["python3", "scripts/mesh_discovery.py"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        print(f"--- Node_{i} Output ---")
        if result.stdout:
            print(f"STDOUT: {result.stdout}")
        if result.stderr:
            print(f"STDERR: {result.stderr}")

if __name__ == "__main__":
    deploy_nodes()
