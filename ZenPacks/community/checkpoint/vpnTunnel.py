from Globals import InitializeClass, DTMLFile
from Products.ZenModel.DeviceComponent import DeviceComponent
from Products.ZenModel.ManagedEntity import ManagedEntity
from Products.ZenModel.ZenossSecurity import * 
from Products.ZenRelations.RelSchema import ToManyCont, ToOne

DOT_GREEN    = 'green'
DOT_PURPLE   = 'purple'
DOT_BLUE     = 'blue'
DOT_YELLOW   = 'yellow'
DOT_ORANGE   = 'orange'
DOT_RED      = 'red'
DOT_GREY     = 'grey'

SEV_CLEAN    = 0
SEV_DEBUG    = 1
SEV_INFO     = 2
SEV_WARNING  = 3
SEV_ERROR    = 4
SEV_CRITICAL = 5

def manage_addvpnTunnel(context, id, userCreated, REQUEST=None):
    """add vpn manually"""
    vpnid = prepId(id)
    vpn = vpnTunnel(vpnid)
    context._setObject(vpnid, vpn)
    vpn = context._getOb(vpnid)
    vpn.tunnelPeerObjName = id
    #if userCreated: db.setUserCreateFlag()
    if REQUEST is not None:
        REQUEST['RESPONSE'].redirect(context.absolute_url()+'/manage_main')

addvpnTunnel = DTMLFile('dtml/addvpnTunnel',globals())

class vpnTunnel(DeviceComponent, ManagedEntity):

    meta_type = portal_type = "vpn_Tunnel"

    tunnelPeerIpAddr = ""
    tunnelPeerObjName = ""
    tunnelState = ""
    tunnelCommunity = ""
    tunnelSourceIpAddr = ""
    tunnelLinkPriority = ""
    tunnelProbState = ""
    tunnelPeerType = ""
    tunnelType = ""

    statusmap ={3: (DOT_GREEN, SEV_CLEAN, 'Active'),
		4: (DOT_ORANGE, SEV_ERROR, 'Destroy'),
		129: (DOT_ORANGE, SEV_ERROR, 'Idle'),
		130: (DOT_ORANGE, SEV_ERROR, 'Phase1'),
		131: (DOT_ORANGE, SEV_ERROR, 'Down'),
		132: (DOT_ORANGE, SEV_ERROR, 'Init'),
		199: (DOT_RED, SEV_CRITICAL, 'Inactive'),
                }	

    _properties = ManagedEntity._properties + (
        {'id':'tunnelPeerIpAddr', 'type':'string', 'mode':'w'},
        {'id':'tunnelPeerObjName', 'type':'string', 'mode':'w'},
        {'id':'tunnelState', 'type':'string', 'mode':'w'},
        {'id':'tunnelCommunity', 'type':'string', 'mode':'w'},
        {'id':'tunnelSourceIpAddr', 'type':'string', 'mode':'w'},
        {'id':'tunnelLinkPriority', 'type':'string', 'mode':'w'},
        {'id':'tunnelProbState', 'type':'string', 'mode':'w'},
        {'id':'tunnelPeerType', 'type':'string', 'mode':'w'},
        {'id':'tunnelType', 'type':'string', 'mode':'w'},
    )

    _relations = (
        ('CheckpointDevice', ToOne(ToManyCont,'ZenPacks.community.checkpoint.CheckpointDevice','vpnTunnel')),
    )

    # Defining the "perfConf" action here causes the "Graphs" display to be
    # available for components of this type.
    factory_type_information = ({
	'id': 			'vpnTunnel',
	'meta_type':		'vpn_Tunnel',
	'icon': 		'FileSystem_icon.gif',
	'factory': 		'manage_addvpnTunnel',
	'immediate_view': 	'viewvpnTunnel',
        'actions': (
		{ 'id'            : 'status'
                , 'name'          : 'Status'
                , 'action'        : 'viewvpnTunnel'
                , 'permissions'   : (ZEN_VIEW,)
                },
                { 'id'            : 'events'
                , 'name'          : 'Events'
                , 'action'        : 'viewEvents'
                , 'permissions'   : (ZEN_VIEW,)
                },
		{
            	'id': 'perfConf',
            	'name': 'Template',
            	'action': 'objTemplates',
            	'permissions': (ZEN_CHANGE_DEVICE,),
        },),
    },)

    # Custom components must always implement the device method. The method
    # should return the device object that contains the component.
    
    def device(self):
        return self.CheckpointDevice()
        
    def StatusString(self):
	return self.statusmap.get(int(self.tunnelState))[2]

        

InitializeClass(vpnTunnel)
