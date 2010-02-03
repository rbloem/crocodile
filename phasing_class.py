"""
Python 2.6
"""

from __future__ import print_function
from __future__ import division

import time
import numpy as np
import pylab

import mess_data_class

import imports

import fourier
import plotting
import constants 




#################
# PHASING CLASS #
#################

        
        
class phasing(mess_data_class.mess_data):

        
    def __init__(self, base_filename):
        mess_data_class.mess_data.__init__(self, diagrams=1, dimensions=2)
        self.base_filename = base_filename
        self.r_domain = ["t", "m"]
        self.s_domain = ["f", "m"]


    def importfile(self):
        self.r[0], self.r_axis[0], self.r_axis[1] = imports.import_file_table(self.path + self.base_filename, has_vert_axis=0, has_hor_axis=1, transpose=0)
        self.r=self.r[0]

    def show_plot(self):
        plotting.rb_phase_plot(self.r, self.r_axis, self.abs_array, self.phase_array, self.s_axis, self.i_max)  
    
    def calc_phase(self):
        
        self.s = (fourier.rb_fft_1d(self.r, undersampling=0, fft_shift_flag=1)).T
#        self.s = self.s.T
        self.abs_array = abs(self.s)
        self.phase_array = pylab.angle(self.s)
        for i in range(0, np.shape(self.phase_array)[0]):
            for j in range(0, np.shape(self.phase_array)[1]):
                  self.phase_array[i][j] = self.phase_array[i][j]*180/np.pi
        
        
        
        
        n_i=np.shape(self.r)[0]
        n_t=np.shape(self.r)[1]
        
        #calculate the frequency axis
        self.s_axis[0]=np.fft.fftfreq(n_t, 3e8*100*2.11e-15)
        self.s_axis[0]=self.s_axis[0][:n_t/2]
        
        self.i_max=self.abs_array[0].argmax()
        
        print("Frequency, rough guess:", self.s_axis[0][self.i_max])
        #now refine this by weighted averaging???
        #this function is general, but it assumes that s[0] is the best interferogram
        w0=np.average(self.s_axis[0][self.i_max-2:self.i_max+3], weights=self.abs_array[0][self.i_max-2:self.i_max+3])
        print("Frequency, refined guess:", w0)	
        tau=1/(w0*3e8*100e-15)

        #now find the phases at the i_max and the point before and after
        i_fit=list(range(self.i_max-1, self.i_max+2)) #these are three points
        ph=np.zeros(n_i)
        for j in range(0, n_i):
            ph[j]=np.average(self.phase_array[j][i_fit])
        
        print(ph[0], ph[1])
	
        simple_phase= (ph[0] - ph[1])
	
        print(simple_phase)

