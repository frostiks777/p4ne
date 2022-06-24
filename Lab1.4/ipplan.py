import ipaddress
import random

class IPv4RandomNetwork(ipaddress.IPv4Network):
    def __init__(self):
        ipaddress.IPv4Network.__init__(self, (random.randrange(0x0B000000, 0xDF000000),
                                              random.randrange(8, 24)),
                                       strict=False)
    def regular(self):
        return not self.is_private and not self.is_multicast
    def key_value(self):
        net = self.network_address
        mask = self.netmask
        return int(mask)*2**32+int(net)

d = {}
for i in range(5):
    net1 = IPv4RandomNetwork()
    while not net1.regular():
        net1 = IPv4RandomNetwork()
    d.update({net1.key_value():net1.exploded})
d = dict(sorted(d.items(), key=lambda item: item[1]))
l = list(d.values())
for a in l:
    print(a)
