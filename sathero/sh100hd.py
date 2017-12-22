# coding: utf-8
#

__author__ = 'Staale Helleberg'
__copyright__ = 'Copyright 2017'
__license__ = 'MIT'
__version__ = '0.0.1'


from . import sathero
import struct

class sh100hd(sathero.sathero):

	def __init__(self):
		super().__init__() 


	def write(self, filename=None):

		num_satellites=len(self.satellites)

		# Update these as we go along
		num_tps=0
		tp_db=b''
		sat_db=b''

		for sat in self.satellites:

			# Build SAT DB entry
			sat_bin=b''

			# Oscillators
			sat_bin+=struct.pack("<H", sat.config['lo1'])
			sat_bin+=struct.pack("<H", sat.config['lo2'])

			# TP for this satellite starts at this entry in the tp database
			sat_bin+=struct.pack("<B", num_tps)
			num_tps+=len(sat.tp)

			if num_tps > 255:
				print("ERROR: Too many transponders for SH100HD (max 255!)")
				return

			# Unknown value ??
			sat_bin+=b'\0'


			# Limit to max 12 char and pad with null
			name=sat.config['name'][:12].encode()
			sat_bin+=name
			sat_bin+=b'\0'*(12-len(name))

			# Length is now 18 bytes

			# Add this entry to the db
			sat_db+=sat_bin

			# Add the TP data to the tp database
			tp_db+=sat.get_tp_bin()



		# Build the header (32 bytes)
		header=b'info' + b'\0'*12 + struct.pack("<H", num_satellites) + struct.pack("<H", num_tps) + b'\0'*12

		# Buld the packet
		packet=header + sat_db + tp_db

		# Pad with zeroes to make 4096 bytes
		packet+=b'\0'*(4096-len(packet))

		# Write to file
		with open(filename, "wb") as f:
			f.write(packet)

