#coding=utf-8

"""
    dp：
        [[1,3,1],
          [1,5,1],
          [4,2,1]]
"""



def find_minpath(ll):
    sum_min = []
    res = []
    for i in range(len(ll)):
        sum_min.append([0 for i in range(len(ll[i]))])

    sum_min[0][0] = ll[0][0]
    for i in range(1, len(ll)):
        sum_min[i][0] = sum_min[i-1][0] + ll[i][0]
    for j in range(1, len(ll[0])):
        sum_min[0][j] = sum_min[0][j-1] + ll[0][j]
    for i in range(1, len(ll)):
        for j in range(1, len(ll[0])):
            if sum_min[i-1][j] < sum_min[i][j-1]:
                sum_min[i][j] = sum_min[i-1][j] + ll[i][j]
            else:
                sum_min[i][j] = sum_min[i][j-1] + ll[i][j]
    return sum_min

def show_path(sum_vals, data_vals):
    res = [data_vals[len(data_vals)-1][len(data_vals[0])-1]]
    i = len(sum_vals)-1
    j = len(data_vals[0])-1
    while i >= 0 and j >= 0:
        if sum_vals[i-1][j] < sum_vals[i][j-1] and i >= 1:
            res.append(data_vals[i-1][j])
            i -= 1
        elif j >= 1:
            res.append(data_vals[i][j-1])
            j -= 1
        else:
            break
    print(res[::-1])
    return res


if __name__ == '__main__':
    data = [[1,3,1,3],
            [1,5,1,4],
            [4,2,1,5],
            [3,5,2,8]]
    res = find_minpath(data)
    min_val = res[len(data)-1][len(data[0])-1]
    print(min_val)
    show_path(res, data)
