/*
###########################################################################
#
# This program is part of Zenoss Core, an open source monitoring platform.
# Copyright (C) 2010, Zenoss Inc.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 2 as published by
# the Free Software Foundation.
#
# For complete information please visit: http://www.zenoss.com/oss/
#
###########################################################################
*/

(function(){

var ZC = Ext.ns('Zenoss.component');

function render_link(ob) {
    if (ob && ob.uid) {
        return Zenoss.render.link(ob.uid);
    } else {
        return ob;
    }
}

ZC.vpn_TunnelPanel = Ext.extend(ZC.ComponentGridPanel, {
    constructor: function(config) {
        config = Ext.applyIf(config||{}, {
            componentType: 'vpn_Tunnel',
            fields: [
        	{name: 'status'},
        	{name: 'severity'},
                {name: 'tunnelPeerObjName'},
                {name: 'tunnelPeerIpAddr'},
                {name: 'tunnelState'},
                {name: 'tunnelCommunity'},
                {name: 'monitor'},
		{name: 'monitored'},
                {name: 'locking'},
            ],
            columns: [{
                id: 'severity',
                dataIndex: 'severity',
                header: _t('Events'),
                renderer: Zenoss.render.severity,
                width: 60
            },{
                id: 'status',
                dataIndex: 'status',
                header: _t('Tunnel Status'),
                sortable: true,
                width: 150
            },{
                id: 'tunnelPeerObjName',
                flex: 1,
                dataIndex: 'tunnelPeerObjName',
                header: _t('Peer Name')
            },{
                id: 'tunnelPeerIpAddr',
                dataIndex: 'tunnelPeerIpAddr',
                header: _t('Peer Ip Address'),
                sortable: true,
                width: 200
            },{
                id: 'tunnelCommunity',
                dataIndex: 'tunnelCommunity',
                header: _t('Community'),
                sortable: true,
                width: 300
            },{
                id: 'monitored',
                dataIndex: 'monitored',
                header: _t('Monitored'),
                width: 60
            },{
                id: 'locking',
                dataIndex: 'locking',
                header: _t('Locking'),
		renderer: Zenoss.render.locking_icons,
                width: 60
	    }]
        });
        ZC.vpn_TunnelPanel.superclass.constructor.call(this, config);
    }
});

Ext.reg('vpn_TunnelPanel', ZC.vpn_TunnelPanel);
ZC.registerName('vpn_Tunnel', _t('VPN Tunnel'), _t('VPN Tunnels'));


})();

