"""
Sniff packets from tshark, submit packets to API
"""

import subprocess
import re

reg = re.compile(":..:..:")

CMD = ("tshark -i en0 -I -T fields -e radiotap.dbm_antsignal -e wlan.ta " +
       "-e wlan.fc.type -e wlan.fc.subtype -e frame.time -e wlan.fcs"
            ).split(" ")

pipe = subprocess.Popen(CMD, stdout=subprocess.PIPE).stdout

for l in pipe:
    if not reg.search(l):
        continue
    print l
