import glob
import os

#print(os.listdir('config_files'))
l = set()

for nm in glob.glob("config_files\*.txt"):
    with open(nm) as f:
        for sttr in f:
            if sttr.find("ip address") == 1:
                l.add(sttr.replace("ip address", "").strip())

for i in l:
    print(i)
#print(l)