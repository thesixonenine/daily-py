import time


def is_update(t: time.struct_time) -> bool:
    return compare_struct_time(t, time.localtime(time.time()))


def compare_struct_time(t1: time.struct_time, t2: time.struct_time) -> bool:
    year = t1.tm_year == t2.tm_year
    mon = t1.tm_mon == t2.tm_mon
    mday = t1.tm_mday == t2.tm_mday
    return year and mon and mday
