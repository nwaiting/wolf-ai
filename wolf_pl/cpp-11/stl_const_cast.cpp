#include <iostream>
#include <stdint.h>

/*
    static_cast<>
        一般转换
    dynamic_cast<>
        能转换：
            通常用在基类和派生类转换时使用，只能由子类转换成基类
        不能转换：
            基础数据类型不能转换，转换具有继承关系的指针或引用，在转换前会进行对象类型检查
    const_cast<>
        主要针对const的转换
    reinterpret_cast<>
        用于没有任何关联之间的转换，比如指针转换为一个整数
*/

class Building{};
class Animal{};
class Cat :public Animal{};

//static_cast
//不可以用于多态类型的转换. 
//不可以用于静态类型的转换.
void func1()
{
    //1、基础类型转换
    int32_t a = 100;
    char b = static_cast<char>(a);
    std::cout << b << std::endl;

    //2、基础类型指针
    int32_t *p = new int32_t();
    //char *sp = static_cast<char*>(p);   //error !!!!!!!!!!!!!

    //3、对象指针
    Building *building = NULL;
    //Animal *anim = static_cast<Animal*>(building);  //error !!!!!!!!!!!!

}

/*
dynamic_cast<> 只能由子类转成父类，转换前会进行对象类型检查
    向下安全性转换，主要用于继承并且有虚函数中 !!!!!!!!

    原因在于 dynamic_cast做类型安全检查
    子类指针可以转换为父类指针（从大到小），类型安全，因为，子类包含父类的元素，指针作用域大，不会指针越界
    父类指针转换成子类指针（从小到达），类型不安全，会发生指针越界
*/
void func2()
{
    Cat *pa = new Cat;
    Animal *panimal = dynamic_cast<Animal*>(pa);

    Animal *panimal2 = new Animal;
    //Cat *pa2 = dynamic_cast<Cat*>(panimal2);    //error !!!!!!!
}

//const_cast<> 指针 引用或者对象指针，增加或者去除const属性
//const修饰的变量会被编译器优化到寄存器中,再次访问该变量时,就会直接从寄存器中区读取
void func3()
{
    int32_t a = 100;
    const int32_t &cb = a;
    int32_t &c = const_cast<int32_t&>(cb);  //const属性消失

    const int32_t* p = NULL;
    int32_t *pa = const_cast<int32_t *>(p); //ok const属性消失

    int32_t *q = NULL;
    const int32_t *cq = const_cast<const int32_t *>(q); //OK 增加const属性
}

//reinterpret_cast<>  强制类型转换，无关类型的
void func4()
{
    Building *pbuild = new Building;
    int32_t pint = reinterpret_cast<int32_t>(pbuild);

    int32_t *p = new int32_t();
    char *sp = reinterpret_cast<char*>(p);   

    Building *building = NULL;
    Animal *anim = reinterpret_cast<Animal*>(building); 
}

int main()
{
    func1();

    std::cin.get();
    return 0;
}
