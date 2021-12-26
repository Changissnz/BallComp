# estimator functions are used primarily to calculate intersection
import math
import numpy as np

euclidean_point_distance = lambda p1, p2: np.sqrt(np.sum((p1 - p2)**2))
circle_area = lambda r: math.pi * r ** 2

FUZZY_TABLE = {1.0: 0.46792,\
            5/6: 0.52544,\
            2/3: 0.61026,\
            1/2: 0.72842,\
            1/3: 0.88860,\
            1/4: 0.96300,\
            1/6:1.0}

"""
description:
- outputs an endpoint given `point`; `endpoint` is distance `length`
  from `point` and at `angle`
"""
def hypotenuse_from_point(point, length, angle):

    # get the x-delta and y-delta
    q = math.sin(math.radians(angle))
    opp = q * length

    q = math.cos(math.radians(angle))
    adj = q * length
    return np.array([point[0] + adj, point[1] + opp])

def angle_between_two_points(startX, endX):
    if np.all(np.round(startX,5) == np.round(endX,5)):
        return 0

    l = euclidean_point_distance(startX, endX)
    opposite = endX[1] - startX[1]

    q = opposite / float(l)
    return math.degrees(np.arcsin(q))

def angle_between_two_points_clockwise(startX, endX):
    angle = angle_between_two_points(startX, endX)

    # case: horizontal
    if angle == 0:
        if startX[0] <= endX[0]:
            return angle
        return 180

    # case: forward
    if startX[0] < endX[0]:
        if angle > 0:
            return angle
        else:
            return angle % 360
    else:
        return 180 - angle
    return angle

"""
ar := float,area ratio
ri := float, intersection ratio
degree := float, d in [0,360]
"""
def generate_circle_for_circle_by_area_ratio_and_ratio_of_intersection(c1,ar,ri,degree):
    # radius of the new circle
    r2 = c1[2] * ar
    # distance
    d = (c1[2] + r2) - (ri * c1[2] * 2)

    # new point
    h = hypotenuse_from_point(c1[:2],d,degree)
    return np.append(h,r2)

################################ start: methods for estimating intersection between two circles

"""
calculates a ratio for each circle that represents the ratio of its diameter
that lies in the intersection space.

A circle that completely lies in another circle will have a ratio of 1.0 and
the other 0.0.

return:
- float::(ratio of diameter of c1 in c2)
- float::(ratio of diameter of c2 in c1)
"""
def ratio_of_intersection_between_two_circles(c1,c2):
    l = [c1[:2],c2[:2]]
    ed = euclidean_point_distance(c1[:2],c2[:2])

    # case: c1 and c2 do not intersect
    if ed >= c1[2] + c2[2]: return None,None

    # case: c2 in c1
    if ed + c2[2] <= c1[2]:
        return 0.0,1.0

    # case: c1 in c2
    if ed + c1[2] <= c2[2]:
        return 1.0,0.0

    # extend the line to cover both circles' bounds
    deg = angle_between_two_points_clockwise(c1[:2],c2[:2])
    deg2 = (deg + 180) % 360

    # get intersection points on line l
    intPFromC1 = hypotenuse_from_point(c1[:2],c1[2],deg)
    intPFromC2 = hypotenuse_from_point(c2[:2],c2[2],deg2)

    # calculate the intersection length / diameter ratios
    dd1 = euclidean_point_distance(intPFromC1,intPFromC2) / (c1[2] * 2)
    dd2 = euclidean_point_distance(intPFromC1,intPFromC2) / (c2[2] * 2)
    return dd1,dd2

"""
estimates the area of circle by a ratio `r`
"""
def area_estimation_of_circle_segment_by_ratio(c1,r):
        ##
    """
    base = 0.5
    base += (r * 0.5)
    return circle_area(c1[2]) * r * base
    """
        ##
    ba = (c1[2] * 2) **2
    a = ba - circle_area(c1[2])
    if r <= 0.5:
        return (ba * r) - (a / 2.0 * r / 0.5)
    else:
        return circle_area(c1[2]) * 0.5 + area_estimation_of_circle_segment_by_ratio(c1,r - 0.5)

def intersection_curvature_est(a):
    return a * 1.0 #0.40

def intersection_area_estimation_of_circle(c1,r):
    return intersection_curvature_est(area_estimation_of_circle_segment_by_ratio(c1,r))

"""
estimates the area of intersection b/t two circles
"""
def intersection_estimation_of_two_circles(c1,c2,r1,r2):
    ##print("RS ", r1,r2)
    if r1 == 1.0:
        return circle_area(c1[2])
    if r2 == 1.0:
        return circle_area(c2[2])
    ##

    def closest_reference_to_ratio(r):
        s = np.array([1/6,1/4,1/3,1/2,2/3,5/6,1])
        i = argmin(abs(s - r))
        return s[i]

    def minimal_area_ratio():
        return min([c1[2] / c2[2],c2[2] / c1[2]])

    def reference_intersection_ratio():
        if c1[2] > c2[2]:
            return r1
        return r2

    def closest_increment_to_ratio(r):
        s = [1/6,1/4,1/3,1/2,2/3,5/6,1]
        for s_ in s:
            if s_ >= r: return s_
        return 1.0

    rir = closest_increment_to_ratio(reference_intersection_ratio())
    cr = closest_increment_to_ratio(minimal_area_ratio())
    scalar = FUZZY_TABLE[cr] + (1- FUZZY_TABLE[cr]) * (rir)
    return min([area_estimation_of_circle_segment_by_ratio(c1,r1),\
            area_estimation_of_circle_segment_by_ratio(c2,r2)]) * scalar

################################ end: methods for estimating intersection between two circles


################################ start: methods for estimating intersection between 3+ circles

def generate_circles(startPoint, startRadius, radiusRatios, intersectionRatios,degrees):

    # declare the first
    c = np.array(startPoint)
    c = np.append(c,startRadius)
    cprs = [c]

    for r,i,d in zip(radiusRatios,intersectionRatios,degrees):
        c_ = generate_circle_for_circle_by_area_ratio_and_ratio_of_intersection(cprs[0],r,i,d)
        cprs.append(c_)
    return np.array(cprs)

################################ end: methods for estimating intersection between 3+ circles
