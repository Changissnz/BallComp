"""
delete this file after project completion
"""

from test_samples import *


def test__CircleScanner__estimate_2int():
    cs = sample_circle_scanner_1(sample_circle_pair_1())
    a = cs.estimate_2int(0,1)
    a2 = cs.estimate_2disjunction(0,1)
    print("2-int ",a)
    print("2-disj ",a2)
    print("est. total ",a + a2)
    print("act. total ", circle_area(cs.cprs[0,2]) + circle_area(cs.cprs[1,2]))
    return

def test__CircleScanner__estimate_2int__2():
    cs = sample_circle_scanner_1(sample_circle_pair_2(),0.01)
    cs.qf = is_equal

    a = cs.estimate_2int(0,1)
    a2 = cs.scan(1,[0,1])

    print("2-disj predicted ",a)
    print("2-disj actual ",a2)

    ###
    """
    a2 = cs.estimate_2disjunction(0,1)
    print("2-int ",a)
    print("2-disj ",a2)
    print("est. total ",a + a2)
    print("act. total ", circle_area(cs.cprs[0,2]) + circle_area(cs.cprs[1,2]))
    """
    ###
    return

def test__CircleScanner__estimate_2int__3():
    cs = sample_circle_scanner_1(sample_circle_pair_3(),0.01)
    cs.qf = is_equal

    a = cs.estimate_2int(0,1)
    a2 = cs.scan(1,[0,1])

    print("2-disj predicted ",a)
    print("2-disj actual ",a2)

def test__CircleScanner__estimate_2int__4():
    cs = sample_circle_scanner_1(sample_circle_pair_4(),0.01)
    cs.qf = is_equal

    a = cs.estimate_2int(0,1)
    a2 = cs.scan(1,[0,1])

    print("2-disj predicted ",a)
    print("2-disj actual ",a2)

def test__CircleScanner__estimate_2int__5():
    cs = sample_circle_scanner_1(sample_circle_pair_5(),0.01)
    cs.qf = is_equal

    a = cs.estimate_2int(0,1)
    a2 = cs.scan(1,[0,1])

    print("2-disj predicted ",a)
    print("2-disj actual ",a2)

def test__CircleScanner__estimate_2int__6():
    cs = sample_circle_scanner_1(sample_circle_pair_6(),0.01)
    cs.qf = is_equal

    a = cs.estimate_2int(0,1)
    a2 = cs.scan(1,[0,1])

    print("2-disj predicted ",a)
    print("2-disj actual ",a2)

def test__CircleScanner__estimate_2int__7():
    cs = sample_circle_scanner_1(sample_circle_pair_7(),0.01)
    cs.qf = is_equal

    a = cs.estimate_2int(0,1)
    a2 = cs.scan(1,[0,1])

    print("2-disj predicted ",a)
    print("2-disj actual ",a2)

def test__CircleScanner__estimate_2int__8():
    cs = sample_circle_scanner_1(sample_circle_pair_8(),0.01)
    cs.qf = is_equal

    a = cs.estimate_2int(0,1)
    a2 = cs.scan(1,[0,1])

    print("2-disj predicted ",a)
    print("2-disj actual ",a2)

def test__CircleScanner__estimate_2int__9():
    cs = sample_circle_scanner_1(sample_circle_pair_9(),0.01)
    cs.qf = is_equal

    a = cs.estimate_2int(0,1)
    a2 = cs.scan(1,[0,1])

    print("2-disj predicted ",a)
    print("2-disj actual ",a2)

def test__CircleScanner__estimate_2int__10():
    cs = sample_circle_scanner_1(sample_circle_pair_9(),0.01)
    cs.qf = is_equal

    a = cs.estimate_2int(0,1)
    a2 = cs.scan(1,[0,1])

    print("2-disj predicted ",a)
    print("2-disj actual ",a2)

####------------------------------------------------------------------------------
