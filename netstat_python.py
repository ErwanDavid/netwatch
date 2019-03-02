import socket
from socket import AF_INET, SOCK_STREAM, SOCK_DGRAM
import time
import psutil
import datetime
from pprint import pprint
from bson.json_util import dumps, loads
import os



AF_INET6 = getattr(socket, 'AF_INET6', object())
proto_map = {
    (AF_INET, SOCK_STREAM):  'tcp',
    (AF_INET6, SOCK_STREAM): 'tcp6',
    (AF_INET, SOCK_DGRAM):   'udp',
    (AF_INET6, SOCK_DGRAM):  'udp6',
}

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def write_json(netdata):
    cpt = 1
    timestr = time.strftime("%Y%m") + "_windows-connection.json"
    logfile = open(timestr, 'w')
    cls()
    sorted_by_value = sorted(netdata.items(), key=lambda kv: kv[1], reverse=True)
    for item in sorted_by_value : 
        connect = {}
        tmp_tab = item[0].split('_')
        connect['src'] = tmp_tab[0]
        connect['dst'] = tmp_tab[1]
        connect['proc'] = tmp_tab[2]
        connect['count'] = item[1]
        strCon = dumps(connect)
        logfile.write(strCon + "\n")
        if (cpt < 20):
            print(strCon)
        cpt += 1
    print("Total", str(cpt))
    logfile.close()

def read_json():
    timestr = time.strftime("%Y%m") + "_windows-connection.json"
    existing_data = {}
    try:
        logfile = open(timestr, 'r')
        data = logfile.readlines()
    except IOError:
        return existing_data
    for line in data:
        try:
            connection = loads(line)
            existing_data[connection['src'] + '_' + connection['dst'] + '_' + connection['proc']] = connection['count']
        except :
            print("ERROR", line)
    return existing_data
    

def main():
    proc_names = {}
    big_status = read_json()
    cpt = 1
    while 1:
        
        for p in psutil.process_iter():
            proc_names[p.pid] = p.name()
        for c in psutil.net_connections(kind='inet'):
            laddr = "%s:%s" % (c.laddr)
            raddr = ""
            if c.raddr:
                raddr = "%s:%s" % (c.raddr)
            if c.status == 'ESTABLISHED':
                logobj = {}
                logobj['proto'] = proto_map[(c.family, c.type)]
                logobj['l_ip'] = laddr
                logobj['r_ip'] = raddr
                logobj['pname'] = proc_names.get(c.pid, '?')
                logobj['dt'] =  datetime.datetime.now()
                local_key = logobj['l_ip'] + '_' +  logobj['r_ip'] + '_' + logobj['pname']
                if local_key in big_status.keys() : 
                    big_status[local_key] += 1
                else :
                    big_status[local_key] = 1
                #logfile.write(json_str)
        if (cpt % 6) == 0 : 
            write_json(big_status)
        cpt += 1
        time.sleep(1)
      
if __name__ == '__main__':
    main()
