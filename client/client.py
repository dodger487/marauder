"""
Sniff packets from tshark, submit packets to API
"""

import os
import subprocess
import multiprocessing
import requests
import re
import datetime
import json
import urllib2
import argparse

#QUERY_URL = "http://localhost:8000/packets/submit_packets"
QUERY_URL = "http://marauderio.herokuapp.com/packets/submit_packets"
DEFAULT_INTERVAL = 2

LINE_REGEX = re.compile(":..:..:")

try:
    MARAUDER_ID = os.environ["MARAUDER_ID"]
except KeyError:
    raise KeyError("Must set MARAUDER_ID variable before running the client")

CMD = ("tshark -i en0 -I -T fields -e radiotap.dbm_antsignal -e wlan.ta " +
       "-e wlan.fc.type -e wlan.fc.subtype -e frame.time -e wlan.fcs"
            ).split(" ")


# set up and parse arguments

p = argparse.ArgumentParser(description=
                            'Sniff and submit packets to marauder.')
p.add_argument('--interval', dest='interval',
                    default=DEFAULT_INTERVAL,
                    help='time (in seconds) between submissions')
p.add_argument('--infile', dest='infile',
                    default=None,
                    help='infile to send to server instead of capturing packets')
p.add_argument('--outfile', dest='outfile',
                    default=None,
                    help='outfile to write to instead of submitting to API')


def submit_batch(batch):
    print "Submitting", len(batch)
    packets = []

    for l in batch:
        spl = l[:-1].split("\t")
        strength, addr, type, subtype, dt, fcs = spl

        #dt = datetime.datetime.strptime(dt, "%B %d, %Y %H:%M:%S.%f000")
        #dt = (dt - datetime.datetime.utcfromtimestamp(0)).total_seconds()
        # fixed packet structure: designed to save keys
        packets.append([addr, strength])

    #
    values = {"listening_device": MARAUDER_ID, "packets": json.dumps(packets)}

    r = requests.post(QUERY_URL, data=values)
    print r.content
    
    print "Submitted"


def process_file(interval, infile):
    with open(infile, "rb") as packetfile:
        batch = []
        start_time = None
        for l in packetfile:
            batch.append(l)
            spl = l[:-1].split("\t")
            strength, addr, type, subtype, dt, fcs = spl
            dt = datetime.datetime.strptime(dt, "%B %d, %Y %H:%M:%S.%f000")
            dt = (dt - datetime.datetime.utcfromtimestamp(0)).total_seconds()
            if not start_time:
                start_time = dt
            else:
                if dt - start_time > interval:
                    start_time = None
                    submit_batch(batch)
                    batch = []
        

def main(interval, infile=None, outfile=None):
    """Collect requests by sniffing, submit in batches"""
        
    if infile:
        process_file(interval, infile)
        return
    
    CMD = ("tshark -i en0 -I -T fields -e radiotap.dbm_antsignal -e wlan.ta " +
       "-e wlan.fc.type -e wlan.fc.subtype -e frame.time -e wlan.fcs"
            ).split(" ")

    pipe = subprocess.Popen(CMD, stdout=subprocess.PIPE).stdout

    last_time = datetime.datetime.now()
    batch = []
    if outfile is not None:
        outf = open(outfile, "w")

    for i, l in enumerate(pipe):
        if not LINE_REGEX.search(l):
            continue

        if outfile is not None:
            outf.write(l)
            continue

        batch.append(l)

        now = datetime.datetime.now()
        if (now - last_time).total_seconds() > interval:
            p = multiprocessing.Process(target=submit_batch, args=(batch, ))
            p.start()
            last_time = now


if __name__ == "__main__":
    args = p.parse_args()
    main(interval=args.interval, infile=args.infile, outfile=args.outfile)
