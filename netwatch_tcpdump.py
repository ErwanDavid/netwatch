import fileinput
import pymongo

from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['netwatch']
coll = db['20151026']

# Usage
# sudo tcpdump -i wlan0 -n  | python ./netwatch.py
#

# Main loop
for line in fileinput.input():
    line = line.rstrip('\n')
    #print line
    alldata = line.split(' ')
    if len(alldata) > 4:
        packet = {}
        packet['l'] = line

        if alldata[1] == 'IP':

            packet['p'] = 'IP'
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
                print line


            coll.update({"ps" : packet['ps'], "ipd" : packet['ipd'],
                         "ips" : packet['ips'], "pd" : packet['pd']},
                        {  "$inc": { "N": 1 ,  "siz":packet['size']},
                           "$currentDate": { "ls": True}      }   ,
                        upsert = True)
        elif alldata[1] == 'ARP,':
            packet['p'] = 'ARP'
            coll.insert(packet)




        #print packet