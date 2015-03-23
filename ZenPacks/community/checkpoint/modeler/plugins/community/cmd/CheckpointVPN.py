import os
from Products.DataCollector.plugins.CollectorPlugin import PythonPlugin
from Products.DataCollector.plugins.DataMaps import ObjectMap
import commands
from Products.ZenUtils.Utils import zenPath
import re

#from Products.DataCollector.plugins.CollectorPlugin import CommandPlugin 


class CheckpointVPN(PythonPlugin):

        transport = "python"
        relname = "vpnTunnel"
        modname = "ZenPacks.community.checkpoint.vpnTunnel"

#	command = '/opt/xensource/bin/xe vm-list is-control-domain=false params'


        def copyDataToProxy(self, device, proxy):
            result = PythonPlugin.copyDataToProxy(self, device, proxy)
            #proxy.guestDevices = [g.id for g in device.guestDevices()]
            return result

        def collect(self, device, log):
                output = ""
                command = 'snmpwalk -Cc -c %s -v1 %s:%s .1.3.6.1.4.1.2620.500.9002.1' % ('qbapub', device.manageIp, 161)
		table = commands.getoutput(command).split('\n')
		ile = len(table)/12
		for i in range(0, ile):
		    output = output + '\n'
		    for j in range(0, 11):
		        output = output + table[i+j*ile] + "\n"
		return output 

        def process(self, device, result, log):

                log.info('processing %s for device %s', self.name(), device.id)
                #log.info('Virtual machines result: %s', result)
                maps = []
		out = []
                rm = self.relMap()
		f1=open('/tmp/testfile', 'w+')
		f1.write(result)
	        vmDataRegex = re.compile(#r'\s*2620.500.9002.1.2*IpAddress:*(?P<ip>.*?)'
        	    #r'.*?2620\.500\.9002\.1\.2.*?STRING: "(?P<name>.*?)"$.*'
        	    r'.*?2620\.500\.9002\.1\.2\.(?P<ip>.*\..*\..*\.*.)\.0.*?STRING: "(?P<name>.*?)"$.*'
        	    r'.*?2620\.500\.9002\.1\.3.*?INTEGER: (?P<state>.*?)$.*'
        	    r'.*?2620\.500\.9002\.1\.4.*?STRING: "(?P<community>.*?)"$.*'
        	    r'.*?2620\.500\.9002\.1\.9.*?INTEGER: (?P<probstate>.*?)$.*'
#        	    r'.*?2620\.500\.9002\.1\.10.*?INTEGER: (?P<peertype>.*?)$.*'
#        	    r'.*?2620\.500\.9002\.1\.11.*?INTEGER: (?P<type>.*?)$.*'
#		    r'networks.*?:\s*(0/ip:\s*)?(?P<ip>.*?)((;.*?)|(\|.*?))?$.*'
            	    , re.M | re.S | re.I)
#
	        for guestData in re.split(r'\n\n', result):
        	    result2 = vmDataRegex.search(guestData)
		    #log.info('guestdata: %s', result2)
		    
	            if result2:
			pass
		        #log.info('guestdata: %s', result2)
	       	        ip = result2.group('ip')
	       	        name = result2.group('name')
	       	        state = result2.group('state')
	       	        community = result2.group('community')
	       	        probstate = result2.group('probstate')
#	       	        peertype = result2.group('peertype')
#	       	        type = result2.group('type')
#	       	        type = result2.group('type')
		    	#log.info('ip: %s', ip)
		    	log.info('name: %s', name)
		    	#log.info('state: %s', state)
		    	#log.info('com: %s', community)
  #              	memory = int(result.group('memory')) / 1024.0 / 1024.0
  	                info = {}
	       	        info['tunnelPeerIpAddr'] = ip
	                info['tunnelPeerObjName'] = name
	                info['tunnelState'] = state
	                info['tunnelCommunity'] = community
	                info['tunnelProbState'] = probstate
			info['tunnelSourceIpAddr'] = '1.3.6.1.4.1.2620.500.9002.1.3.%s' % (ip)
#	                info['tunnelPeerType'] = peertype
#	                info['tunnelType2'] = type
	                om = self.objectMap(info)
	         	om.id = self.prepId(name)
#	            before.discard(om.id)
        	        rm.append(om)
#	        for id in before:
#        	    om = self.objectMap(dict(adminStatus=False))
#	            om.id = id
#        	    rm.append(om)
		maps.append(rm)
	        return maps
