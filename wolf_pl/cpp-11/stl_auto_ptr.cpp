#include <iostream>
#include <memory>

/*
//在rocketdb中用到的
https://heleifz.github.io/14696398760857.html

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
std::auto_ptr_ref<>
std::weak_ptr<>
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
