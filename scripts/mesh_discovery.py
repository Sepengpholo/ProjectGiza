import requests
import socket

GIST_ID = "8b44dc1fca767767acc448045c9025b7"
TOKEN = "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" # Generate a fresh one!

def get_ip():
    return socket.gethostbyname(socket.gethostname())

def update_gist():
    ip = get_ip()
    headers = {"Authorization": f"token {TOKEN}"}
    # Fetch current
    res = requests.get(f"https://api.github.com/gists/{GIST_ID}", headers=headers)
    content = res.json()['files']['nodes.txt']['content']
    
    # Add new IP if not present
    if ip not in content:
        new_content = f"{content}\n{ip}".strip()
        data = {"files": {"nodes.txt": {"content": new_content}}}
        requests.patch(f"https://api.github.com/gists/{GIST_ID}", headers=headers, json=data)
        print(f"Registered IP: {ip}")

if __name__ == "__main__":
    update_gist()
