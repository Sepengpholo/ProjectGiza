import requests
import sys

# Replace with your actual Personal Access Token (Classic)
TOKEN = "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" 
GIST_ID = "8b44dc1fca767767acc448045c9025b7"

def update_gist(node_id):
    url = f"https://api.github.com/gists/{GIST_ID}"
    
    # These headers are MANDATORY for GitHub API v3
    headers = {
        "Authorization": f"token {TOKEN}",
        "Accept": "application/vnd.github.v3+json",
        "Content-Type": "application/json"
    }
    
    # Data to push: updating nodes.txt
    payload = {
        "files": {
            "nodes.txt": {
                "content": f"Node {node_id} is active"
            }
        }
    }
    
    try:
        response = requests.patch(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            print(f"SUCCESS: Node {node_id} registered.")
        else:
            print(f"FAILED: Node {node_id} - Status: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"ERROR: {str(e)}")

if __name__ == "__main__":
    # We pass the node index as a command-line argument
    node_idx = sys.argv[1] if len(sys.argv) > 1 else "Unknown"
    update_gist(node_idx)
