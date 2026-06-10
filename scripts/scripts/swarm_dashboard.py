import os, json, time

def show_dashboard():
    while True:
        # Pull latest registry from Gist
        os.system("git -C gist_repo pull origin main")
        with open("gist_repo/swarm_registry.json", "r") as f:
            data = json.load(f)
        
        os.system('cls' if os.name == 'nt' else 'clear')
        print("--- SWARM DASHBOARD ---")
        print(f"Active Nodes: {len(data['nodes'])}")
        for node, timestamp in data['nodes'].items():
            print(f"Node: {node} | Last Active: {timestamp}")
        time.sleep(10)

if __name__ == "__main__":
    show_dashboard()
