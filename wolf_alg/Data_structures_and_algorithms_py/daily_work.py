#coding=utf-8

import sched, time

def edit_distance(ts1, ts2):
    l1 = len(ts1)
    l2 = len(ts2)
    arr = [[0 for i in xrange(l2+1)] for j in xrange(l1+1)]
    for i in xrange(l1+1):
        arr[i][0] = i
    for j in xrange(l2+1):
        arr[0][j] = j
    print arr
    for i in xrange(1,l1):
        for j in xrange(1,l2):
            if ts1[i-1] == ts2[j-1]:
                arr[i][j] = arr[i-1][j-1]
            else:
                arr[i][j] = min(arr[i-1][j-1]+1, arr[i-1][j]+1, arr[i][j-1]+1)
            print arr
    return arr[i][j]

def test_print():
    print "time ",time.time()

def test_timer(inc):
    print "after enter ",time.time() 
    schedule.enter(inc,0,test_timer,(inc,))
    print "end enter ",time.time()
    test_print()

def test_schedule():
    schedule.enter(0,0,test_timer,(10,))
    schedule.run()

if __name__ == '__main__':
    s1 = 'hel'
    s2 = 'hell0'
    print edit_distance(s1, s2)


    schedule = sched.scheduler ( time.time, time.sleep )
    test_schedule()
