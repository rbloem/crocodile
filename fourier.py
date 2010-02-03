"""
Python 2.6

This module contains the functions to do a fourier transform.

"""

from __future__ import print_function
from __future__ import division

import pdb

import numpy as np
import pylab
import matplotlib as plt

import constants

reload(constants)



def rb_fft_1d(data_t, undersampling, fft_shift_flag=0):
    """
    This function does a 1D fourier transform of the data. 
    INPUT:
        data_t: the data in the time domain
        undersampling: the undersampling
        fft_shift_flag: is 0 or 1. In the latter case, the t=0 is in the middle and has to be shifted.
    OUTPUT:
        data_ft: the fourier transformed data
        
    The function assumes that the time array is longer than the amount of pixels. This might become a problem for 64 pixel arrays.   
    
    """
    

    # the data should have the shape time * pixels        
    x, y = np.shape(data_t)
    if y > x:
        data_t = data_t.T
        transpose_FLAG=True
        n_t, n_pix = y, x
    else:
        transpose_FLAG=False
        n_t, n_pix = x, y      
    
    if n_t % 2 == 0:
        status_BOOL = True
    else:
        status_BOOL = False
        print("ERROR (fourier, rb_fft_1d): The time array has an odd amount of steps. The function terminates.")
        data_FT = 0
        

    
    if status_BOOL: 
    

        
        data_ft=[]    
        for i in range(0, n_pix):
            if fft_shift_flag:
                data_ft = np.append(data_ft, np.fft.fft(np.fft.fftshift(data_t[:,i])))
            else:
                # Do the correction of the first point        
                data_t[0,:]=data_t[0,:]/2 
                data_ft = np.append(data_ft, np.fft.fft(data_t[:,i]))
            
        
        # The data is now one long list
        data_ft=data_ft.reshape(n_pix, n_t)
        
        # Select the correct part
        data_ft=np.hsplit(data_ft,2) 
        if undersampling%2 == 0:                
            data_ft=data_ft[0]
        else:
            data_ft=data_ft[1]
            
        if transpose_FLAG == True:
            data_ft = data_ft.T
    
    return data_ft

def fft_axis(t_array, undersampling):
#    dt=(t_array[1]-t_array[0])
#    n_t = len(t_array)
#    w_array=np.fft.fftfreq(n_t, dt*3e8*100*1e-15*4/(2*undersampling+1))
#    w_array=w_array[:n_t/2]


    dt=(t_array[1]-t_array[0])
    centerperiod=dt*4/(2.0*undersampling+1.0)
    centerfreq=(10**5)/(3.0*centerperiod)
    nt=len(t_array)
    dw=1/(1.0*nt*dt*constants.cms*10**(-13))
    fftstart=centerfreq-(nt/4.0)*dw
    w_array=np.arange(fftstart, fftstart+dw*nt/2.0, dw)

    return w_array
    
    

