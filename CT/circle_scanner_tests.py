from test_samples import *

def test__CircleScanner_stat_of_coordinate__sample_1():
    cs = sample_circle_scanner_1(sample_circle_pair_1())
    cs.set_scan_region()
    stat1 = cs.stat_of_coordinate(cs.cprs[0][:2])
    stat2 = cs.stat_of_coordinate(cs.cprs[1][:2])
    stat3 = cs.stat_of_coordinate(np.array([8.5,6]))
    stat4 = cs.stat_of_coordinate(cs.scanRegion[0] + 0.5)
    assert stat1 == [0], "incorrect stat case 1"
    assert stat2 == [1], "incorrect stat case 2"
    assert stat3 == [0,1], "incorrect stat case 3"
    assert stat4 == [], "incorrect stat case 4"
    return

def test__CircleScanner__scan_collect_lineset_():
    cs = sample_circle_scanner_1(sample_circle_pair_1())
    cs.qf = is_equal

    # case: scan right starting at left-edge center
    dir = "right"
    a = np.array([1,6.0])
    ls = cs.scan_collect_lineset_(a,"right", [0,1])
    sol = np.array([[[8.5,6.],\
        [8.999,6.]]])

    for (ls1,sol1) in zip(ls,sol):
        assert np.all(np.round(ls1,5) == np.round(sol1,5)),"failed case 1\ngot\t{}\nwant\t{}".format(ls1,sol1)

    cs.qf = is_in_d
    ls = cs.scan_collect_lineset_(a,"right", [0,1])
    sol2 = np.array([[[1.,6.],\
        [8.499,6.]],\
        [[9.,6.],\
        [13.5,6.]]])
    for (ls1,sol1) in zip(ls,sol2):
        assert np.all(np.round(ls1,5) == np.round(sol1,5)),"failed case 2\ngot\t{}\nwant\t{}".format(ls1,sol1)

    # case: scan right starting from left-edge bottom
    cs.qf = is_equal
    a = np.copy(cs.scanRegion[0])
    ls = cs.scan_collect_lineset_(a,"right", [])
    sol3 = np.array([[[1.,2.],\
        [4.999,2.]],\
        [[5.001,2.],\
        [13.5,2.]]])
    for (ls1,sol1) in zip(ls,sol3):
        assert np.all(np.round(ls1,5) == np.round(sol1,5)),"failed case 3\ngot\t{}\nwant\t{}".format(ls1,sol1)

    # case: scan up starting from left-edge bottom
    a = np.copy(cs.scanRegion[0])
    ls = cs.scan_collect_lineset_(a,"up", 0)
    sol4 = np.array([[[ 1.,2.],\
                [1.,5.999]],\
                [[1.,6.001],\
                [1.,10.]]])
    for (ls1,sol1) in zip(ls,sol4):
        assert np.all(np.round(ls1,5) == np.round(sol1,5)),"failed case 3\ngot\t{}\nwant\t{}".format(ls1,sol1)
    return

def test__CircleScanner___area_between_two_linesets():
    cs = sample_circle_scanner_1(sample_circle_pair_1())
    cs.qf = is_equal

    a = np.array([1,6.0])
    ls = cs.scan_collect_lineset_(a,"right",[0,1])

    a2 = np.array([1,6.1])
    ls2 = cs.scan_collect_lineset_(a2,"right",[0,1])

    ls3 = coexistence_between_linesets(ls,ls2,0)
    a = area_of_coexisting_lineset(ls3, 0.1)
    assert round(a,5) == 0.0495, "incorrect area b/t 2 linesets"
    return

"""
varies intersection ratio
"""
def test__CircleScanner__estimate_2int__trials(c1radius = 3.0, areaRatio = 1.0):

    # construct the circles
    cs = [np.array([0.0,0.0,c1radius])]

            # varying intersection ratio w/ area ratio = 1.0
    ars = [1/6,1/4,1/3,1/2,2/3,5/6,1]

    for a in ars:
        c = generate_circle_for_circle_by_area_ratio_and_ratio_of_intersection(cs[0],areaRatio,a,180.0)
        cs.append(c)

    cs = np.array(cs)
    cs = sample_circle_scanner_1(cs,0.01)
    cs.qf = is_equal_subset

    ###
    results = []
    for i in range(1,cs.cprs.shape[0]):
        a2 = cs.scan_mp(1,[0,i])
        print("area is ",a2)
        a3 = cs.estimate_2int(0,i)
        print("est is ",a3)
        print("----------------")

        x = [areaRatio, ars[i - 1],a2,a3,a2/a3]
        results.append(x)

    results = np.array(results)
    return results

def test__CircleScanner__estimate_2int__trials2(c1radius = 3.0, areaRatio = 1.0):

    deg = [0.0,-30.0,-45.0,30.0,45.0]
    roi = 0.5
    cs = [np.array([0.0,0.0,c1radius])]

    for degree in deg:
        c = generate_circle_for_circle_by_area_ratio_and_ratio_of_intersection(cs[0],areaRatio,roi,degree)
        cs.append(c)

    cs = np.array(cs)
    cs = sample_circle_scanner_1(cs,0.01)
    cs.qf = is_equal_subset

    for i in range(1,cs.cprs.shape[0]):
        a2 = cs.scan_mp(1,[0,i])
        print("area is ",a2)
        a3 = cs.estimate_2int(0,i)
        print("est is ",a3)


def test__CircleScanner__estimate_3int__trials():
    startPoint = (0,0)
    startRadius = 3.0

    # case 1,2,3
    ##radiusRatios = [1.0,1.0]
    # case 4
    ##radiusRatios = [1.0,2/3]
    # case 5
    ##radiusRatios = [1.0,0.5]
    ##intersectionRatios = [0.5,0.5]

    # case 1
    ##degrees = [0.0,315.0]
    # case 2
    ##degrees = [135.0,45.0]
    # case 3,4,5
    ##degrees = [60.0,120.0]

    # case 6
    radiusRatios = [0.5,1.0]
    degrees = [-180.0,45.0]
    intersectionRatios = [1.0,1/6]

    cs = generate_circles(startPoint, startRadius, radiusRatios, intersectionRatios,degrees)
    cs = sample_circle_scanner_1(cs,0.01)

    r1,r2 = ratio_of_intersection_between_two_circles(cs.cprs[1],cs.cprs[2])

    print("ratio of intersection ",r1,r2)
    return

    # scan for 2-way intersections
    cs.qf = is_equal_subset
    a2 = cs.scan_mp(1,[0,1])
    print("(0,1) area is ",a2)
    a2 = cs.scan_mp(1,[0,2])
    print("(0,2) area is ",a2)
    a2 = cs.scan_mp(1,[1,2])
    print("(1,2) area is ",a2)

    cs.qf = is_equal
    a2 = cs.scan_mp(1,[0,1,2])
    print("(0,1,2) area is ",a2)
    return -1
