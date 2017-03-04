# netwatch
Couple of python scripts to analyse ip (v4) connected host to a machine


# netwatch_tcpdump.py
Use tcpdump (so linux friendly) in command line (tcpdump options | this python script)
Require mongodb, as it group data (number of packets and total packets sizes) by host/port, using the upsert facility. 

# netstat_python.py
Use socket lib and run each 5sec to track connected IP/ports. Creates a json file (1 doc per line, tested on mongoimport)

