import numpy as np
import pylab as pl
import matplotlib
import matplotlib.pyplot as plt

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



def rb_plot_helper(data, x, y, xmin, xmax, ymin, ymax, zlimit, contours):

    # make the mesh grid
    X, Y = make_mesh(x,y)

    # the contours
    if not zlimit:
        zlimit=find_limit_abs(data)
        print "The z-axis is totally:", round(zlimit,2)
    V=make_contours(contours, zlimit)
    
    # the limits of the axes
    xmin, xmax, ymin, ymax = make_axes_limits(x, y, xmin, xmax, ymin, ymax)
    
    return X, Y, V, xmin, xmax, ymin, ymax



def rb_contour2d_helper(data, X, Y, V, xmin, xmax, ymin, ymax):
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
            - the spacing between the contours
        - the limits for the x and y axes
    """
    X, Y, V, xmin, xmax, ymin, ymax = rb_plot_helper(data, x, y, xmin=0, xmax=0, ymin=0, ymax=0, zlimit=0, contours=21)

    rb_contour2d_helper(data, X, Y, V, xmin, xmax, ymin, ymax)


#def rb_slice(data, x, y, 



if __name__ == "__main__":
    x=[[0,1,2,3]]
    print average_delta(x)



