from socket import *
from pickle import *
from test import RR
from test import Cache

# qualComm socket info
qualPort = 21000
qualSocket = socket(AF_INET, SOCK_DGRAM)
qualSocket.bind(('', qualPort))

qualCache = Cache(10)

qualCache.pushCache(RR(1, "www.qualcomm.com", 'A', "104.86.224.205", "", 1))
qualCache.pushCache(RR(2, "qtiack12.qti.qualcomm.com",'A', "129.49.100.21", "", 1))

print("[QualComm Server] Ready to Receive...")
while 1:
    qualMsg, localAddr = qualSocket.recvfrom(2048)
    modQualMsg = qualMsg.decode()

    # get Name and type
    qualQuery = modQualMsg.split(',')

    print(f"\nQualcomm DNS server: Received an {qualQuery[1]} request for hostname {qualQuery[0]}")

    qualSearch = qualCache.searchQuery(qualQuery[0], qualQuery[1])
    if(qualSearch != -1):
        #print("Found in qualcomm server table")
        print(f"Qualcomm DNS server: An {qualQuery[1]} record for hostname {qualQuery[0]} was found")
        response = qualSearch

        # no encode method for RR so take only the most important info
        importantInfo = [response.name, response.infoType, response.val]
    else:
        print(f"Qualcomm DNS server: An {qualQuery[1]} record for hostname {qualQuery[0]} was not found")
        importantInfo = ["Error","from","qualcomm"]

    for i in range(0, 3):
        qualSocket.sendto(importantInfo[i].encode(), localAddr)
    


