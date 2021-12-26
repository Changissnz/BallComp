"""
tests runtime for multi-processing version
"""
from test_samples import *
import time

def test__CircleScanner__scan():
    cs = sample_circle_scanner_1(sample_circle_pair_1(),0.005)

    a = cs.scan(1,[0,1])
    print("2-disj ",a)

    cs.qf = is_equal
    a2 = cs.scan(1,[0,1])
    print("2-int ", a2)

    int2 = cs.estimate_2int(0,1)
    print("2-int est: ",int2)

def test__CircleScanner__scan___runtime():
    cs = sample_circle_scanner_1(sample_circle_pair_1(),increment = 0.005)#5 * 10 ** -3)

    ts = time.time()
    a = cs.scan_mp(0,[0,1])
    rt = time.time() - ts
    print("area scan-mp: ",a)
    print("time elapsed: ", rt)

    ts = time.time()
    a2 = cs.scan(0,[0,1])
    rt2 = time.time() - ts
    print("area scan: ",a2)
    print("time elapsed: ", rt2)
    assert a < a2, "multi-processing version is to be faster"
