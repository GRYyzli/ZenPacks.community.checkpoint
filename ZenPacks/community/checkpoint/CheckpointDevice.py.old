from Globals import InitializeClass
from Products.ZenModel.Device import Device
from Products.ZenModel.ZenossSecurity import ZEN_VIEW
from Products.ZenRelations.RelSchema import *

from copy import copy

class CheckpointDevice(Device):
        "VMWare ESX Server"

        _relations = Device._relations + (
                ('vpnTunnel', ToManyCont(ToOne,
                        "ZenPacks.community.checkpoint.vpnTunnel", "CheckpointDevice")),
                )

        def __init__(self, *args, **kw):
                Device.__init__(self, *args, **kw)
                self.buildRelations()

InitializeClass(CheckpointDevice)

