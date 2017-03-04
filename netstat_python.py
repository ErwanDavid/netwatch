import socket
from socket import AF_INET, SOCK_STREAM, SOCK_DGRAM
import time
import psutil
import datetime
import json
from bson import json_util


AF_INET6 = getattr(socket, 'AF_INET6', object())
proto_map = {
    (AF_INET, SOCK_STREAM):  'tcp',
    (AF_INET6, SOCK_STREAM): 'tcp6',
    (AF_INET, SOCK_DGRAM):   'udp',
    (AF_INET6, SOCK_DGRAM):  'udp6',
}

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj,  datetime.date):
        serial = obj.isoformat()
        return serial
    raise TypeError ("Type not serializable")

def main():
    proc_names = {}
    while 1:
        timestr = time.strftime("%Y%m%d") + "_windows-connection.json"
        logfile = open(timestr, 'a')
        for p in psutil.process_iter():
            try:
                proc_names[p.pid] = p.name()
            except psutil.Error:
                pass
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
                logobj['pid'] = str(c.pid)
                logobj['pname'] = proc_names.get(c.pid, '?')
                #logobj['dt'] =  'ISODate("' + datetime.datetime.now().isoformat() + '")'
                logobj['dt'] =  datetime.datetime.now()
                #logstring = proto_map[(c.family, c.type)] + "\t" +  laddr + "\t" +  raddr + "\t" +  c.status + "\t" +  str(c.pid) + "\t" +  proc_names.get(c.pid, '?')[:15]
                #print(logstring)
                logfile.write(json.dumps(logobj, default=json_util.default) + "\n")
        logfile.close()
        time.sleep(5)
      
if __name__ == '__main__':
    main()
