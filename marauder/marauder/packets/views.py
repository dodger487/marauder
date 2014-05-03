from django.shortcuts import render
from models import *
import datetime


def submit_packets(request):
    """
    API for submitting packets to be saved
    """
    device = request.POST.get("device")

    # find the current listener of that device
    listener = Listener.objects.get(device__pk=device, stopped=None)

    packets = request.POST.get("packets", [])
    # fixed packet structure (doesn't use dictionaries to avoid overhead):
    # (address, strength, time)
    
    # TODO: bulk request
    for addr, strength, time in packets:
        # TODO: fix time zones!!
        p = Packet(address=addr, listener=listener,
                   strength=strength,
                   time=datetime.datetime.fromtimestamp(time))
        p.save()
