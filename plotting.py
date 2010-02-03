
from __future__ import print_function
from __future__ import division


import numpy as np
import pylab as pl
import matplotlib 
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid import AxesGrid
#from mpl_toolkits.axes_grid.parasite_axes import SubplotHost

cdict = {'red':   [(0.0,  0.0, 0.0),(0.475,  1.0, 1.0),(0.525,  1.0, 1.0),(1.0,  1.0, 1.0)],
         'green': [(0.0,  0.0, 0.0),(0.475,  1.0, 1.0),(0.525,  1.0, 1.0),(1.0,  0.0, 0.0)],
         'blue':  [(0.0,  1.0, 1.0),(0.475,  1.0, 1.0),(0.525,  1.0, 1.0),(1.0,  0.0, 0.0)]}
my_cmap = matplotlib.colors.LinearSegmentedColormap('my_colormap',cdict, 256)


def average_delta(x):
    """
    Make sure you have a one dimensional array. 
    x=[[1,2,3]] will give an error.
    """
    temp=0
    for i in range(0, len(x)-1):
        temp=temp+x[i+1]-x[i]
    temp /= (len(x)-1)
    return temp

def make_mesh(x,y):  
    """
    This functions makes the 2D mesh grid. 
    INPUT:
        x, y: one dimensional arrays with the values of the axes
    OUTPUT:
        X, Y: the meshgrids
    
    """  
    xstart=x[0]
    xres=average_delta(x)
    xend=xstart+xres*len(x)    

    ystart=y[0]
    yres=average_delta(y)
    yend=ystart+yres*len(y) 
        
    X, Y=np.mgrid[xstart:xend:xres, ystart:yend:yres]
    
    return X, Y

def make_contours(contours, zlimit):
    V=np.arange(contours+1)
    delta=(2*zlimit)/float(contours)
    for i in range(0, contours+1):
        V[i]=(-zlimit)+i*delta  
    return V

def make_axes_limits(x, y, xmin, xmax, ymin, ymax):
    """
    This function finds the limits for the axes.
    There are 3 cases:
        1) all xmin etc are 0. In this case, it will plot the whole spectrum
        2) xmin and xmax are given. In this case, ymin=xmin etc
        3) all xmin etc are given. It will return just that.
    There is a special case: 
        1) xmin=-1: both the x and y axes will be the full x axis
        2) ymin=-1: idem, for the y axes
    """
    if xmin == 0 and xmax == 0 and ymin == 0 and ymax == 0:
        xmin = x[0]
        xmax = x[-1]
        ymin = y[0]
        ymax = y[-1]
    if xmin == -1 and xmax == 0 and ymin == 0 and ymax == 0:
        xmin = x[0]
        xmax = x[-1]
        ymin = x[0]
        ymax = x[-1]    
    if xmin == 0 and xmax == 0 and ymin == -1 and ymax == 0:
        xmin = y[0]
        xmax = y[-1]
        ymin = y[0]
        ymax = y[-1]
    """
    if xmin != 0 or xmax != 0:
        if ymin == 0 and ymax == 0:
            ymin = xmin
            ymax = xmax
        else:
            pass
    
    if xmin < x[0]: 
        xmin = x[0]
    if xmax > x[-1]: 
        xmax = x[-1]
    if ymin < y[0]: 
        ymin = y[0]
    if ymax > y[-1]: 
        ymax = y[-1]
    """
    return xmin, xmax, ymin, ymax    

def find_closest_value(thelist, thevalue):
    """
    Does a linear interpolation and finds the closest value.
    """
    a=pl.polyfit(range(0, len(thelist)), thelist, 1)
    
    return round((thevalue-a[1])/a[0])

def find_limit_abs(data):
    ma=data.max()
    mi=data.min()
    if abs(ma) > abs(mi): 
        return abs(ma)
    else: 
        return abs(mi)


def normalize_data(data, normalize_to=1):

    ndata = np.arange(np.shape(data)[0]*np.shape(data)[1], dtype=float)
    ndata = ndata.reshape(np.shape(data)[0],np.shape(data)[1])

    for i in range(0, np.shape(data)[0]):
        ma=max(data[i])
        mi=min(data[i])
        if -mi > ma: ma = -mi
        for j in range(0, np.shape(data)[1]):
            ndata[i][j]=1.0*data[i][j]*normalize_to/ma
            
    return ndata
        
           
    







def rb_plot_init(data, x, y, xmin, xmax, ymin, ymax, zlimit, contours):
    plt.clf()
    
    # make the mesh grid
    X, Y = make_mesh(x,y)

    # the contours
    if not zlimit:
        zlimit=find_limit_abs(data)
        print("The z-axis is totally:", round(zlimit,2))
    V=make_contours(contours, zlimit)
    
    # the limits of the axes
    xmin, xmax, ymin, ymax = make_axes_limits(x, y, xmin, xmax, ymin, ymax)
    
    return X, Y, V, xmin, xmax, ymin, ymax



def plot_rb_contour2d(data, X, Y, V, xmin, xmax, ymin, ymax):
    # the actual plot    
    plt.contourf(X,Y,data, V, cmap=my_cmap, antialiased=True)
    plt.contour(X,Y,data, V, linewidths=1, linestyles="solid", colors="k")
    plt.xlim(xmin, xmax)
    plt.ylim(ymin, ymax)



def rb_contour2d(data, x, y, xmin=0, xmax=0, ymin=0, ymax=0, zlimit=0, contours=21):
    """
    For the plotting you need the following:
        - data
        - meshgrid:
            - x-axis (full)
            - y-axis (full)
        - contours:
            - number of contours
            - the spacing between the contours. zlimit: the total range is 2*zlimit
        - the limits for the x and y axes
    """
    X, Y, V, xmin, xmax, ymin, ymax = rb_plot_init(data, x, y, xmin, xmax, ymin, ymax, zlimit, contours)

    plot_rb_contour2d(data, X, Y, V, xmin, xmax, ymin, ymax)

"""
def rb_vert_slice(data, x, y, xwavenr, xmin=0, xmax=0, ymin=0, ymax=0, zlimit=0, contours=21):
    
    X, Y, V, xmin, xmax, ymin, ymax = rb_plot_init(data, x, y, xmin, xmax, ymin, ymax, zlimit, contours)
    
    xindex=find_closest_value(x, xwavenr)
    print(xindex)
    
    plt.clf()
    fig = plt.figure()
    ax = SubplotHost(fig, 1,1,1, aspect=1.)
#    fig = plt.figure(1, (2., 2.))
    grid = AxesGrid(fig, 111, # similar to subplot(111)
                nrows_ncols = (2, 1), # creates 2x2 grid of axes
                axes_pad=0.1, # pad between axes in inch.
                )    
                
    grid[0].plot(Y[0,:], np.real((data[xindex,])[:]))
    grid[1].contourf(X,Y,data, V, cmap=my_cmap, antialiased=True)
    grid[1].set_xlim(xmin, xmax)
#    grid.axes_llc.set_xticks([xmin, xmax])


"""
def rb_vert_slice(data, x, y, xwavenr, xmin=0, xmax=0, ymin=0, ymax=0, zlimit=0, contours=21):
    
    X, Y, V, xmin, xmax, ymin, ymax = rb_plot_init(data, x, y, xmin, xmax, ymin, ymax, zlimit, contours)
    
    xindex=find_closest_value(x, xwavenr)
    print(xindex)
    
    
    fig = plt.figure(1)
    ax = fig.add_subplot(211)
    ax.plot(
        Y[0,:],
        np.real((data[xindex,])[:]))
    ax.set_xlim(xmin, xmax)

    ax = fig.add_subplot(212)
    plot_rb_contour2d(data, X, Y, V, xmin, xmax, ymin, ymax)
    plt.xlabel(r"$\omega_3 (cm^{-1})$")




def rb_phase_plot(r, r_axis, abs_array, phase_array, s_axis, i_max):
        
        plt.clf()
        
        # adjust the white space        
        plt.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.05, wspace=0.15)
        
        # normalize the time domain data
        rn=normalize_data(r)
        
        # full time domain
        fig = plt.figure(1)
        plt.subplot(221)
        plt.plot(r_axis[0], rn[0])
        plt.plot(r_axis[0], rn[1])
        plt.xlim(r_axis[0][0], r_axis[0][-1])
        plt.ylim(-1.05,1.05)
        plt.yticks([-1,0,1])

        # zoom time domain
        plt.subplot(223)
        plt.plot(r_axis[0], rn[0])
        plt.plot(r_axis[0], rn[1])
        plt.xlim(-10,10)
        plt.ylim(-1.05,1.05)
        plt.yticks([-1,0,1])
        
        # full absolute frequency
        plt.subplot(422)
        plt.plot(s_axis[0], abs_array[0])
        plt.plot(s_axis[0], abs_array[0])
        plt.xlim(s_axis[0][0], s_axis[0][-1])
        plt.xticks([-10])
        
        # full angle 
        plt.subplot(424)
        plt.plot(s_axis[0], phase_array[0])
        plt.plot(s_axis[0], phase_array[1])
        plt.xlim(s_axis[0][0], s_axis[0][-1]) 
        plt.ylim(-180,180)
        plt.yticks([-180,0,180], (r"$-\pi$", 0, r"$\pi$"))
        plt.xticks([0,2000,4000, 6000, 8000])

        # zoom absolute frequency        
        plt.subplot(426)
        plt.plot(s_axis[0], abs_array[0])
        plt.plot(s_axis[0], abs_array[0])
        plt.xlim(s_axis[0][i_max-10], s_axis[0][i_max+10])
        
        # zoom angle
        plt.subplot(428)
        plt.plot(s_axis[0], phase_array[0])
        plt.plot(s_axis[0], phase_array[1])
        plt.xlim(s_axis[0][i_max-10], s_axis[0][i_max+10])        
        plt.ylim(-180,180)
        plt.yticks([-180,0,180], (r"$-\pi$", 0, r"$\pi$"))








if __name__ == "__main__":
    a=[[1,2,3,4],[6,7,8,-9]]
    print(normalize_plots(a))



