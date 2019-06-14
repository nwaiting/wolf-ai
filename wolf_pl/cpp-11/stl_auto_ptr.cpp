#include <iostream>
#include <memory>

/*
参考：
    https://heleifz.github.io/14696398760857.html   shared_ptr 原理及事故
    https://blog.csdn.net/qq_29108585/article/details/78027867  shared_ptr的引用计数原理
    https://www.cnblogs.com/diysoul/p/5930372.html   C++智能指针 weak_ptr
    https://blog.csdn.net/albertsh/article/details/82286999 智能指针（三）：weak_ptr浅析

//在rocketdb中用到的
std::shared_ptr<>
    允许多个对象管理同一个指针，但仅当管理这个指针的最后一个对象析构时才调用delete
    注：1、引用计数容易出现循环引用问题

    shared_ptr<> 的引用计数本身是安全无锁的，但对象的读写则不是，因为share_ptr<> 有两个数据成员，读写操作不能原子化 !!!!!!!!!!!
    如果要从多个线程读写同一个share_ptr对象，那么需要加锁
    使用时注意事项：
        1、不使用相同的内置指针值初始化（或reset）多个智能指针
        2、不delete get函数返回的指针
        3、如果你使用了get返回的指针，记住当最后一个对应的智能指针销毁后，你的指针就变为无效了
        4、如果你使用智能指针管理的资源不是new分配的内存，记得传递给他一个删除器

std::unique_ptr<>
    1、unique_ptr类型指针不能赋值给其他的对象，但是可以通过返回值返回给其他指针
    2、不允许多个对象管理一个指针

std::make_shared<>

std::auto_ptr<>
    auto_ptr的出现，主要是为了解决“有异常抛出时发生内存泄漏”的问题

std::auto_ptr_ref<>

std::weak_ptr<>
    weak_ptr 是一种不控制对象生命周期的智能指针, 它指向一个 shared_ptr 管理的对象.
        进行该对象的内存管理的是那个强引用的 shared_ptr. weak_ptr只是提供了对管理对象的一个访问手段
    weak_ptr 设计的目的是为配合 shared_ptr 而引入的一种智能指针来协助 shared_ptr 工作, 它只可以从一个 shared_ptr或另一个weak_ptr对象构造, 它的构造和析构不会引起引用记数的增加或减少
    应用：
        使用 weak_ptr解决shared_ptr因循环引有不能释放资源的问题
        使用 shared_ptr 时, shared_ptr 为强引用, 如果存在循环引用, 将导致内存泄露. 而 weak_ptr 为弱引用, 可以避免此问题, 其原理:
            对于弱引用来说, 当引用的对象活着的时候弱引用不一定存在. 仅仅是当它存在的时候的一个引用, 弱引用并不修改该对象的引用计数, 这意味这弱引用它并不对对象的内存进行管理.
            weak_ptr 在功能上类似于普通指针, 然而一个比较大的区别是, 弱引用能检测到所管理的对象是否已经被释放, 从而避免访问非法内存。
        注意: 虽然通过弱引用指针可以有效的解除循环引用, 但这种方式必须在程序员能预见会出现循环引用的情况下才能使用, 也可以是说这个仅仅是一种编译期的解决方案, 如果程序在运行过程中出现了循环引用, 还是会造成内存泄漏.


*/

class Build
{
public:
    Build(){
        std::cout << __FUNCTION__ << std::endl;
    }
    ~Build(){
        std::cout << __FUNCTION__ << std::endl;
    }
    void Show(){
        std::cout << __FUNCTION__ << std::endl;
    }
};
class Animal{};
class Cat :public Animal{};

//std::unique_ptr<>
//  1、unique_ptr类型指针不能赋值给其他的对象，但是可以通过返回值返回给其他指针

void applyUniquePtr(std::unique_ptr<Build> pb)
{
    pb->Show();
}

void func1()
{
    //构造
    std::unique_ptr<Cat> pcat(new Cat);
    std::unique_ptr<Cat> pcat2(new Cat);

    //赋值
    //std::unique_ptr<Cat> pcat3 = pcat2; //error !!!!!!!!!!!!!!!
    std::unique_ptr<Cat> pcat3 = std::move(pcat2);
    std::unique_ptr<Cat> pcat4(std::move(pcat));

    //函数传值
    std::unique_ptr<Build> pbuilding(new Build);
    //func2(pbuilding); //error !!!!!!!!
    applyUniquePtr(std::move(pbuilding));
}

//std::shared_ptr<>
// shared_ptr<> 的引用计数本身是安全无锁的，但对象的读写则不是，因为share_ptr<> 有两个数据成员，读写操作不能原子化 !!!!!!!!!!!
// 如果要从多个线程读写同一个share_ptr对象，那么需要加锁
/*
使用时注意事项：
    1、不使用相同的内置指针值初始化（或reset）多个智能指针
    2、不delete get函数返回的指针
    3、如果你使用了get返回的指针，记住当最后一个对应的智能指针销毁后，你的指针就变为无效了
    4、如果你使用智能指针管理的资源不是new分配的内存，记得传递给他一个删除器

何时使用：
    1、程序不知道使用
*/
void func2()
{
    // 构造方法1
    std::shared_ptr<Build> pb1(new Build);
    std::shared_ptr<Build> pb2 = pb1;
    std::cout << pb1.use_count() << std::endl;

    //构造方法2
    std::shared_ptr<Build> pb3 = std::make_shared<Build>();
    std::cout << pb3.use_count() << std::endl;

    std::shared_ptr<int32_t> pb4 = std::make_shared<int32_t>(10086);
    std::cout << *pb4 << std::endl;
}

int main()
{
    //func1();
    func2();

    std::cin.get();
    return 0;
}
