import os

for i in range(10): 
    print(f"Deploying Node_{i}...")
    # This command tells the new node to start its discovery script in the background
    cmd = f"python3 mesh_discovery.py &"
    
    # If you are using SSH or an API, execute that command now:
    os.system(f"ssh user@node_{i} '{cmd}'") 
    
    # Or, if you're just simulating it for now:
    print(f"Node_{i} initialized and running discovery.")
