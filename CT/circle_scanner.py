from estimators import *
from operator import le,ge
from functools import partial
from multiprocessing import Pool

"""
p := 2-vector, (x,y)
cpr := 3-vector, [0] is x-coord., [1] is y-coord., [2] is radius
"""
def is_point_in_circle(p, cpr):
    assert len(p.shape) == 1 and p.shape[0] == 2, "invalid arguments `p`"
    assert len(cpr.shape) == 1 and cpr.shape[0] == 3, "invalid arguments `cpr`"
    d = euclidean_point_distance(p,cpr[:2])
    return d <= cpr[2]

'''
n := int, number of circles
intersectionCenterPoint := 2-tuple, (x,y) coordinate that is the center of intersection area
distanceDegreePairs := matrix, n x 2,
                        [0] is distance from `intersectionCenterPoint`
                        [1] is degree of point w.r.t. `intersectionCenterPoint`
'''
def generate_n_intersecting_circles(n, intersectionCenterPoint, distanceDegreePairs):
    return -1

'''
generates a circle with reference to circle of center `cp` and radius `r`;
new circle will have radius `r2` and have a center point at degree `d` to `cp`
'''
def generate_circle_for_circle(cp,distance,deg,r2):
    assert len(cp) == 3, "invalid circle"
    cp2 = hypotenuse_from_point(cp, distance, deg)
    return np.hstack((cp2,r2))

"""
determines the coexistence between two linesets.
Each lineset is a list of 2 x 2 arrays. Each element
in a lineset will not co-exist with any other element
in the lineset, and the elements are ordered in ascending
order.

CAUTION: arguments are not checked for orderedness

arguments:
- ls1 := list(2 x 2 np.array)
- ls2 := list(2 x 2 np.array)
- axis := 0|1

return:
- list(2-vector)
"""
def coexistence_between_linesets(ls1,ls2,axis):
    assert axis in [0,1], "invalid axis"

    # collect the values
    def collect_values(ls):
        return np.array([l[:,axis] for l in ls])

    l1 = collect_values(ls1)
    l2 = collect_values(ls2)
    c1 = 0
    c2 = 0
    v = []
    while c1 < ls1.shape[0] and c2 < ls2.shape[0]:
        ## case: no co-existence
            # case: increment c1
        if l1[c1,1] <= l2[c2,0]:
            c1 += 1
            # case: increment c2
        elif l2[c2,1] <= l1[c1,0]:
            c2 += 1
        else:
            # case: start of l1 in l2
            if l1[c1,0] >= l2[c2,0] and l1[c1,0] <= l2[c2,1]:
                ve = min([l1[c1,1],l2[c2,1]])
                v_ = np.array([l1[c1,0],ve])

                c1 += 1
            # case: start of l2 in l1
            elif l2[c2,0] >= l1[c1,0] and l2[c2,0] <= l1[c1,1]:
                ve = min([l2[c2,1],l1[c1,1]])
                v_ = np.array([l2[c2,0],ve])
                c2 += 1
            else:
                raise ValueError("delete this!!")
            v.append(v_)
    return np.array(v)

"""
lineset := list(2-vector)
"""
def area_of_coexisting_lineset(lineset, increment):
    s = sum([l[1] - l[0] for l in lineset])
    return s * increment


# adjustment methods
"""
adjusts the center point of a circle by the arg. "distance","degree"

return:
- None
"""
def adjust_circle_in_list_by_distance_and_degree(cprs,index,distance,degree):
    cprs[index][:2]  = hypotenuse_from_point(cprs[index][:2], distance, degree)

    ###### TODO: this method is used for testing

def increment_one(s,axis,increment):
    s[axis] = s[axis] + increment ####
    return s

"""
use this for disjunction
"""
def is_in_d(x,r):
    c = 0
    for x_ in x:
        if (x_ in r):
            c += 1
        if c > 1:
            return False
    return True if c == 1 else False

"""
use this for intersection or [] case
"""
def is_equal(x,r):
    return x == r
"""
use this for subset intersection; r in x

EX:

True:
    r = [0,1]
    x = [0,1,2]

False:
    r = [0,1,2]
    x = [0]|[0,1]|[0,2]

"""
def is_equal_subset(x,r):
    for r_ in r:
        if r_ not in x: return False
    return True

'''
a scanner specialized for collecting the unique area of a list of
circles
'''
class CircleScanner:

    '''
    cprs := np.array, n x 3, [0] is x-coord., [1] is y-coord., [2] is radius
    '''
    def __init__(self,cprs,increment,qf = is_in_d):
        assert type(cprs) is np.ndarray and len(cprs.shape) == 2 and cprs.shape[1] == 3, "invalid cprs"
        assert type(increment) is float and increment <= 1.0 and increment >= 0.0, "increment must be in [0.0,1.0]"
        self.cprs = cprs
        self.increment = increment
        self.scanRegion = None
        self.targetStat = None
        self.qf = qf
        return


    def set_target_stat(self,ts):
        ts = sorted(set(ts))
        assert min(ts) >= 0 and max(ts) < self.cprs.shape[0]


    ## THIS NEEDS TO BE REVISED FOR n-way intersection
    """
    coordinate is unique if it exists in only 1 circle

    arguments:
    - coord := 2-vector

    return:
    - (0 if not in any circle)|(1 if in circle)|(2 if in > 1 circle)
    """
    def stat_of_coordinate(self,coord):
        ## TODO: delete, for 2-way
        """
        c = 0
        for i in range(self.cprs.shape[0]):
            if is_point_in_circle(coord, self.cprs[i]):
                c += 1
            if c > 1: return 2
        return c
        """
        ##----------------------------------------------
        c = []
        for i in range(self.cprs.shape[0]):
            if is_point_in_circle(coord, self.cprs[i]):
                c.append(i)
        return c


    def set_scan_region(self):

        # get x extremum
        xext = np.vstack((self.cprs[:,0] - self.cprs[:,2], self.cprs[:,0] + self.cprs[:,2])).T
        xMin = np.min(xext[:,0])
        xMax = np.max(xext[:,1])

        # get y extremum
        q = self.cprs[:,1]
        yext = np.vstack((self.cprs[:,1] - self.cprs[:,2], self.cprs[:,1] + self.cprs[:,2])).T
        yMin = np.min(yext[:,0])
        yMax = np.max(yext[:,1])
        self.scanRegion = np.array([(xMin,yMin),(xMax,yMax)])

    ####################### related methods

    def end_coord_from_coord_by_direction(self,coord,direction):
        c = np.copy(coord)
        if direction == "left":
            c[0] = self.scanRegion[0,0]
        elif direction == "right":
            c[0] = self.scanRegion[1,0]
        elif direction == "up":
            c[1] = self.scanRegion[1,1]
        elif direction == "down":
            c[1] = self.scanRegion[0,1]
        else:
            raise ValueError("direction is invalid")
        return c

    """
    conducts a scan from coordinate of "stat" in the specified `direction`
    until either the coordinate is either the boundary of `scanRegion` or the
    coordinate before the coordinate with a stat not equal to "stat".

    return:
    - np.array, 2 x 2, [0] is start coordinate, [1] is end coordinate.
                encloses a region of the same coordinate stat
    - 0|1|2, coordinate stat
    - bool, not the end of region boundary
    """
    def line_scan_from_coordinate_for_extreme(self,coord,direction):
        coordStat = self.stat_of_coordinate(coord)
        start = np.copy(coord)
        endCoord = self.end_coord_from_coord_by_direction(coord,direction)

        # two required conditions
        ##clause1 = lambda x: self.stat_of_coordinate(x) == coordStat
        def clause1(x):
            return self.stat_of_coordinate(x) == coordStat


        index = 0 if direction in {"left","right"} else 1
        op = le if direction in {"right","up"} else ge
        def clause2(x): return op(x[index],endCoord[index])

        increment = self.increment if direction in {"right","up"} else - self.increment
        def inc(x):
            x[index] = x[index] + increment
            return x

        notEnd = True
        while True:
            # check for out-of-bounds
            notEnd = clause2(coord)
            if not notEnd:
                coord = endCoord
                break

            # check for same coord. stat
            if not clause1(coord):
                coord[index] = coord[index] - increment
                break
            coord = inc(coord)
        return np.array([start,coord]),coordStat,notEnd

    def scan_collect_lineset_(self,startCoord, direction, uniqueCapture):
        assert direction in {'left', 'right', 'up', 'down'}, "direction {} invalid".format(direction)
        ##assert uniqueCapture in {0,1,2}, "unique capture {} invalid"

        sc = np.copy(startCoord)
        stat = True

        linesets = []
        index = 0 if direction in {"left","right"} else 1
        increment = self.increment if direction in {"right","up"} else - self.increment

        while stat:
            lineset, coordStat,stat = self.line_scan_from_coordinate_for_extreme(sc,direction)
            ##if coordStat == uniqueCapture:
            if self.qf(coordStat,uniqueCapture):
                linesets.append(lineset)
            sc[index] = sc[index] + increment
        return np.array(linesets)

    """
    # axis = 0
    each line will scan up

    # axis = 1
    each line will scan right
    """
    def scan(self,axis,coordStat):
        assert type(self.scanRegion) != type(None), "scan region must be set"
        assert axis in {0,1}, "invalid axis"

        # start with the first lineset
        sp = np.copy(self.scanRegion[0])

        scanDir = "up" if axis == 0 else "right"
        ls1 = self.scan_collect_lineset_(sp, scanDir, coordStat) ####

        # this is the boundary point that scan will stop on
        endDir = "up" if axis == 1 else "right"
        p2 = self.end_coord_from_coord_by_direction(sp,endDir)
        antiaxis = 0 if axis else 1
        area = 0.0

        while sp[axis] < p2[axis]:
            sp = increment_one(sp,axis,self.increment)
            i = self.increment

            # case: past boundary, round `sp` to boundary point
            if sp[axis] > p2[axis]:
                i = p2[axis] - (sp[axis] - i)
                sp[axis] = p2[axis]

            # add the area b/t the two linesets
            ls2 = self.scan_collect_lineset_(sp, scanDir, coordStat)

            ls = coexistence_between_linesets(ls1,ls2,antiaxis)
            area += area_of_coexisting_lineset(ls,i)

            # increment the first lineset
            ls1 = ls2

        return area

    def fetch_coordinate_pairs_for_scan(self,axis):
        s = np.copy(self.scanRegion[0])
        q = []
        stat = True
        while stat:
            r = increment_one(np.copy(s),axis,self.increment)

            if r[axis] >= self.scanRegion[1,axis]:
                r[axis] = self.scanRegion[1,axis]
                stat = not stat
            q.append([s,r])
            s = r
        return q

    def area_between_coord_pair(self,scanDir,coordStat,cs):
        ls1 = self.scan_collect_lineset_(cs[0], scanDir, coordStat)
        ls2 = self.scan_collect_lineset_(cs[1], scanDir, coordStat)
        ls = coexistence_between_linesets(ls1,ls2,0 if scanDir == "right" else 1)
        i = np.abs(np.sum(cs[0] - cs[1]))
        a = area_of_coexisting_lineset(ls,i)
        return a

    """
    multi-processing version of method<scan>
    """
    def scan_mp(self,axis,coordStat):
        scanDir = "up" if axis == 0 else "right"
        p = self.fetch_coordinate_pairs_for_scan(axis)

        """
        q = 0.0
        for p_ in p:
            q += self.area_between_coord_pair(scanDir, coordStat,p_)
        return q
        """

        f = partial(self.area_between_coord_pair, scanDir, coordStat)
        w = Pool(5)
        q = sum(w.map(f, p))
        w.close()
        w.join()
        return q

    ######## start: estimation methods
    '''
    estimates 2-intersection

    arguments:
    - i1 := int, index of circle in `cprs`
    - i2 := int, index of circle in `cprs`
    '''
    def estimate_2int(self,i1,i2):
        r1,r2 = ratio_of_intersection_between_two_circles(self.cprs[i1],self.cprs[i2])
        ##print("RATIOS ",r1,r2)
        ie = intersection_estimation_of_two_circles(self.cprs[i1],self.cprs[i2],r1,r2)
        return ie

    def estimate_2disjunction(self,i1,i2):
        s = self.estimate_2int(i1,i2)
        return circle_area(self.cprs[i1,2]) +\
            circle_area(self.cprs[i2,2]) - (2 * s)

    ######## end: estimation methods

###--------------------------------------------------------------------------------
