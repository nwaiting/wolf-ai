#include <iostream>
#include <thread>
#include <mutex>
#include <chrono>
#include <future>
using namespace std;

/*
mutex类型
    std::mutex mutex类型
    std::recursive_mutex 递归mutex
    std::time_mutex 定时mutex
    std::recursive_timed_mutex 定时递归mutex

lock类：
    std::lock_guard 与mutex RAll相关 方便上锁
    std::unique_lock 与mutex RAll相关 提供了更好的上锁和解锁

其他类型：
    std::once_flag
    std::adopt_lock_t
    std::defer_lock_t
    std::try_to_lock_t

函数：
    std::try_lock 尝试同时对多个互斥量上锁
    std::lock 同时对多个互斥量上锁
    std::call_once 如果多个线程需要同时调用某个函数，call_once可以保证多个线程对改函数只调用一次

volatile：
    一个类型修饰符，被设计用来修饰被不同线程访问和修改的变量，如果不加入volatile，要么无法编写多线程程序，要么编译器失去大量优化的机伿

timed_mutex::try_lock_for(timeout_duration)
    阻塞直到经过指定的 timeout_duration 或得到锁，取决于何者先到来。成功获得锁时返回 true, 否则返回 false

std::call_once：
    多个线程执行一个函数，只保证执行一次

std::promise：
    保存某一类型T的值，可被future对象读取(可能在另外线程)
    promise提供了一种线程同步手段，promise对象构造时可以和一个共享状态future关联

    std::promise::get_future()  
    std::promise::set_value()
    void set_value (const T& val);
    void set_value (T&& val);

*/

volatile int counter = 0;
const int max_recur_times = 10000;
mutex t_mutex;
timed_mutex time_mt;

//mutex 锁
void f(void)
{
    for (int i = 0; i < max_recur_times; i++) {
        if (t_mutex.try_lock()) {
            counter++;
            t_mutex.unlock();
        }
    }
}

//timed_mutex锁
void f2(int v, char tag)
{
    while (!time_mt.try_lock_for(chrono::milliseconds(1000))) {
        cout << v;
    }
    this_thread::sleep_for(chrono::milliseconds(1000));
    cout << tag << endl;
    time_mt.unlock();
}

//lock_guard 自动管理锁
void f3(int i)
{
    lock_guard<mutex> t_lock(t_mutex);
    cout << "value is " << i << endl;
    this_thread::sleep_for(chrono::milliseconds(200));
}

//unique_lock管理锁
void f4(int i)
{
    unique_lock<mutex> t_lock(t_mutex);
    // t_lock.lock(); 可选
    // t_lock.try_lock();
    cout << "value is " << i << endl;
    this_thread::sleep_for(chrono::milliseconds(200));
}

void setValue(int n)
{
    counter = n;
    cout << "in setvalue " << counter << endl;
}

//多线程只执行一次
once_flag value_flag;
void f5(int id)
{
    this_thread::sleep_for(chrono::milliseconds(200));
    call_once(value_flag, setValue, id + 1);
}

//通过std::future获取共享状态的值
void func6(future<int>& state)
{
    this_thread::sleep_for(chrono::milliseconds(100));
    int n = state.get();
    cout << "share state value " << n << endl;
}

//使用默认构造函数构造一个空共享状态的promise对象
promise<int> prom;
void func7()
{
    future<int> ft = prom.get_future();
    cout << "wait for future" << endl;
    // 这里会等待 其他线程设置 prom.set_value(10086)
    int fint = ft.get();
    cout << "future share int " << fint << endl;
}

void func8(promise<int>& p)
{
    int n{ 0 };
    cout << "please input an integer : ";
    //设置如试图从不能解析为整数的字符串里想要读一个整数等，顺便说下eof也会造成failbit被置位，则产生异常
    cin.exceptions(ios::failbit);
    try
    {
        cin >> n;
        p.set_value(n);
    }
    catch (exception&)
    {
        p.set_exception(current_exception());
    }
}

void func9(future<int>& f)
{
    try
    {
        int n = f.get();
        cout << "get future value is "<< n << endl;
    }
    catch (exception& e)
    {
        cout << "exception current:{" << e.what() << "}" << endl;
    }
}

int main()
{
    thread threads[10];
    /*
    for (int i = 0; i < 10; i++) {
        threads[i] = thread(f);
    }

    for (auto &t : threads) {
        t.join();
    }

    cout << "counter " << counter << endl;
    cout << "threads exe finished" << endl;
    */

    /*
    char end_tag[] = { '!', '@', '#', '$', '%', '^', '&', '*', '(', ')' };
    for (int i = 0; i < 10; i++) {
        threads[i] = thread(f2, i, end_tag[i]);
    }

    for (auto & t : threads) {
        t.join();
    }
    */


    /*
    for (int i = 0; i < 10; i++) {
        threads[i] = thread(f3, i);
    }

    for (auto & t : threads) {
        t.join();
    }
    */

    /*
    for (int i = 0; i < 10; i++) {
        threads[i] = thread(f4, i);
    }

    for (auto & t : threads) {
        t.join();
    }
    */

    /*
    for (int i = 0; i < 10; i++) {
        threads[i] = thread(f5, i);
    }

    for (auto & t : threads) {
        t.join();
    }

    cout << "counter is " << counter << endl;
    */

    /*
    promise<int> prom;
    //和future关联
    future<int> fut = prom.get_future();
    //将future交给线程t
    thread t(func6, ref(fut));
    //设置共享状态值  和线程t保存同步
    prom.set_value(10086);
    cout << "set value 10086" << endl;
    t.join();
    */

    /*
    thread t1(func7);
    this_thread::sleep_for(chrono::milliseconds(1000));
    prom.set_value(10086);
    cout << "set value 10086 end" << endl;
    t1.join();
    //promise<int>()创建一个匿名空的promise对象，使用移动拷贝构造函数给prom
    prom = promise<int>();

    thread t2(func7);
    prom.set_value(10010);
    cout << "set value 10010 end" << endl;
    t2.join();
    */

    /**/
    promise<int> prom;
    future<int> ft = prom.get_future();
    //这里t1和t2不能都用 func8重载函数
    thread t1(func8, ref(prom));
    thread t2(func9, ref(ft));
    t1.join();
    t2.join();

    cout << "threads end" << endl;
    cin.get();
    cin.get();
    return 0;
}
