from django.db import models
from django.contrib.auth.models import User

MAX_NAME_LENGTH = 32
MAX_ADDR_LENGTH = 12


class Site(models.Model):
    name = models.CharField(max_length=MAX_NAME_LENGTH)
    owner = models.ForeignKey(User)


class DeviceType(models.Model):
    name = models.CharField(max_length=MAX_NAME_LENGTH)


class Device(models.Model):
    name = models.CharField(max_length=MAX_NAME_LENGTH)
    type = models.ForeignKey(DeviceType)


class Listener(models.Model):
    name = models.CharField(max_length=MAX_NAME_LENGTH)
    device = models.ForeignKey(Device)
    site = models.ForeignKey(Site)
    started = models.DateTimeField()
    stopped = models.DateTimeField(null=True)


class Address(models.Model):
    address = models.CharField(max_length=12)
    name = models.CharField(null=True)


class Packet(models.Model):
    address = models.ForeignKey(Address)
    listener = models.ForeignKey(Listener)
    strength = models.SmallIntegerField()
    time = models.DateTimeField()
