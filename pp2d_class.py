"""
Python 2.6
"""

from __future__ import print_function
from __future__ import division

import pdb
import time
import numpy as np
import pylab

import mess_data_class

import imports

import fourier
import plotting
import constants 


##############################
# PUMP PROBE IN THE 2D SETUP #
##############################

class pp2d(mess_data_class.mess_data):
    """
    This class contains pump probe measurements done with the 2D setup. There is one diagram that consists of the frequency axis and the four measurements.    
    """

    def __init__(self, base_filename):
        mess_data_class.mess_data.__init__(self, diagrams=1, dimensions=2)
        self.base_filename = base_filename
        self.r_domain = ["f", "m"]
        self.s_domain = ["f", "m"]

    def importfile(self):
        self.r[0], self.r_axis[0], self.r_axis[1] = imports.import_file_table(self.path + self.base_filename + ".dat", has_vert_axis=1, has_hor_axis=1, transpose=1)

        
    def calc_spectrum(self):
        self.pp=np.arange(30,dtype="float")
        for i in range(0,30):
            self.pp[i]=-self.r[0][i][0]-self.r[0][i][1]+self.r[0][i][2]+self.r[0][i][3]
        
        
    def show_plot(self, PEtoPPclass):
        """
        This function will plot the pump probe measurement and the 2D 
        """    
    
        plotting.plt.clf

        # the pump probe spectrum is scaled, to make a good comparison possible.        
        max2d=max(PEtoPPclass.pp)
        maxpp=max(self.pp)
        scaling=max2d/maxpp
        
        # plotting the whole stuff            
        plotting.plt.plot(self.r_axis[0], scaling*self.pp)
        plotting.plt.plot(PEtoPPclass.r_axis[2], PEtoPPclass.pp)
        plotting.plt.axhline(y=0)     
            

