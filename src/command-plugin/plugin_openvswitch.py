#
# 
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		         version 6.2 (SideWinder)
# 
# Copyright (c) 2000 - 2014 The Regents of the University of California.
# All rights reserved.	
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
# 
# 1. Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright
# notice unmodified and in its entirety, this list of conditions and the
# following disclaimer in the documentation and/or other materials provided 
# with the distribution.
# 
# 3. All advertising and press materials, printed or electronic, mentioning
# features or use of this software must display the following acknowledgement: 
# 
# 	"This product includes software developed by the Rocks(r)
# 	Cluster Group at the San Diego Supercomputer Center at the
# 	University of California, San Diego and its contributors."
# 
# 4. Except as permitted for the purposes of acknowledgment in paragraph 3,
# neither the name or logo of this software nor the names of its
# authors may be used to endorse or promote products derived from this
# software without specific prior written permission.  The name of the
# software includes the following terms, and any derivatives thereof:
# "Rocks", "Rocks Clusters", and "Avalanche Installer".  For licensing of 
# the associated name, interested parties should contact Technology 
# Transfer & Intellectual Property Services, University of California, 
# San Diego, 9500 Gilman Drive, Mail Code 0910, La Jolla, CA 92093-0910, 
# Ph: (858) 534-5815, FAX: (858) 534-7345, E-MAIL:invent@ucsd.edu
# 
# THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS''
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS
# BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN
# IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# 
# @Copyright@
#

import rocks.commands


class Plugin(rocks.commands.Plugin):

	def provides(self):
		return 'test'

	def run(self, args):
		""" """
		# args is a dictionary with 'host' = hostname 
		#                           net_id = net.id
		#                               primary keys interface table
		#                           text = outputText 
		#				list of existing text 
		
		host = str(args['host'])
		netid = int(args['net_id'])
		outputText = args['text']
		OVSBRIDGE = 'ovs-bridge'
		OVSLINK	= 'ovs-link'

		# find the OVS bridge(s) defined on this host
		self.owner.db.execute("""SELECT net.subnet,s.name,net.device FROM networks net, subnets s, nodes n WHERE
			n.name = '%s' AND net.node = n.id AND net.subnet = s.id AND net.module = '%s'""" % (host, OVSBRIDGE))
		ovsbridges = self.db.fetchall()
		if ovsbridges == []:
			return	# there are no bridges

		# find the subnet id, name, module  THIS interface
		self.owner.db.execute("""SELECT n.subnet,s.name,n.module,n.options FROM networks n, subnets s WHERE 
			n.id = '%d' AND s.id = n.subnet""" % netid)
		subnet,sname,module,options = self.db.fetchone()

		if module == OVSBRIDGE:
			outputText.insert(0,"##Configured by Rocks")
			for l in outputText:
				if l.find('ONBOOT') >= 0: outputText.remove(l)
			outputText.append( 'ONBOOT=yes') 
			outputText.append( 'TYPE="OVSBridge"') 
			outputText.append( 'DEVICETYPE="ovs"') 
			outputText.append( 'OVS_EXTRA="%s"' % options )
			outputText.append( 'NM_CONTROLLED="no"')
			outputText.append( 'ROCKS_SUBNET="%s"' % sname)
		elif module == OVSLINK:
			for (brsubid, brsubname, brname) in ovsbridges:
				if brsubid == subnet:
					outputText.insert(0,"##Configured by Rocks")
					for l in outputText:
						if l.find('ONBOOT') >= 0: outputText.remove(l)
					outputText.append('ONBOOT=yes')
					outputText.append('DEVICETYPE=ovs')
					outputText.append('TYPE=OVSPort')
					outputText.append('OVS_BRIDGE=%s' % brname)
					outputText.append('BOOTPROTO=none')
					outputText.append('ROCKS_SUBNET="%s"' % sname)

