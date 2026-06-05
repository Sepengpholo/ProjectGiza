import requests, socket, time

# Replace with your Gist ID and Token
GIST_ID = 8b44dc1fca767767acc448045c9025b7
TOKEN = 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

def update_gist(ip):
    data = {"files": {"nodes.txt": {"content": ip}}}
    headers = {"Authorization": f"token {TOKEN}"}
    requests.patch(f"https://api.github.com/gists/{GIST_ID}", json=data, headers=headers)

while True:
    try:
        ip = socket.gethostbyname(socket.gethostname())
        update_gist(ip)
    except: pass
    time.sleep(60)

