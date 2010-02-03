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

#############################
# COMPARE WATER PEAKS CLASS #
#############################

def find_closest_value(thelist, thevalue):
    """
    Does a linear interpolation and finds the closest value.
    """
    a=pylab.polyfit(range(0, len(thelist)), thelist, 1)
    
    return round((thevalue-a[1])/a[0])

def interpolate_spectrum(data, axis, shift, amount):
    """
    data = the data that is to be interpolated
    axis = the accompanying axis
    shift = a shift in where to start
    amount = by how much should it be interpolated
    
    """    
    # reduce the resolution of the H2O spectrum


    
    temp = np.arange(len(data)//amount, dtype=float)     # create a new array with 1/5 the resolution (=1cm-1)
    temp_axis = np.zeros(len(data)//amount, dtype=float)
    
    for i in range(len(temp)):
        temp[i]=0
        temp_axis[i]=0
        for j in range(amount):
            temp[i] += data[amount*i+j+shift]
            temp_axis[i] += axis[amount*i+j+shift]

        temp_axis[i] /= amount
                    
    return temp, temp_axis
        
class water(mess_data_class.mess_data):

    def __init__(self, base_filename):
        mess_data_class.mess_data.__init__(self, diagrams=2, dimensions=2)
        self.base_filename = base_filename
        self.r_domain = ["f", "m"]
        self.s_domain = ["f", "m"]

    def importfile(self):
        """
        This function calls the imports.import_file_table method. 
        It imports both the rephasing and non-rephasing diagrams. 
        It determines the population time by looking at the filename.
        If ask_for_input == 1, it will ask the user for the phase and undersampling. Otherwise, you'll have to provide it separately.    
        """
        self.r[0], self.r_axis[0], self.r_axis[1] = imports.import_file_table(self.path + "ref_no_water", has_vert_axis=1, has_hor_axis=1, transpose=1)
        self.r[1], dump, dump = imports.import_file_table(self.path + "ref_with_water", has_vert_axis=1, has_hor_axis=1, transpose=1)
        self.r[0] = self.r[0][:,0]
        self.r[1] = self.r[1][:,0]

        self.h2o, dump, self.h2o_axis = imports.import_file_table(self.path + "H2O", has_vert_axis=1, has_hor_axis=0, transpose=0)
        self.h2o = (self.h2o.T)[0]
        
        
        
        
        
    def calc_spectrum(self):  
        # calculate the water spectrum      
        self.s=self.r[0]-self.r[1]

        # reduce the H2O spectrum to something more manage-able     
        min_value = int(find_closest_value(self.h2o_axis, self.r_axis[0][0]))
        max_value = int(find_closest_value(self.h2o_axis, self.r_axis[0][-1]))
        
        min_value = min_value + 200 # is 20 cm-1
        max_value = max_value - 200
        
        self.h2o = self.h2o[max_value:min_value] # selects the range from the spectrum, and a bit more
        self.h2o_axis = self.h2o_axis[max_value:min_value]
        
        #interpolate data
#        amountx=int(round((self.r_axis[0][1]-self.r_axis[0][0])/(self.h2o_axis[0]-self.h2o_axis[1]))) # reduction of resolution

#        temp, temp_axis = interpolate_spectrum(self.h2o, self.h2o_axis, 0, 40) #amountx)
        
        """
        
        for i in range(10):
            step = 0.5
            for j in range(len(self.h2o_axis)):
                temp_axis
                
        """            


        
#        self.h2o = temp
#        self.h2o_axis = temp_axis

        # now normalize the spectra to 1
        ma=max(self.s)
        
        for i in range(len(self.s)):
            self.s[i] = self.s[i]/ma
            
        ma=max(self.h2o)
        
        for i in range(len(self.h2o)):
            self.h2o[i] = self.h2o[i]/ma

            























