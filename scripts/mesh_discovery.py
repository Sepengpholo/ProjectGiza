import requests
import socket

GIST_ID = "8b44dc1fca767767acc448045c9025b7"
TOKEN = "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"

def update_gist():
    try:
        ip = socket.gethostbyname(socket.gethostname())
        headers = {"Authorization": f"token {TOKEN}"}
        
        # 1. Fetch
        res = requests.get(f"https://api.github.com/gists/{GIST_ID}", headers=headers)
        res.raise_for_status() # This will crash if the token is wrong
        
        content = res.json()['files']['nodes.txt']['content']
        
        # 2. Update
        if ip not in content:
            new_content = f"{content}\n{ip}".strip()
            data = {"files": {"nodes.txt": {"content": new_content}}}
            requests.patch(f"https://api.github.com/gists/{GIST_ID}", headers=headers, json=data)
            print(f"SUCCESS: Registered {ip}")
            
    except Exception as e:
        # This will print the error to your Render dashboard logs
        print(f"CRITICAL ERROR: {e}")

if __name__ == "__main__":
    update_gist()
