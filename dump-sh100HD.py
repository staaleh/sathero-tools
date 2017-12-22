#!/usr/bin/python3
#
# coding: utf-8
#
""" Dumps the content of binary files for Sathero SH100HD (and similar) devices
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
sat_data=data[len(header):len(header)+num_satellites*18]
transponder_data = data[len(header)+len(sat_data):len(header)+len(sat_data)+4*num_transponders]


transponders=[]
for y in range(0, num_transponders):
	this_tp=transponder_data[y*4:y*4+4]
	tmp=struct.unpack("<H", this_tp[0:2])[0]
	freq=tmp & 0x3FFF
	pol=(tmp >> 14) & 0x03
	symrate=struct.unpack("<H", this_tp[2:4])[0]
	transponders.append({'freq': freq, 'pol': pol, 'symrate': symrate})



satellites=[]
for x in range(0, num_satellites):
	start=x*18
	sat_info=sat_data[start:start+18]
	lo1=struct.unpack("<H", sat_info[0:2])[0]
	lo2=struct.unpack("<H", sat_info[2:4])[0]
	start_tp=struct.unpack("<B", sat_info[4:5])[0]
	name=sat_info[6:].split(b'\0', 1)[0].decode()

	if len(satellites) > 0:
		prev_sat_start_tp = satellites[-1]['start_tp']
		prev_sat_num_tp=start_tp - prev_sat_start_tp
		satellites[-1]['num_tp'] = prev_sat_num_tp
		satellites[-1]['transponders'] = transponders[ prev_sat_start_tp : prev_sat_start_tp + prev_sat_num_tp]

	satellites.append({'lo1': lo1, 'lo2': lo2, 'start_tp': start_tp, 'name': name})


prev_sat_start_tp = satellites[-1]['start_tp']
prev_sat_num_tp=num_transponders - prev_sat_start_tp
satellites[-1]['num_tp'] = prev_sat_num_tp
satellites[-1]['transponders'] = transponders[ prev_sat_start_tp : prev_sat_start_tp + prev_sat_num_tp]


for sat in satellites:
	print("")
	print("%s: LO %d, %d, %d transponders" % (sat['name'], sat['lo1'], sat['lo2'], sat['num_tp']))

	for tp in sat['transponders']:
		print("\t%d%s - SR: %d" % (tp['freq'], 'V' if tp['pol']>0 else 'H', tp['symrate']))




