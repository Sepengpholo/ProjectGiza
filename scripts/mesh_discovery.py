import requests
import sys
import json

# Hard-coded Token and ID to eliminate configuration drift
TOKEN = "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"
GIST_ID = "8b44dc1fca767767acc448045c9025b7"

def register_node(node_id):
    url = f"https://api.github.com/gists/{GIST_ID}"
    
    # We use Bearer and the exact API version required
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "Mesh-Node-Agent"
    }
    
    # Minimal payload
    payload = {
        "files": {
            "nodes.txt": {
                "content": f"Node {node_id} is active"
            }
        }
    }
    
    try:
        response = requests.patch(url, headers=headers, json=payload)
        
        # Log precisely what happened
        if response.status_code == 200:
            print(f"Node {node_id}: SUCCESS")
        else:
            print(f"Node {node_id}: FAILED - Code {response.status_code}")
            print(f"Debug: {response.text}")
            
    except Exception as e:
        print(f"Node {node_id}: ERROR - {str(e)}")

if __name__ == "__main__":
    node_id = sys.argv[1] if len(sys.argv) > 1 else "Unknown"
    register_node(node_id)
