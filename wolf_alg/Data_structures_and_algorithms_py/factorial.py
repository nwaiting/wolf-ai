#coding=utf-8

def factorial(n):
    if n <= 0:
        return 1
    else:
        v = factorial(n - 1)
        return v * n

if __name__ == '__main__':
    print factorial(6)
