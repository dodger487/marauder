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


def submit_batch(batch):
    print "Submitting", len(batch)
    packets = []

    for l in batch:
        spl = l[:-1].split("\t")
        strength, addr, type, subtype, dt, fcs = spl

        dt = datetime.datetime.strptime(dt, "%B %d, %Y %H:%M:%S.%f000")
        dt = (dt - datetime.datetime.utcfromtimestamp(0)).total_seconds()
        # fixed packet structure: designed to save keys
        packets.append([addr, strength, dt, type, subtype])

    #
    values = {"device": MARAUDER_ID, "packets": json.dumps(packets)}

    r = requests.post(QUERY_URL, data=values)
    print r.read()
    
    print "Submitted"


def main(interval):
    """Collect requests by sniffing, submit in batches"""
    CMD = ("tshark -i en0 -I -T fields -e radiotap.dbm_antsignal -e wlan.ta " +
       "-e wlan.fc.type -e wlan.fc.subtype -e frame.time -e wlan.fcs"
            ).split(" ")

    pipe = subprocess.Popen(CMD, stdout=subprocess.PIPE).stdout

    last_time = datetime.datetime.now()
    batch = []

    for i, l in enumerate(pipe):
        if not LINE_REGEX.search(l):
            continue

        batch.append(l)

        now = datetime.datetime.now()
        if (now - last_time).total_seconds() > interval:
            p = multiprocessing.Process(target=submit_batch, args=(batch, ))
            p.start()
            last_time = now


if __name__ == "__main__":
    args = p.parse_args()
    main(interval=args.interval)
