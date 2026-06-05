import requests
import socket
import os
import sys

# Replace with your actual Gist ID and a fresh Token
GIST_ID = "8b44dc1fca767767acc448045c9025b7"
TOKEN = "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" 

def register_node():
    try:
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        headers = {"Authorization": f"Bearer {TOKEN}"}
        # Fetch current nodes
        res = requests.get(f"https://api.github.com/gists/{GIST_ID}", headers=headers)
        res.raise_for_status()
        
        content = res.json()['files']['nodes.txt']['content']
        
        # Check and update if IP is new
        if ip not in content:
            new_content = f"{content}\n{ip}".strip()
            data = {"files": {"nodes.txt": {"content": new_content}}}
            requests.patch(f"https://api.github.com/gists/{GIST_ID}", headers=headers, json=data)
            print(f"SUCCESS: Registered {ip}")
        else:
            print(f"Node {ip} already registered.")
            
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    register_node()
