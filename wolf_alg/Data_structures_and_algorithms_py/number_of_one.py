#coding=utf-8

def number_of_one(n):
    if n <= 0:
        return 0
    count = 0
    while n:
        count += 1
        n = (n - 1) & n
    return count

if __name__ == '__main__':
    print number_of_one(7)
