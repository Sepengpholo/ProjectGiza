import os

# Loop to create your nodes
for i in range(10): 
    # Add your Colab/Cloud API trigger here to launch the bootstrap
    print(f"Deploying Node_{i}...")
    os.system(f"echo 'Deploying Node_{i} via internal API...'")
