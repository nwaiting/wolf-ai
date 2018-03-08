#coding=utf-8

def test_list():
    a = [2,4,6,8,10]
    print a[0:2] #[begin:end]
    print a[:2] #[0:end]
    print a[1::2] #[begin:end but step is 2]
    print a[-2:-1] #[-2:end](but end > -2)
    print a[-1] #[index]
    print a[::-1] #同reverse

    b = a[:]
    b.reverse()
    print b

    print a

def get_age(age):
    if age < 20:
        return 'small'

def sort_defi():
    kel = []
    kel_list = sorted(kel,key=get_age)

    class Student(object):
        def __init__(self, name=None, res=None, age=None):
            self.name = name
            self.res = res
            self.age =age
    student_some = [Student('kel','B',35),Student('jun','C',30)]
    print sorted(student_some,key= lambda x :x.age)

    def reversed_cmp(x, y):
        if x > y:
            return 1
        if x < y:
            return -1
        return 0
    print sorted([36, 5, 12, 9, 21], reversed_cmp)

if __name__ == '__main__':
    #test_list()
    sort_defi()
