from collections import Counter

from scapy.main import *
from scapy.utils import *

addresses = {"ADD:MAC:HERE:0": "Known Test Phone 1",
             "ADD:MAC:HERE:1": "Known Test Phone 2",
             "ADD:MAC:HERE:2": "Known Test Phone 3"}

# channel 1, two minutes
#packets = rdpcap("/tmp/airportSniffL22mQT.cap")
packets = rdpcap("/tmp/airportSniffkDUjbp.cap")

starting_time = packets[0].time

goodpackets = [pkt for pkt in packets if hasattr(pkt, "type")
                and pkt.type == 0 and pkt.subtype == 4]

interesting_packets = [p for p in goodpackets if p.addr2 in addresses]

with open("output.txt", "w") as outf:
    for p in goodpackets:
        strength = -(256-ord(p.notdecoded[-3:-2]))
        outf.write("\t".join(map(str,
            [p.addr2, addresses.get(p.addr2),
             p.time - starting_time, strength])) + "\n")

addrs = [p.addr2 for p in goodpackets]

print "Captured", len(packets), "packets"

print PHONE_2 in addrs
print PHONE_3 in addrs

def strengths(a):
    ps = [p for p in goodpackets if p.addr2 == a]
    return [-(256-ord(p.notdecoded[-3:-2])) for p in ps]

print strengths(PHONE_2)
print strengths(PHONE_3)

from matplotlib import pyplot as plt
