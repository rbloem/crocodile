"""
Python 2.6
"""

from __future__ import print_function
from __future__ import division

import pdb  # debugger

#break      b   Set a breakpoint.
#continue   c   Continue with program execution.
#exit       q   Abort the program.
#help       h   Print list of commands or help for a given command.
#list       l   Show source code around current line.
#return     r   Continue execution until the current function returns.

#import logging
 
#logging.basicConfig(level=logging.DEBUG, filename='debug.log')
""" 
logging.basicConfig(level=logging.DEBUG, filename='xdebug.log',
                    format='%(asctime)s %(levelname)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
"""


import time
import numpy as np
import pylab

import imports
import fourier
import plotting
import constants

#logging.debug('This is a debug message 3.')

reload(fourier)
reload(plotting)
reload(imports)
reload(constants)

# the classes should be loaded after the other modules
import mess_data_class
import data2d_class
import phasing_class
import water_class

reload(mess_data_class)
reload(data2d_class)
reload(phasing_class)
reload(water_class)


def test(self):
    print("It works!")

   

        

        
        

###########
# TESTING #
###########

# The testing part, only seen when run directly 
if __name__ == "__main__":

    x=water_class.water("a")
    x.path="testdata/"
    x.importfile()
    x.calc_spectrum()
    
    x.r_correction = [-4.1,0]
    x.correct_freq_axes()
    
    plotting.plt.clf()
    plotting.plt.plot(x.r_axis[0] ,x.s)
    plotting.plt.plot(x.h2o_axis ,x.h2o)


    """
    x=phasing_class.phasing("phase_interferogram-4")
    x.path="testdata/"
    x.importfile()
    x.calc_phase()
    x.show_plot()


#    print(x)

    """
    """
    x=[0,0,0]
    
    x[0]=data2d_class.data2d("L4_trans_1_T300")
    x[0].path="testdata/20091021/"
    x[0].undersampling=2
    x[0].phase=-110
    x[0].importfile(ask_for_input=0)
    x[0].calc_spectrum()
    
    x[1]=data2d_class.data2d("L4_cis_1_T300")
    x[1].path="testdata/20091021/"
    x[1].undersampling=2
    x[1].phase=-110
    x[1].importfile(ask_for_input=0)
    x[1].calc_spectrum()
    
    x[2]=data2d_class.data2d("L4_diff_T300")

    x[2].s=x[0].s-x[1].s
    x[2].s_axis = x[1].s_axis



#    x.calc_spectrum()
    
#    plotting.rb_contour2d(x.r[0], x.r_axis[0], x.r_axis[2]) 
#    plotting.rb_vert_slice(x.s, x.s_axis[2], x.s_axis[0], xwavenr=1600, xmin=-1)
#    plotting.rb_contour2d(x[0].s, x[0].s_axis[2], x[0].s_axis[0], xmin=-1, zlimit=120)
    plotting.rb_contour2d(x[2].s, x[2].s_axis[2], x[2].s_axis[0], xmin=-1, zlimit=50)

    """
    """
    y=data2d("nmad_L4_1_T300")
    y.path="testdata/20091021/"
    y.undersampling=2
    y.phase=-110
    y.r_correction = [0,0,-4]
    y.importfile(ask_for_input=0)
    y.correct_freq_axes()
    y.calc_spectrum()
    
#    plotting.rb_contour2d(y.s, y.s_axis[2], y.s_axis[0], xmin=-1, zlimit=100)
    
    y.PEtoPP(40, 80)
    
#    plotting.plt.plot(y.pp)

    z=pp2d("ppNMAaba")
    z.path="testdata/20091021/"
    z.importfile()
    print(z.r_axis)

    z.r_correction = [-6,0]
    z.correct_freq_axes()
    print(z.r_axis)
    z.calc_spectrum()
    z.show_plot(y)
    """

    

















