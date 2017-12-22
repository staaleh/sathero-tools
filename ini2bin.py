#!/usr/bin/python3
#
# coding: utf-8
#
""" Convert .ini files from e.g.  http://satellites-xml.eu or http://www.fastsatfinder.com to SatHero binary
"""

__author__ = 'Staale Helleberg'
__copyright__ = 'Copyright 2017'
__license__ = 'MIT'
__version__ = '0.0.1'


import sys, os, struct, glob, configparser, datetime
import sathero

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

folder=sys.argv[2]
if not os.path.isdir(folder):
	print("%s not a folder" % (folder))
	quit()



config = configparser.ConfigParser()
for f in sorted(glob.glob(os.path.join(folder, "*.ini"))):
	config.read(f)

	position=float(config['SATTYPE']['1']) / 10.0
	name=config['SATTYPE']['2']

	print("Adding %s - %.1f" % (name, position))

	# Note: Need to specify LNB LOs manually...!
	this_satellite = mod.add_satellite(name=name, position=position, lo1=9750, lo2=10600)

	for tp_data in config['DVB'].items():
		if tp_data[0] == '0':
			length=int(tp_data[1])
			continue

		tp=tp_data[1].split(',')

		freq=int(tp[0])
		pol=tp[1]
		symrate=int(tp[2])

		if freq < 10000:
			continue

		if freq > 13000:
			continue

		this_satellite.add_tp(freq=freq, pol=pol, symrate=symrate)

	print("\tAdded %d transponders" % (len(this_satellite.tp)))

timestamp=datetime.datetime.now().strftime("%Y%m%d")
bin_file = mod.write("bin/%s_%s" % (version, timestamp))

