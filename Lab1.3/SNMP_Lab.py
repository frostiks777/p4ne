from pysnmp.hlapi import *

result = getCmd(SnmpEngine(),
                CommunityData("public", mpModel=0),
                UdpTransportTarget(("10.31.70.107", 161)),
                ContextData(), ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysDescr', 0)))
for i in result:
    for s in i[3]:
        print(s)