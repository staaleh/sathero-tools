# coding: utf-8
#

__author__ = 'Staale Helleberg'
__copyright__ = 'Copyright 2017'
__license__ = 'MIT'
__version__ = '0.0.1'


from . import sat

class sathero():

	def __init__(self):
		self.satellites=[]


	def add_satellite(self, **kwargs):
		self.satellites.append(sat.sat(**kwargs))
		return self.satellites[-1]
