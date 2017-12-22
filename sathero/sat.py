# coding: utf-8
#

__author__ = 'Staale Helleberg'
__copyright__ = 'Copyright 2017'
__license__ = 'MIT'
__version__ = '0.0.1'

import struct

class sat():

	def __init__(self, **kwargs):
		self.config=dict(kwargs)
		self.tp=[]

	def add_tp(self, **kwargs):
		self.tp.append(dict(kwargs))

	def get_tp_bin(self):
		res=b''

		for tp in self.tp:
			pol_mask=1 if tp['pol'] in ['V'] else 0
			f= (pol_mask << 14) | int(tp['freq'])
			this=b''

			this+=struct.pack("<H", f)
			this+=struct.pack("<H", int(tp['symrate']))

			res+=this


		return res

