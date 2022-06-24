import re
import ipaddress
import glob

def strtoip(sttr):
    if re.match("^(ip address) ([0-9.]+) ([0-9.]+)", sttr):
        m = re.match("^(ip address) ([0-9.]+) ([0-9.]+)", sttr)
        ip = ipaddress.IPv4Interface(m.group(2))
    else:
        ip = None
    return ip

l = set()

for nm in glob.glob("config_files\*.txt"):
    with open(nm) as f:
        for sttr in f:
            if sttr.find("ip address") == 1:
                #l.add(sttr.replace("ip address", "").strip())
                l.add(sttr.strip())
step=0
ls = list()
for i in l:
    step = step+1
    if strtoip(i) != None:
        #print(step, strtoip(i))
        ls.append(strtoip(i))

step = 0
for i in ls:
    step +=1
    print(step, i)

