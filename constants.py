"""
Python 2.6
"""

from __future__ import print_function
from __future__ import division

import pdb

cms=2.99792458*10**8 #Google c in m/s




############################
# THE MOST BASIC CONSTANTS #
############################

#speed of light
c_ms	=	2.9979e8		#m/s
c_cms	=	c_ms*100		#cm/s
c_cmfs	=	c_ms*100*1e-15	#cm/fs

#charge
q 		=	1.6e-19 			

#planck
h 		=	6.626e-34 		





#######################
# DERIVATED CONSTANTS #
#######################

#cm-1 to fs-1
wavenumbersToInvFs 	=	c_cms*1e-15
wavenumbersToInvPs	=	c_cms*1e-12

invFsToWavenumbers	=	1/wavenumbersToInvFs
invPsToWavenumbers	=	1/wavenumbersToInvPs

#fringes to fs
fringeToFs 			= 	632.8e-7/c_cmfs 		#FIXME!!!
