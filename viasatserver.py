from socket import *
from pickle import *
from test import RR
from test import Cache

# viasat socket info
viaPort = 22000
viaSocket = socket(AF_INET, SOCK_DGRAM)
viaSocket.bind(('', viaPort))

viaCache = Cache(10)

viaCache.pushCache(RR(1, "www.viasat.com", 'A', "8.37.96.179", "", 1))

print("[Viasat Server] Ready to Receive...")
while 1:
    viaMsg, localAddr = viaSocket.recvfrom(2048)
    modViaMsg = viaMsg.decode()

    # get Name and type
    viaQuery = modViaMsg.split(',')

    print(f"\nViasat DNS server: Received an {viaQuery[1]} request for hostname {viaQuery[0]}")

    viaSearch = viaCache.searchQuery(viaQuery[0], viaQuery[1])
    if(viaSearch != -1):
        print(f"Viasat DNS server: An {viaQuery[1]} record for hostname {viaQuery[0]} was found")
        response = viaSearch
        # no encode method for RR so take only the most important info
        importantInfo = [response.name, response.infoType, response.val]
    else:
        print(f"Viasat DNS server: An {viaQuery[1]} record for hostname {viaQuery[0]} was not found")
        importantInfo = ["Error", "from", "viasat"]

    for i in range(0, 3):
        viaSocket.sendto(importantInfo[i].encode(), localAddr)