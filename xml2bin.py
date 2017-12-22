#!/usr/bin/python3
#
# coding: utf-8
#
""" Convert .xml files from e.g.  http://satellites-xml.eu to SatHero binary
"""

__author__ = 'Staale Helleberg'
__copyright__ = 'Copyright 2017'
__license__ = 'MIT'
__version__ = '0.0.1'


import sys, os, struct, glob, datetime
import sathero

# Remember to install python3-lxml
from lxml import etree

modules = {'sh100hd': sathero.sh100hd, 'sh300hd': sathero.sh300hd}

if len(sys.argv) !=3:
	print("Use: %s <version> <folder with ini files>" % sys.argv[0])
	print("\tversion: %s" % (" or ".join(sorted(modules.keys()))))
	quit()

version=sys.argv[1].strip().lower()
if version not in modules:
	print("Does not support %s" % (version))
	quit()

mod = modules[version]()

filename=sys.argv[2]
if not os.path.isfile(filename):
	print("%s not a file" % (filename))
	quit()


tree=etree.parse(filename)
root=tree.getroot()

for sat in root.xpath('./sat'):
#	print(sat.attrib)
	position=float(sat.attrib['position']) / 10.0
	if position < 0.0:
		position+=360.0

	name=sat.attrib['name']

	print("Adding %s - %.1f" % (name, position))

	# Note: Need to specify LNB LOs manually...!
	this_satellite = mod.add_satellite(name=name, position=position, lo1=9750, lo2=10600)

	for tp_data in sat.xpath('./transponder'):
		freq=int(tp_data.attrib['frequency']) / 1000
		pol='V' if tp_data.attrib['polarization'] == '1' else 'H'
		symrate=int(tp_data.attrib['symbol_rate'])/1000

		if freq < 10000:
			continue

		this_satellite.add_tp(freq=freq, pol=pol, symrate=symrate)

	print("\tAdded %d transponders" % (len(this_satellite.tp)))

timestamp=datetime.datetime.now().strftime("%Y%m%d")
bin_file = mod.write("bin/%s_%s" % (version, timestamp))

