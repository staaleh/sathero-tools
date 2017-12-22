#!/usr/bin/python3
#
# coding: utf-8
#
""" Dumps the content of binary files for Sathero SH300HD (and similar) devices
"""

__author__ = 'Staale Helleberg'
__copyright__ = 'Copyright 2017'
__license__ = 'MIT'
__version__ = '0.0.1'

import sys, os, struct

if len(sys.argv) !=2:
	print("Use: %s <binfile>" % sys.argv[0])
	quit()

filename=sys.argv[1]
if not os.path.isfile(filename):
	print("%s not a file" % filename)
	quit()


with open(filename, "rb") as f:
	data = f.read(8192)

header=data[0:32]
magic=header[0:4].decode()

if magic != u"info":
	print("Unknown magic '%s'" % (magic))
	quit()

num_satellites=struct.unpack("<H", header[16:18])[0]
num_transponders=struct.unpack("<H", header[18:20])[0]
sat_data=data[len(header):len(header)+num_satellites*22]
transponder_data = data[len(header)+len(sat_data):len(header)+len(sat_data)+4*num_transponders]


for x in range(0, num_satellites):
	start=x*22
	sat_info=sat_data[start:start+22]
	lo1=struct.unpack("<H", sat_info[0:2])[0]
	lo2=struct.unpack("<H", sat_info[2:4])[0]
	deg=struct.unpack("<H", sat_info[4:6])[0] / 10.0


	start_tp=struct.unpack("<H", sat_info[6:8])[0]
	num_tp=struct.unpack("<B", sat_info[8:9])[0]
	unknown=struct.unpack("<B", sat_info[9:10])[0]
	name=sat_info[10:].split(b'\0', 1)[0].decode()
	tp_data = transponder_data[start_tp*4:start_tp*4+num_tp*4]

	print("")
	print("%s: LO %d, %d, Deg: %.1f, %d transponders" % (name, lo1,lo2, deg, num_tp))
	for y in range(0, num_tp):
		this_tp=tp_data[y*4:y*4+4]
		tmp=struct.unpack("<H", this_tp[0:2])[0]
		freq=tmp & 0x3FFF
		pol=(tmp >> 14) & 0x03
		symrate=struct.unpack("<H", this_tp[2:4])[0]
		print("\t%d%s - SR: %d" % (freq, 'V' if pol>0 else 'H', symrate))

