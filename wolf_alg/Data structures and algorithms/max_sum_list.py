#coding=utf-8

"""
#求连续子数组中的最大和
"""

def max_sum(l):
    if len(l) <= 0:
        return None
    t = 0
    t_max = 0
    for i in l:
        if i + t <= 0:
            t = 0
        else:
            t += i
        t_max=t if t > t_max else t_max

    return t_max


if __name__ == '__main__':
    l = [3,1,-4,-5,2,-1,6,7,-10]
    print max_sum(l)
