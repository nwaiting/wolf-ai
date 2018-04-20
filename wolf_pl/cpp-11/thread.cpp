#include <thread>
#include <iostream>
#include <chrono>

/*
chrono：时间库 源于boost 现在已是c++标准
*/

using namespace std;

void thread_func(void)
{
    cout << "start thread func" << endl;
}

void thread_func1(int n)
{
    for (int i = 0; i < 2; i++)
    {
        cout << "pass value, executing thread " << n << " thread id "<< this_thread::get_id() << endl;
        this_thread::sleep_for(chrono::milliseconds(10));
    }
}

void thread_func2(int& n)
{
    for (int i = 0; i < 2; i++)
    {
        cout << "pass reference, executing thread " << n << " thread id "<< this_thread::get_id() << endl;
        n++;
        this_thread::sleep_for(chrono::milliseconds(5));
    }
}

void thread_func3(int n)
{
    this_thread::sleep_for(chrono::seconds(2));
    cout << "this thread " << this_thread::get_id()
        << " sleep " << n << endl;
}

int main()
{
    /*
    //c++11线程使用
    thread t1(thread_func);
    t1.join();
    */

    /*
    //线程不同的构造函数
    int a = 10086;
    thread t1;
    thread t2(thread_func1, a);
    //引用
    thread t3(thread_func2, ref(a));
    //move赋值
    thread t4(move(t3));
    //硬件并发特性 CPU核数
    cout << "concurrency " << t4.hardware_concurrency() endl;
    //t1.join();
    t2.join();
    //t3.join();
    t4.join();
    */

    //
    thread threads[3];
    for (int i = 1; i <= 3; i++)
    {
        thread t(thread_func3, i);
        //会报错因为赋值的是一个引用
        //threads[i - 1] = t;
        threads[i - 1] = move(t);
    }

    cout << "finish 3 thread, wait for join" << endl;

    /*
    //会报错 原因就是copy操作不可用，相当于是delete操作，所以报错
    for (auto t : threads)
    {
        t.join();
    }
    */

    for (auto &t : threads)
    {
        t.join();
    }
    cout << "threads finished" << endl;
    cin.get();
    return 0;
}
