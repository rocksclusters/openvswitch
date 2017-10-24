PKGROOT		= /opt/sed
NAME    	= sedresolve
VERSION 	= 1
RELEASE 	= 1
RPM.FILESLIST	= filelist 
RPM.REQUIRES	= sed
RPM.EXTRAS	= Provides: /usr/bin/sed
RPM.DESCRIPTION = \
This resolves /usr/bin/sed for various packages that explicitly demand it. It isa vacuous package in that it requires sed and provides /usr/bin/sed

