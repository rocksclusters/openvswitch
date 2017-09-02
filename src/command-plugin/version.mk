NAME			= openvswitch-command-plugins
VERSION			= 1
RELEASE			= 4
RPM.REQUIRES		= rocks-pylib
PLUGIN 			= plugin_openvswitch.py
PLUGINDIR		= $(PY.ROCKS)/rocks/commands/report/host/interface
RPM.FILES		= $(PLUGINDIR)/* 
