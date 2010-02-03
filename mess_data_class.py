"""
Python 2.6
"""

from __future__ import print_function
from __future__ import division

import time
import numpy as np
import pylab

import classtools


###################
# MESS_DATA CLASS #
###################

class mess_data(classtools.ClassTools):
    """
    This class stores all the data. 
    Most of the variables are lists which point to ndarrays with the real data.
    """
    
    def __init__(self, diagrams, dimensions):
        # file stuff
        self.path = ""
        self.base_filename = ""
        self.time_stamp = time.localtime()
        
        # order
        self.dimensions = dimensions        # t1, t2, t3 etc. so 2D -> 3 dimensions
        self.diagrams = diagrams            # number of response functions

        # data
        self.r = [0]*diagrams               # r is a collection of response functions
        self.r_domain = [0]*dimensions      # r_domain about one response function
        self.r_axis = [0]*dimensions        # r_axis are the times/frequencies

        self.r_correction = [0]*dimensions  # correction for spectrometer inaccuracies
        self.r_correction_applied = [0]*dimensions
        
        # spectra
        self.s = [0]                        # s is a collection of response functions
        self.s_domain = [0]*dimensions      # s_domain about one response function
        self.s_axis = [0]*dimensions        # s_axis are the times/frequencies
        
        # other experimental stuff
        self.phase = False                     # in degrees
        self.undersampling = []
        self._comment = ""

    @property
    def comment(self):  
        return self._comment
    @comment.setter
    def comment(self, text):
        self._comment = self._comment + time.strftime("%d/%m/%Y %H:%M:%S: ", time.localtime()) + text + "\n"
        

        
    def correct_freq_axes(self):
        """
        This function will correct a frequency axis by a few of wave numbers. It will add the number, so 1600 cm-1 with a correction of 10 cm-1 becomes 1610 cm-1.
        After the correction has be done, the correction will be written into r_correction_applied and r_correction will be set to zeros. You can run this function as many times as you want, as it will not change anything anymore. 
        If you change r_correction it will of course change the frequency axis again. The extra amount will be added to r_correction_applied and r_correction will be set to zeros. This way, you can always keep track of the total amount of correction you have applied.  
        
        """
        for i in range(0, self.dimensions):
            if self.r_domain[i] == "f":
                for j in range(0, len(self.r_axis[i])):
                    self.r_axis[i][j] += self.r_correction[i]
                self.r_correction_applied[i] += self.r_correction[i]
                self.r_correction[i] = 0
                
    def undo_correct_freq_axes(self):
        """
        You might want to read the instructions of correct_freq_axes first.
        This function will remove all the corrections in one go.
        """
        for i in range(0, self.dimensions):
            if self.r_domain[i] == "f":
                for j in range(0, len(self.r_axis[i])):
                    self.r_axis[i][j] -= self.r_correction_applied[i]
                self.r_correction[i] += self.r_correction_applied[i]
                self.r_correction_applied[i] = 0                


     