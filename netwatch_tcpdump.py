import fileinput
import pymongo
import platform


from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['netwatch']
coll = db['grosmatou_11_01']
print("platerofm", str(platform.node()))
#coll = db[str(platform.node())]

# Usage
# sudo tcpdump -i wlan0 -n  | python ./netwatch.py
#

# Main loop
for line in fileinput.input():
    line = line.rstrip('\n')
    print("LINE", line)
    alldata = line.split(' ')
    if len(alldata) > 4:
        packet = {}
        packet['l'] = line
        if alldata[1] == 'IP6':
            packet['p'] = 'IP6'
            ipsport = alldata[2].split('.')
            try:
                packet['ps'] = int(ipsport.pop())
                packet['ips'] = ipsport[0]
            except:
                packet['ps'] = 0
                packet['ips'] = alldata[2]

            ipdport= alldata[4].split('.')
            try:
                packet['pd'] = int(ipdport.pop())
                packet['ipd'] = ipdport[0]
            except:
                packet['pd'] = 0
                packet['ipd'] = alldata[4]
            packet['date'] = alldata[0]
            try :
                packet['size'] = int(alldata.pop())
            except :
                packet['size'] = 0
                #print line

            print("IP6", packet)
            coll.update({"ps" : packet['ps'], "ipd" : packet['ipd'],
                         "ips" : packet['ips'], "pd" : packet['pd']},
                        {  "$inc": { "N": 1 ,  "siz":packet['size']},
                           #"$push": {"full" : packet['l']},
                           "$currentDate": { "ls": True}      }   ,
                        upsert = True)

        elif alldata[1] == 'IP':
            packet['p'] = 'IP4'
            ipsport = alldata[2].split('.')
            packet['ps'] = int(ipsport.pop())
            packet['ips'] = '.'.join(ipsport)

            ipdport= alldata[4].split('.')
            packet['pd'] = ipdport.pop()
            packet['pd'] = int(str(packet['pd']).replace(':',''))
            packet['ipd'] = '.'.join(ipdport)

            packet['date'] = alldata[0]

            try :
                packet['size'] = int(alldata.pop())
            except :
                packet['size'] = 0
                #print line

            print("IP4", packet)
            coll.update({"ps" : packet['ps'], "ipd" : packet['ipd'],
                         "ips" : packet['ips'], "pd" : packet['pd']},
                        {  "$inc": { "N": 1 ,  "siz":packet['size']},
                           #"$push": {"full" : packet['l']},
                           "$currentDate": { "ls": True}      }   ,
                        upsert = True)
        elif alldata[1] == 'ARP,':
            packet['p'] = 'ARP'
            print("ARP",packet)
            coll.insert(packet)
