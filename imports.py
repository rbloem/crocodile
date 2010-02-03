"""
imports.py

DESCRIPTION
    This file contains functions to import data.

DEPENDENCIES
    numpy 

CHANGELOG
    RB 20091211 - first draft. import_file seems to work for interferograms 
        and 2D data. 3D can be added, but I think we need another function to import 
        all additional 3D-files.
    RB 20091214 - added a function to determine the undersampling.
    RB 20100117 - wrote a new import function import_file_table 
    RB 20100122 - added the format_key function, added some try, except stuff

"""

from __future__ import print_function
from __future__ import division

import numpy as np
import os

debug_FLAG = False

def import_file_table(  path_name_ext, 
                        has_vert_axis=0, 
                        has_hor_axis=0, 
                        transpose=0):
    """
    This function imports a file that has a table view with two axis (so a time 
        and a frequency axis, for example). An example is the 2D setup. The 
        alternative is a list view, as used in the 3D setup.
    INPUT:
        path_name_ext: the path, filename and extension (extension and existence will be checked)
        has_vert_axis=1: this will remove the vertical axis from the output
        has_hor_axis=1: this will remove the horizontal axis from the output
        transpose=1: you can transpose the data. 
        IMPORTANT: the has_vert_axis and has_hor_axis will work on the data as it is in the file. So if you have a file with the frequencies on the first row and you transpose it, you still have to set has_hor_axis=1.
         
    OUTPUT:
        data: the data
        hor_axis: what was on the horizontal axis of the file, independent of transpose
        vert_axis: what was on the vertical axis of the file, independent of transpose
        If an axis is missing, it will give False.
        If the file was not found or someting, data will be False
    
    """

    try:
        path_name_ext = check_for_extension(path_name_ext, extension=".dat")
        
        data = np.loadtxt(path_name_ext)
        
        if transpose == 1:
            data = data.T
            has_vert_axis, has_hor_axis = has_hor_axis, has_vert_axis

        if has_hor_axis == 1:
            hor_axis, data = np.vsplit(data, [1])
            hor_axis = hor_axis[0]
        else:
            hor_axis = False
            
        if has_vert_axis == 1:
            vert_axis, data = np.hsplit(data, [1])
            vert_axis = (vert_axis.T)[0]     # to make it a list, instead of a list with 1D-list
            
            if has_hor_axis == 1:
                dump, hor_axis = np.hsplit(hor_axis, [1])
        else:
            vert_axis = False
            
        if transpose == 1:
            hor_axis, vert_axis = vert_axis, hor_axis
            
    except IOError:
        print("ERROR (imports, import_file_table): Unable to load file", path_name_ext)
        data = False
        hor_axis = False
        vert_axis = False
        
    return data, hor_axis, vert_axis
            


def check_for_extension(path_name_ext, extension=""):
    """
    This is a helper function, to check for the extension.
    
    INPUT:
        extension: if given, it will check if the file has that extension. If not, it will add that extension.

    """
    # check if there is an extension, but only if the extension is given.
    if extension:
        if path_name_ext[-len(extension):] != extension:
            path_name_ext += extension
#            print("NOTE (imports, check_for_extension): the extension", extension, "was added to the filename.")
    
    return path_name_ext


def import_file(name, hasTimeAxis=1, hasFreqAxis=1, TransposeData=0):   
    """
    Imports the interferograms and 2D data. This is independent of the number of 
        interferograms. It reshapes the data to a time (vertical) * 
        interferograms (horizontal) format. 
    
    INPUT:
    name: is the full name of the file (including .dat)
    hasTimeAxis: is 1 for interferograms and 2D data
    hasFreqAxis: is 1 for the 2D data, 0 for the interferograms
    TransposeData: is 1 for the phasing stuff, 0 for the 2D data.
        I don't like this, but it is necesary for the phasing data
    
    OUTPUT:
    n_t: length of the time axis
    n_i: number of interferograms (2 or so for phasing, 31 for 2D or 
        3D measurements)
    time_axis
    freq_axis
    data
    """
    
    data=np.loadtxt(name)
    
    n_t, n_i = np.shape(data)   # Vert, hor, good for the 2D
    
    if TransposeData == 1:      # But the phasing needs some extra love    
        data = data.T
        n_t, n_i = n_i, n_t
    
    n_t -= hasFreqAxis 
    n_i -= hasTimeAxis
   
    if hasTimeAxis: 
        time_axis, data = np.hsplit(data, [1])
        time_axis=(time_axis.T)[0]
    else:
        time_axis=[]

    if hasFreqAxis: 
        freq_axis, data = np.vsplit(data, [1])
        freq_axis=freq_axis[0]
        dump, time_axis = np.hsplit(time_axis, [1])
    else:
        freq_axis=[]
    
    return n_t, n_i, time_axis, freq_axis, data

def find_undersampling(time_axis, guess_period):
    """
    The 2D setup doesn't save the undersampling. This function tries to find the 
        undersampling. However, it would be best to avoid this. 
    """
    deltaT=time_axis[1]-time_axis[0]
    nyquistT=guess_period/4
    test=deltaT/nyquistT
    undersampling=test//2
    
    print("Undersampling has been guessed to be:", undersampling)
    
    return undersampling
    
    
    
# The testing part, only seen when run directly  
if __name__ == "__main__": 


#    print import_file_table("testdata/L4_1_T300.dat", has_vert_axis=1, has_hor_axis=1, transpose=0)


#    find_undersampling([0,25], 20)


    """   
    xn_t, xn_i, xtime_axis, xfreq_axis, xdata=import_file("testdata/phase_interferogram-4.dat", 1,0,1)
    print xn_t, xn_i
    n_t, n_i, time_axis, freq_axis, data=import_file("testdata/L4_1_T300.dat")
    print n_t, n_i
    """
    

 