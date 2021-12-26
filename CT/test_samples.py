# manual construction here
from circle_scanner import *

def sample_circle_1():
    return np.array([5.0,6.0,4.0])

#
def sample_circle_pair_1():
    cp = sample_circle_1()
    distance = 6
    deg = 0.0
    r2 = 2.5
    cp2 = generate_circle_for_circle(cp,distance,deg,r2)
    return np.array([cp,cp2])

def sample_circle_pair_2():
    cp = sample_circle_1()
    distance = 6
    deg = 90.0
    r2 = 4.0
    cp2 = generate_circle_for_circle(cp,distance,deg,r2)
    return np.array([cp,cp2])

def sample_circle_pair_3():
    cp = sample_circle_1()
    distance = 8
    deg = 90.0
    r2 = 8.0
    cp2 = generate_circle_for_circle(cp,distance,deg,r2)
    return np.array([cp,cp2])

        ### below methods used for obtaining intersection

"""
intersection is i_l = 1.0 => 1/6
"""
def sample_circle_pair_4():
    c1 = np.array([0,0,3.0])
    c2 = np.array([11.0,0,9.0])
    return np.array([c1,c2])

def sample_circle_pair_5():
    c1 = np.array([0,0,3.0])
    c2 = np.array([5.0,0,3.0])
    return np.array([c1,c2])

def sample_circle_pair_6():
    c1 = np.array([0,0,3.0])
    c2 = np.array([4.5,0,3.0])
    return np.array([c1,c2])

def sample_circle_pair_7():
    c1 = np.array([0,0,3.0])
    c2 = np.array([13.5,0,12.0])
    return np.array([c1,c2])

def sample_circle_pair_8():
    c1 = np.array([0,0,3.0])
    c2 = np.array([12.0,0,12.0])
    return np.array([c1,c2])

def sample_circle_pair_9():
    c1 = np.array([0,0,3.0])
    c2 = np.array([9.0,0,9.0])
    return np.array([c1,c2])

#####---------------------------------------------------------------------------

"""
"""
def sample_circle_scanner_1(circlePair,increment = 10 ** -3):
    cs = CircleScanner(circlePair,increment)
    cs.set_scan_region()
    return cs
