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

################
# DATA2D CLASS #
################
        
class data2d(mess_data_class.mess_data):
    """
    This class is for the measured 2D data. 2D measurements come with two diagrams: rephasing and non-rephasing (r[0] and r[1]). One diagram has three dimensions: time axis, population time and frequency axis.       
    """
    def __init__(self, base_filename):
        mess_data_class.mess_data.__init__(self, diagrams=2, dimensions=3)
        self.base_filename = base_filename
        self.r_domain = ["t", "t", "f"]
        self.s_domain = ["f", "t", "f"]

    def importfile(self, ask_for_input=1):
        """
        This function calls the imports.import_file_table method. 
        It imports both the rephasing and non-rephasing diagrams. 
        It determines the population time by looking at the filename.
        If ask_for_input == 1, it will ask the user for the phase and undersampling. Otherwise, you'll have to provide it separately.    
        """
        self.r[0], self.r_axis[2], self.r_axis[0] = imports.import_file_table(self.path + self.base_filename, has_vert_axis=1, has_hor_axis=1, transpose=0)
        self.r[1], dump, dump = imports.import_file_table(self.path + self.base_filename + "_NR", has_vert_axis=1, has_hor_axis=1, transpose=0)
        try:
            self.r_axis[1] = int(self.base_filename.rsplit("T")[1])
        except IndexError:
            print("ERROR (data2d, importfile): The population time can not be determined. This usually means there is no capital T in the filename.")
                
        if ask_for_input:   
            self.phase = int(raw_input("Phase: "))
            self.undersampling = int(raw_input("Undersampling: "))
    
    def calc_spectrum(self):
        """
        This function calculates the 2DIR spectrum from measurement data. It does a 1D fourier transform and phases the spectra.
        It checks first if there is a spectrum in the first place and if the phase is given. 
        
        """
        if type(self.phase) == bool:
            print("WARNING (data2d, calc_spectrum): The phase was not given. It will now use 0!")
        try:
            phase_rad=self.phase*np.pi/180
            self.s=(    np.exp(-1j*phase_rad) * fourier.rb_fft_1d(self.r[0], self.undersampling) +
                        np.exp( 1j*phase_rad) * fourier.rb_fft_1d(self.r[1], self.undersampling)
                    )
            self.s_axis[2] = self.r_axis[2]
            self.s_axis[0] = fourier.fft_axis(self.r_axis[0], self.undersampling)
        except:
            print("ERROR (data2d, calc_spectrum): The spectrum couldn't be calculated.")
            
    def PEtoPP(self, start, end):
        """
        This function sums a selected part of the fourier transformed axis (from start to end) to a pump probe-like spectrum.
        """    
        self.pp=np.zeros(31)
        for p in range(0,31):
            for w in range(start, end):
                self.pp[p] += self.s[p,w]


