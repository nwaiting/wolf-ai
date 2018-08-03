#coding=utf-8


def func1():
    """
        f = open("a.txt", "r")
        f.tell() #查看在文件中的当前位置
        f.seek(8, 0) #表示从文件开始处移动到文件的X字节处,第二个参数：0表示从文件开始处移动到文件的x处，1表示相对于当前位置移动到X字节处，2表示相对于文件末尾的位置
    """
    import os
    file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'a.txt')
    with open(file, 'r') as fd:
        fd.seek(1)
        print(fd.read())

def func2():
    """
    装饰器：
        def w1(func):
            def inner():
                print('inner')
                return func()
            return inner

        @w1
        def f1():
            print('f1')

    详解：
        没错，从表面上看解释器仅仅会解释这两句代码，因为函数在没有被调用之前其内部代码不会被执行。
        从表面上看解释器着实会执行这两句，但是 @w1 这一句代码里却有大文章，@函数名 是python的一种语法糖。
        如上例@w1内部会执行一下操作：
            执行w1函数，并将 @w1 下面的 函数 作为w1函数的参数，即：@w1 等价于 w1(f1)
            所以，内部就会去执行：
            def inner:
                #...
                return f1()   # func是参数，此时 func 等于 f1
            return inner     # 返回的 inner，inner代表的是函数，非执行函数
            其实就是将原来的 f1 函数塞进另外一个函数中
            将执行完的 w1 函数返回值赋值给@w1下面的函数的函数名
            w1函数的返回值是：
                def inner:
                    #...
                return 原来f1()  # 此处的 f1 表示原来的f1函数
            然后，将此返回值再重新赋值给 f1，即：
            新f1 = def inner:
            #...
            return 原来f1()
            所以，以后业务部门想要执行 f1 函数时，就会执行 新f1 函数，在 新f1 函数内部先执行验证，再执行原来的f1函数，然后将 原来f1 函数的返回值 返回给了业务调用者。
            如此一来， 即执行了验证的功能，又执行了原来f1函数的内容，并将原f1函数返回值 返回给业务调用着
    """
    """
    带参数的装饰器：
        #带多个参数
        def w1(func):
            def inner(*args,**kwargs):
                print('inner')
                return func(*args,**kwargs)
            return inner

        @w1
        def f1(arg1,arg2,arg3):
            print('f1')

    多个装饰器：
        def w1(func):
            def inner(*args,**kwargs):
                print('w1')
                return func(*args,**kwargs)
            return inner
        def w2(func):
            def inner(*args,**kwargs):
                print('w2')
                return func(*args,**kwargs)
            return inner

        @w2
        @w1
        def f1(arg1,arg2,arg3):
            print('f1')

        详解：
            def decorator_a(func):
                print 'Get in decorator_a'
                def inner_a(*args, **kwargs):
                    print 'Get in inner_a'
                    return func(*args, **kwargs)
                return inner_a

            def decorator_b(func):
                print 'Get in decorator_b'
                def inner_b(*args, **kwargs):
                    print 'Get in inner_b'
                    return func(*args, **kwargs)
                return inner_b

            @decorator_b
            @decorator_a
            def f(x):
                print 'Get in f'
                return x * 2
            当解释器执行下面这段代码时，实际上按照从下到上的顺序已经依次调用了 decorator_a 和 decorator_b ，这是会输出对应的 Get in decorator_a 和 Get in decorator_b 。
                这时候 f 已经相当于 decorator_b 里的 inner_b 。但因为 f 并没有被调用，所以 inner_b 并没有调用，依次类推 inner_b 内部的 inner_a 也没有调用，所以 Get in inner_a 和 Get in inner_b 也不会被输出
            然后最后一行当我们对 f 传入参数1进行调用时， inner_b 被调用了，它会先打印 Get in inner_b ，然后在 inner_b 内部调用了 inner_a
                所以会再打印 Get in inner_a, 然后再 inner_a 内部调用的原来的 f, 并且将结果作为最终的返回

            详解2：
                对于打印 print 'Get in inner_b'的解释：
                由此可见，是先运行的decorator_b，再运行的decorator_a，最后运行的被装饰函数f(x)
                这是因为decorator_a装饰器先return 了inner_a, 而decorator_b后面又把inner_a装饰了，最终整个暴露在外面的是inner_b，所以显示inner_b先运行，
                    最终的效果看起来就是装饰器decorator_b先运行。实际上代码在机器上跑的时候是先跑的decorator_a函数，再跑的decorator_b函数

                对于打印 print 'Get in inner_b' 的解释：
                那是因为在装饰器中的内层闭包函数被return了，而装饰器也相当于是函数调用，只是闭包的函数需要在最后被return出来，在调用被装饰函数f(x)时，
                    装饰其中return的inner_a和inner_b才会被执行。return一个函数的名字，这个函数是没有被执行的，函数名带有括号和参数才会去执行，
                    没有带括号的函数名只是一个对象而已，没有被执行。

    """
    def w1(func):
        print('w1 w1')
        def inner(*args,**kwargs):
            print('w1 inner')
            func(*args,**kwargs)
            print('w1 inner end')
        return inner

    def w2(func):
        print('w2 w2')
        def inner(*args,**kwargs):
            print('w2 inner')
            func(*args,**kwargs)
            print('w2 inner end')
        return inner

    @w2
    @w1
    def f1(arg1,arg2,arg3):
        print('f1')
    #f1(1,2,3)

    def decorator_a(func):
        print ('Get in decorator_a')
        def inner_a(*args, **kwargs):
            print ('Get in inner_a')
            print ("in a, args ", args)
            print ("in a, kwargs ", kwargs)
            kwargs.update({"params": "1234"})
            return func(*args, **kwargs)
        return inner_a

    def decorator_b(func):
        print ('Get in decorator_b')
        def inner_b(*args, **kwargs):
            print ('Get in inner_b')
            print ("in b, args ", args)
            print ("in b, kwargs ", kwargs)
            return func(*args, **kwargs)
        return inner_b

    @decorator_b
    @decorator_a
    def ffff(x, params):
        print ('Get in f')
        print ("params: ", params)
        return x
    ffff(*(1,))

if __name__ == '__main__':
    #func1()

    func2()
