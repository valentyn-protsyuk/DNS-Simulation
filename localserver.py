from socket import *
from pickle import *
from test import *
from datetime import datetime, time, timedelta

# LocalServer Info
localPort = 15000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', localPort))

# Qualcomm Server info
qualPort = 21000
qualSocket = socket(AF_INET, SOCK_DGRAM)

# ViaSat Server info
viaPort = 22000
viaSocket = socket(AF_INET, SOCK_DGRAM)

# DNS chain is Local -> Qualcomm -> Viat

'''
use pickle and create an object to send to client containing
information about the query
'''

# initialize Resource Record object


# create Cache obj
localCache = Cache(10)

localCache.pushCache(RR(1, "www.csusm.edu", 'A', "144.37.5.45", "", 1))
localCache.pushCache(RR(2, "cc.csusm.edu", 'A', "144.37.5.117", "", 1))
localCache.pushCache(RR(3, "cc1.csusm.edu", 'CNAME', "cc.csusm.edu", "", 1))
localCache.pushCache(RR(4, "cc1.csusm.edu", 'A', "144.37.5.118", "", 1))
localCache.pushCache(RR(5, "my.csusm.edu", 'A', "144.37.5.150", "", 1))
localCache.pushCache(RR(6, "qualcomm.com", "NS", "dns.qualcomm.com", "", 1))
localCache.pushCache(RR(7, "viasat.com", 'NS', "dns.viasat.com", "", 1))

print("[Local Server] Ready to receive...")
# local server shall wait for response through 'recvfrom' and iterate indefinately
while 1:
    importantInfo = []
    newId = 0

    # Decode message
    msg, clientADDR = serverSocket.recvfrom(2048)
    modMsg = msg.decode()

    # get Name and type
    query = modMsg.split(',')

    # print name & type
    print(f"\nLocal DNS server: The client with IP address XXX sent an {query[1]} request for hostname {query[0]}")
    
    # Figure out ttl
    # seconds since midnight
    now = datetime.now()
    sinceMidnight = (now - now.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()
    # Remove decimals and add 60
    ttl = int(sinceMidnight) + 60
    # convert to string so we can decode/encode it
    ttlString = str(ttl)


    # print Before table
    for rr_instance in localCache.cache:
        """
        print(f"ID: {rr_instance.id}, Name: {rr_instance.name}, Type: {rr_instance.infoType}, Value: {rr_instance.val}"
              f", TTL:{rr_instance.ttl}, Static: {rr_instance.static}")
        """
        # find highest ID
        if (newId < rr_instance.id):
            newId = rr_instance.id

        # while looping check ttl
        if (rr_instance.ttl == ""):
            # from original table do nothing
            pass
        # remove if expired
        elif (int(rr_instance.ttl) < int(sinceMidnight)):
            localCache.delCache(rr_instance)
        elif (int(rr_instance.ttl) > int(sinceMidnight)):
            # still has some time do nothing
            pass
        else:
            importantInfo = ["Error", "wrong", "ttl"]

    # look for entry in the table
    response = localCache.searchQuery(query[0], query[1])

    if (response != -1):  # search query in cache
        print("Local DNS server: Query found in local server RR table")

        # if it is still in the table it should be good
        importantInfo = [response.name, response.infoType, response.val]

    elif ((query[0].find("qualcomm.com") != -1) and response == -1):
        #  query wasn't in cache; Ask qualComm server
        print(f"Local DNS server: An {query[1]} record for hostname {query[0]} was not found")
        print(f"Local DNS server: I sent an {query[1]} request to the qualcomm DNS server for the hostname {query[0]}")

        # send query to qualComm
        qualSocket.sendto(msg, ('localhost', qualPort))

        # wait for viasat response
        for i in range(0, 3):
            qualResponse, qualAddress = qualSocket.recvfrom(2048)
            importantInfo.append(qualResponse.decode())

        localCache.pushCache(RR.assembleRR(newId, importantInfo, ttlString))

    # query wasn't in qualcom ask csusm
    elif ((query[0].find("viasat.com") != -1) and response == -1):
        print(f"Local DNS server: An {query[1]} record for hostname {query[0]} was not found")
        print(f"Local DNS server: I sent an {query[1]} request to the viasat DNS server for the hostname {query[0]}")

        #send query
        viaSocket.sendto(msg, ('localhost', viaPort))

        # wait for viasat response
        for i in range(0, 3):
            viaResponse, viaAddress = viaSocket.recvfrom(2048)
            importantInfo.append(viaResponse.decode())

        if(importantInfo[0] == "Error"):
            pass
        else:
            localCache.pushCache(RR.assembleRR(newId, importantInfo, ttlString))

        # EROR not found at all
    else:
        print(f"Unable to answer query ---> Name: {query[0]}, Type: {query[1]}")
        importantInfo = ["Error", "unable to capture", "requested value"]

    importantInfo.append(ttlString)
    # no encode method for RR so take only the most important info
    for i in range(0, 4):
        serverSocket.sendto(importantInfo[i].encode(), clientADDR)

    print("\nLocal server RR Table after getting response:------------------------------")
    localCache.printCache()
    importantInfo.clear()