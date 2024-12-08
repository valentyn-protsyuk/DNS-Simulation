
class Cache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = []  # declare cache data member
        self.index = -1

    def searchName(self, query):
        i = 0
        while i < len(self.cache):
            if self.cache[i].name == query:
                return self.cache[i].val
                # return True
            else:
                i += 1

        print("No RR by that name")
        return -1

    # Search based on name and type
    # Returns whole row
    def searchQuery(self, url, infType):
        i = 0
        while i < len(self.cache):
            if (self.cache[i].name == url and self.cache[i].infoType == infType):
                print("Query was found in the table!")
                return self.cache[i]
                # return True
            else:
                i += 1

        print("Query not found in the table")
        return -1



    def returnObject(self, query):
        i = 0
        while i < len(self.cache):
            if self.cache[i].name == query:
                return self.cache[i]  # returns entire object this time

            else:
                i += 1

        print("No Object by that Name")
        return -1



    def getCache(self, query):
        if query in self.cache:
            return self.cache[query]
        else:
            return None

    def searchCache(self, query):
        if query in self.cache:
            return True
        else:
            return False

    def pushCache(self, val):
        if(len(self.cache) >= self.capacity):
            print("Cache is full")
            print(f"Element: '{val}' could not be pushed")
            return None
        else:
            self.cache.append(val)
            self.index += 1

    def delCache(self, val):

        if val in self.cache:

            self.cache.remove(val)
            self.index -= 1

        else:
            print("Element not found")
            return None

    def printCache(self):
        for i in self.cache:
            print(f"ID: {i.id}, Name: {i.name}, Type: {i.infoType}, Value: {i.val}"
                  f", TTL:{i.ttl}, Static: {i.static}")


class RR:
    def __init__(self, id, name, infoType, val, ttl, static):
        self.id = id
        self.name = name
        self.infoType = infoType
        self.val = val
        self.ttl = ttl
        self.static = static
        self.list = [id, name, infoType, val, ttl, static]


    def printAll(self):
        print(self.list)

    def assembleRR(newID ,importantInfoList, newTtl):
        # current highest ID + 1 for a new entry ID
        newID += 1
        return RR(newID, importantInfoList[0], importantInfoList[1] ,importantInfoList[2], newTtl ,0)


# '''
test = Cache(10)

test.pushCache(RR(1, "www.csusm.edu", 'A', "144.37.5.45", "", 1))
test.pushCache(RR(2, "cc.csusm.edu", 'A', "144.37.5.117", "", 1))
test.pushCache(RR(3, "cc1.csusm.edu", 'CNAME', "cc.csusm.edu", "", 1))
test.pushCache(RR(4, "cc1.csusm.edu", 'A', "144.37.5.118", "", 1))
test.pushCache(RR(5, "my.csusm.edu", 'A', "144.37.5.150", "", 1))
test.pushCache(RR(6, "qualcomm.com", "NS", "dns.qualcomm.com", "", 1))

'''
testName = test.returnObject("my.csusm.edu")
if(testName != -1):
    print(testName.val)
else:
    print("It's -1")
'''

'''
nameTest = "qualcomm.com"
if(test.searchName("qualcomm.com")):
    print(nameTest)
    print("SUCCESS")
else:
    print("FAILED")
'''

'''
test = Cache(5)
test.pushCache(1)
test.pushCache(2)
test.pushCache(3)
test.pushCache(4)
test.pushCache(5)
'''

'''
if test.searchCache(3):
    print("Found")
else:
    print("Not found")
'''
    
            
        

