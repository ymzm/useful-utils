# -*-coding:utf-8 -*-
import numpy as np
from scipy import interpolate
import pylab as pl

#%matplotlib inline
X=0
Y=1
SHOW=1

# TODO: 加入旋转 1到360度 可以简化

def cublic_insert(l, n):
    length = len(l[0])
    for i in range(1, length-1):
        if ((l[X][i]-l[X][i+1])*((l[X][i-1]-l[X][i])) > 0):
            continue;
            #return l;
        else:
            print ("not a monotone increasing function!\n")
            do_rotate()
            #return l;
            break;

    x0 = l[X][0]
    xn_1 = l[X][length-1]

    xnew=np.linspace(x0,xn_1,100)
    if SHOW>0:
        pl.plot(l[X],l[Y],"ro")
    f = interpolate.interp1d(l[X],l[Y],kind="cubic",fill_value="extrapolate")
    ynew = f(xnew)
    
    do_convert()

    if SHOW>0:
        pl.plot(xnew,ynew,label="cubic")
        pl.legend(loc="lower right")
        pl.show()
        if SHOW >1:
            print([xnew, ynew])
    return [xnew, ynew]

def do_rotate():
    pass

def do_convert():
    pass

test0_x = [1, 5, 9, 13, 15, 18]
test0_y = [1, 5, 1, 5, 7, -5]
test0_l = [test0_x, test0_y]
test1_x = [-1,-0.866,-0.7071, -0.5, 0,0.5, 0.7071, 0.866,1]
test1_y = [ 0, 0.5,  0.7071, 0.866,1, 0.866,0.7071, 0.5, 0]
test1_x.reverse()
test1_l = [test1_x, test1_y]

def test_cublic_insert():
    #cublic_insert(test0_l, 20)
    cublic_insert(test1_l, 20)

if __name__ == "__main__":
    test_cublic_insert()

