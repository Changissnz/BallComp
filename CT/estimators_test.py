from estimators import *

############################################# tests involving linesets

"""
tests for correct horizontal and vertical coexisting linesets
"""
def test__coexistence_between_linesets():

    # horizontal test
    ls1 = np.array([[[-2,10],[4,10]], [[6,10], [7.5,10]], [[11,10],[14,10]]])
    ls2 = np.array([[[2,12],[5,12]], [[5.1,12], [17.5,12]], [[19.0,12],[24,12]]])

    coext = coexistence_between_linesets(ls1,ls2,0)
    sol = np.array([[2.,4.],[6.,7.5],[11.,14.]])
    assert np.all(coext == sol), "failed horizontal test"

    # vertical test
    ls3 = []
    for x in ls1:
        x_ = np.array([x[:,1],x[:,0]]).T
        ls3.append(x_)
    ls3 = np.array(ls3)

    ls4 = []
    for x in ls2:
        x_ = np.array([x[:,1],x[:,0]]).T
        ls4.append(x_)
    ls4 = np.array(ls4)
    coext = coexistence_between_linesets(ls3,ls4,1)
    assert np.all(coext == sol), "failed vertical test"
    return

def test__coexistence_between_linesets__case2():

    ls1 = np.array([[[1.,2.],[4.9,2.]],[[5.1,2.],[13.5,2.]]])
    ls2 = np.array([[[1.,2.1],[4.1,2.1]],[[5.9,2.1],[13.5,2.1]]])
    coext = coexistence_between_linesets(ls1,ls2,0)

    print("COEXT")
    print(coext)


############################################# tests involving circles

def test__area_estimation_of_circle_segment_by_ratio():

    c1 = np.array([5.0,6.0,4.0])

    a = area_estimation_of_circle_segment_by_ratio(c1,0.5)

    print("est ",a)
    print("circle area ",circle_area(c1[2]))
    return -1

def test__angle_between_two_points():
    p1 = np.array((0,0.0))

    p2 = np.array((0,3.0))
    p3 = np.array((0,-3.0))
    p4 = np.array((3.0,0.0))
    p5 = np.array((-3.0,0.0))

    assert angle_between_two_points(p1,p2) == 90.0
    assert angle_between_two_points(p1,p3) == -90.0
    assert angle_between_two_points(p1,p4) == 0.0
    assert angle_between_two_points(p1,p5) == 0.0
    return

def test__angle_between_two_points_clockwise():
    p1 = np.array((0,0.0))

    p2 = np.array((0,3.0))
    p3 = np.array((0,-3.0))
    p4 = np.array((3.0,0.0))
    p5 = np.array((-3.0,0.0))

    p6 = np.array((1.5,1.5))
    p7 = np.array((-1.5,1.5))
    p8 = np.array((-1.5,-1.5))
    p9 = np.array((1.5,-1.5))

    assert angle_between_two_points_clockwise(p1,p2) == 90.0
    assert angle_between_two_points_clockwise(p1,p3) == 270.0
    assert angle_between_two_points_clockwise(p1,p4) == 0.0
    assert angle_between_two_points_clockwise(p1,p5) == 180.0

    assert abs(angle_between_two_points_clockwise(p1,p6) - 45.0) < 10 ** -6
    assert angle_between_two_points_clockwise(p1,p7) == 135.0
    assert angle_between_two_points_clockwise(p1,p8) == 225.0
    assert angle_between_two_points_clockwise(p1,p9) == 315.0
    return

def test__generate_circle_for_circle_by_area_ratio_and_ratio_of_intersection():
    c1 = np.array([0.0,0.0,3.0])

    # varying intersection ratio w/ area ratio = 3.0
    ars = [1/6,1/4,1/3,1/2,2/3,5/6,1]

    for a in ars:
        c = generate_circle_for_circle_by_area_ratio_and_ratio_of_intersection(c1,3,a,180.0) # 180.0
        r1,r2 = ratio_of_intersection_between_two_circles(c1,c)
        assert abs(r1 - a) < 10 ** -5, "incorrect generation for ratio {}, got {}".format(a,(r1,r2))
