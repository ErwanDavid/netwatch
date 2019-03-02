from pymongo import MongoClient
from ipwhois import IPWhois
from pprint import pprint


client = MongoClient('mongodb://localhost:27017/')
db = client['netwatch']
coll = db['grosmatou_11_03']

seen_host = {}

for host in coll.find({"DNS": {"$exists": False}}).distinct('ips'):
    if not host in seen_host:
        print("search " + host)

        obj = IPWhois(host)
        results = obj.lookup()
        print("ok")
        coll.update({"ips": host},
                        {"$set": {"DNS":  results}},
                        upsert=True, multi=True)
        pprint(results)
        seen_host[host] = True

for host in coll.find({"DNS": {"$exists": False}}).distinct('ipd'):
    if not host in seen_host:
        print("search " + host)
        try:
            obj = IPWhois(host)
            results = obj.lookup()
            print("ok")
            coll.update({"ipd": host},
                        {"$set": {"DNS":  results}},
                        upsert=True, multi=True)
            pprint(results)
        except:
            print("error ?? " + host)
        seen_host[host] = True


# 192.168.1.96:60243      37.59.243.50:443 mono
# 178.32.100.7 ???
