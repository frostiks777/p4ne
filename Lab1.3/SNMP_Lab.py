from pysnmp.hlapi import *

result = getCmd(SnmpEngine(),
                CommunityData("public", mpModel=0),
                UdpTransportTarget(("10.31.70.107", 161)),
                ContextData(), ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysDescr', 0)))

result2 = nextCmd(SnmpEngine(),
                CommunityData("public", mpModel=0),
                UdpTransportTarget(("10.31.70.107", 161)),
                ContextData(),
                ObjectType(ObjectIdentity('1.3.6.1.2.1.2.2.1.2')),
                lexicographicMode=False)

for i in result:
    for s in i[3]:
        print(s)
print('')

for i in result2:
    for s in i[3]:
        print(s)