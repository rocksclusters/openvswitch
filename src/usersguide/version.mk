ROLL			= openvswitch
VERSION			= 2.7.2
NAME    		= roll-$(ROLL)-usersguide
RELEASE			= 0

SUMMARY_COMPATIBLE	= $(VERSION)
SUMMARY_MAINTAINER	= Rocks Group
SUMMARY_ARCHITECTURE	= i386, x86_64

ROLL_REQUIRES		= base kernel os
ROLL_CONFLICTS		=
PM.FILES       = /var/www/html/roll-documentation/$(ROLL)/*

