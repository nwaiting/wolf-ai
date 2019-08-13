#coding=utf-8

total_statistic = {}
def frequenttopk(d,k):
    total_statistic[d] = total_statistic.get(d,0)+1
    total_list = zip(total_statistic.keys(),total_statistic.values())
    new_list = sorted(total_list,key=lambda x:x[1],reverse=True)
    return new_list[:k]


if __name__ == '__main__':
    print(frequenttopk(1,3))
    print(frequenttopk(1,3))
    print(frequenttopk(1,3))
    print(frequenttopk(2,3))
    print(frequenttopk(2,3))
    print(frequenttopk(3,3))
    print(frequenttopk(4,3))
    print(frequenttopk(5,3))
    print(frequenttopk(6,3))
    print(frequenttopk(7,3))
    print(frequenttopk(7,3))
    print(frequenttopk(7,3))
    print(frequenttopk(8,3))
