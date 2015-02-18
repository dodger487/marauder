import fileinput
import sqlite3
import collections

packets = []
addresses = collections.defaultdict(lambda: [])

known = {"ADD:MAC:HERE:0": "Known Test Phone 1",
         "ADD:MAC:HERE:1": "Known Test Phone 2",
         "ADD:MAC:HERE:2": "Known Test Phone 3"}


def process_line(line):
    strength = int(line[:4])
    address = line[4:21]
    packets.append((strength, address))
    addresses[address].append(strength)
    #print "Packets:", len(packets), "Uniques:", len(addresses)
    if len(addresses) > 1000:
        a = addresses.keys()
        a.sort()
        print a
        for mac in known:
            if mac in addresses:
                print known[mac], "has strengths of", addresses[mac]
        raise Exception

for line in fileinput.input():
    if len(line)==26 or len(line)==27:# and line[-2:-1] == "8":
        process_line(line)
