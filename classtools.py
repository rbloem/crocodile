"""
classtools.py

DESCRIPTION
    This class contains some general functions for classes.

DEPENDENCIES
    numpy


CHANGELOG
    Adapted from an example in "Learning Python"
    RB 20091214 - first draft.
    RB 20091216 - renamed AttrDisplay to ClassTools
                - rewrote gatherAttrs to use find_types
    RB 20091217 - Added the shelve functions.
"""

import numpy as np
import time

import os.path
import shelve
import sys

####################
# SHELVE FUNCTIONS #
####################

def make_db(array_of_class_instances, base_filename):
    """
    Makes a database and writes all values.
    The input should be an array with class instances, not a class 
        instance itself!
    If the database already exists, it will update the values. Make
        sure that everything stored in the database has the same class.
    """
    """
    Ninye i prisno i vo vyeki vyekov
    """
    db=shelve.open(base_filename + ".db")
    for object in array_of_class_instances:
        db[object.name]=object
    db.close()



def import_db(base_filename):
    """
    Imports a database. 
    The function checks for the existence of the database. It returns "False" 
        if the file doesn't exist. Otherwise, it will return an array with
        class instances.
    """

    if os.path.isfile(base_filename + ".db") == True:
        db=shelve.open(base_filename + ".db")
        array_of_class_instances=[]
        for key in db:
            array_of_class_instances.append(db[key])
        db.close()
        return array_of_class_instances
    else:
        print "classtools.import_db: The file doesn't exist!"
        return False

####################
# HELPER FUNCTIONS #
####################

def format_print(var):
    """
    format_print is a helper function for the gatherAttrs function. 
    There are a few situations:
        1) var is not a list or an ndarray, it will print the value. This include tuples
        2) var is an ndarray, the shape will be printed
        3) the var is a list, it will do recursion to print either 1 or 2
    Examples:
        42          => 42
        "car"       => "car"
        [1,2]       => [1,2]
        ndarray     => shape
        [1,ndarray] => [1, shape]
    """
# list
    if type(var) == list:
        typ=range(len(var))       
        for i in range(0, len(var)):
            typ[i]=(format_print(var[i]))
        return typ
# ndarray
    elif type(var) == np.ndarray:
        a=np.shape(var)
        if len(a) == 1: return (str(a[0]) + " x 1")
        else: return str(a[0]) + " x " + str(a[1])
# time
    elif type(var) == time.struct_time: 
        var = time.strftime("%a, %d %b %Y %H:%M:%S", var)
        return var
# the rest
    else:
        return var

def format_key(key):
    """
    Strips keys from _. These keys are semi-protected and should be run through the getter and setter methods.
    """
    if key[0] == "_":
        key = key[1:]
    else:
        pass
    
    return key
    
    

##############
# CLASSTOOLS #
##############

class ClassTools(object):
    """
    A way to print the whole class in one go.
    It prints the key and the value.
    """
    def gatherAttrs(self):
        attrs=[]
        for key in sorted(self.__dict__):
            attrs.append("\t%20s  =  %s\n" % (format_key(key), format_print(getattr(self, key))))
        return " ".join(attrs)

    def __str__(self):
        return "[%s:\n %s]" % (self.__class__.__name__, self.gatherAttrs())
        



###########
# TESTING #
###########

if __name__=="__main__":
    testing="extract_shape"
    if testing == "extract_shape":
        
        
        y=range(2)
          
        y[0]=ClassTools()
        y[0].name="fiets"
        y[0].test = "check2"
        y[0].time = time.localtime()
        y[0].tup = (1, 2, 3)
        
        y[1]=ClassTools()
        y[1].name="auto"
        y[1].test = "check3"
        y[1].time = time.localtime()
        y[1].tup = (1, 2)        
        
        make_db(y, "testdb")
        
        x=range(2)
        
        
        x[0]=0
        x[1]=0
        
        x=import_db("testdb")
        
        print x, x[0], x[1]
        
        x.append(ClassTools())
        x[2].name="boot"
        
        print x[2]
        
        make_db(x, "testdb")
        
        z=range(3)
        
        z=import_db("testdb")
        
        print z, z[0], z[1], z[2]

#        print x, x[0], x[1], x[2]        
#        make_db(x, "testdba")
        
#        z=import_db("testdba")





