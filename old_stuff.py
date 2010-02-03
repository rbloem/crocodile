
        
    


    else:
    
        a="fiets"
        b=["auto",1,2]
        c=np.arange(5)
        d=[1,b,c]
        e=np.arange(20).reshape(4,5)
        f=time.localtime()
        
        print find_types(a)
        print find_types(b)
        print find_types(c)
        print find_types(d)
        print find_types(e)
        print find_types(f)
    
        class TopTest(AttrDisplay):
            count=0
            def __init__(self):
                self.attr1=TopTest.count
                self.attr2=TopTest.count+1
                TopTest.count += 2
        
        class SubTest(TopTest):
            pass
    
        X,Y=TopTest(), SubTest()
        print X
        print Y


#############################
# OLD CRAP, will be deleted #
#############################

def extract_shape(temp):
    """
    extract_shape is a helper function for the gatherAttrs function.        
    """
    tmp=[]
    for i in range(0, len(temp)):
        if type(temp[i]) == np.ndarray:
            a = np.shape(temp[i])
            if len(a) == 1: tmp.append(str(a[0]) + "x1")
            else: tmp.append(str(a[0]) + "x" + str(a[1]))
        else:
            tmp.append(temp[i])
    return tmp 


def functionx(var):  
    if type(var) == int:
        print var
    else:   #list or ndarray
        a = np.shape(var)
        if len(a) == 1: #list
            print var
        else:   #ndarray
            print "fiets" #(str(a[0]) + "x" + str(a[1]))
            
def find_types(var):
    typ=[]
    if type(var) == int or type(var) == str:
        typ=var
    elif type(var) == list:
        typ=range(len(var))       
        for i in range(0, len(var)):
            typ[i]=(find_types(var[i]))
    elif type(var) == np.ndarray:
        a=np.shape(var)
        if len(a) == 1: typ = (str(a[0]) + " x 1")
        else: typ = str(a[0]) + " x " + str(a[1])
    return typ   

class ClassToolsBU:
    """
    A way to print the whole class in one go.
    It prints the key and the value.
    For a few special cases (d, s, w and t array), the helper function extract_shape 
        will be called. In that case, the size of the array will be shown.
    The output looks like:
        key_int = value
        key_list = [value1, value2, ...]
        key_special = [value1, (shape), value2]    #for the case: [1, [2, 3], 4]
    
    """
    def gatherAttrs(self):
        attrs=[]
        for key in sorted(self.__dict__):

            if key == "d" or key == "s" or key == "w" or key == "t":
                temp = getattr(self, key)
                tmp = extract_shape(temp)
                attrs.append("\t%20s\t  =\t %s\n" % (key, tmp))                      
            else:
                attrs.append("\t%20s\t  =\t %s\n" % (key, getattr(self, key)))
        return " ".join(attrs)
    def __str__(self):
        return "[%s:\n %s]" % (self.__class__.__name__, self.gatherAttrs())