#coding=utf-8

def floyd(double_list, vertexs):
    for k in xrange(1, vertexs + 1):
        for i in xrange(1, vertexs + 1):
            for j in xrange(1, vertexs + 1):
                tmp = min_value if double_list[i][k] >= min_value or double_list[k][j] >= min_value else double_list[i][k] + double_list[k][j]
                if double_list[i][j] > tmp:
                    double_list[i][j] = tmp
    return double_list

if __name__ == '__main__':
    min_value = 999999999
    ll = [
    [min_value,min_value,min_value,min_value,min_value],
    [min_value,0,2,6,4],
    [min_value,min_value,0,3,min_value],
    [min_value,7,min_value,0,1],
    [min_value,5,min_value,12,0]]
    print floyd(ll, 4)
