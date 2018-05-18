#include <iostream>
#include <stdint.h>
#include <stdlib.h>
#include <iomanip>
using namespace std;

/*
    简单的梯度上升算法
    求 f(x) = -x^2 + 4x 的极值
*/

float grad(float x_old)
{
    return -2.0 * x_old + 4.0; // f(x)的导数
}

void func1()
{
    float x_old = -1.0;     //初始值，一个比x_new小的值
    float x_new = 0.0;      //梯度上升初始值，即从(0,0)开始
    float alpha = 0.01;     //学习率(步长)
    float presion = 0.0000001;  //精度
    int32_t loop_times = 0;
    while (abs(x_old-x_new) > presion) {
        x_old = x_new;
        x_new = x_old + alpha * grad(x_old);
        loop_times++;
    }

    printf("%f\n", x_new);
    //setprecision 输出10位数
    cout << setprecision(10) << x_new << " loop times " << loop_times << endl;
}

int main()
{
    func1();

    cin.get();
    return 0;
}
