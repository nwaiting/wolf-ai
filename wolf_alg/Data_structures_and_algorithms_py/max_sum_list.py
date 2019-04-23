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

def max_sum2(l):
    sum = 0
    b = -1
    for i in l:
        if b < 0:
            b = i
        else:
            b += i
        if sum < b:
            sum = b
    return sum

def rever_str(s):
    result = []
    pre_index = len(s)
    for i in range(len(s)-1,-1, -1):
        print("s[i]=",s[i])
        if s[i]==" ":
            result.append(s[i+1:pre_index])
            pre_index = i
    result.append(s[0:pre_index])
    return result


if __name__ == '__main__':
    """
    l = [3,1,-4,-5,2,-1,6,7,-10]
    print(max_sum(l))
    print(max_sum2(l))
    ll = [-3,-1,-4,-5,-2,-1,-6,-7,-10]
    print(max_sum2(ll))
    """
    print(rever_str("this is me"))
    s = "this is me"
    print(list(range(len(s)-1,-1, -1)))
