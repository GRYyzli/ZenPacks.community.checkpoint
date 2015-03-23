#! /opt/zenoss/bin/python
import sys
import commands

if len(sys.argv) != 5:
	print "not enought arguments"
	sys.exit()	
	
command = 'snmpwalk -Cc -c %s -v1 %s:%s 1.3.6.1.4.1.2620.500.9002.1.3.%s' % (sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
table = commands.getoutput(command)
try:
	state = table.split(':')[3].lstrip()
	print "check OK|tunnelState=%s" % (state)
except:
	print "check ERROR|tunnelState=199"

