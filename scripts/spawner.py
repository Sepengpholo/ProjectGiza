import os
import time

for i in range(10): 
    print(f"Deploying Node_{i}...")
    # Trigger the deployment
    os.system(f"your_deployment_command_here &")
    
    # Give it a moment to boot up
    time.sleep(5) 
    
    # Check if the process exists on the system
    # This assumes they are running on the same host or via your cloud API
    check = os.popen(f"pgrep -f 'mesh_discovery'").read()
    if check:
        print(f"Node_{i} is ONLINE and reporting.")
    else:
        print(f"Node_{i} FAILED to initialize.")
