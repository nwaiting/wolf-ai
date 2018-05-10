#include <time.h>
#include <random>
#include <iostream>
using namespace std;

/*
    c++11之前随机数：
        srand() 设置种子，初始化rand() 
        rand() 获取随机数
        如：srand(time(NULL));
            rand() 获取随机数


    c++11提供了很多随机数的选择：
        均匀分布：
        uniform_int_distribution          整数均匀分布
        uniform_real_distribution        浮点数均匀分布

        伯努利类型分布：（仅有yes/no两种结果，概率一个p，一个1-p）
        bernoulli_distribution    伯努利分布
        binomial_distribution     二项分布
        geometry_distribution    几何分布
        negative_biomial_distribution  负二项分布

        Rate-based distributions:
        poisson_distribution 泊松分布
        exponential_distribution指数分布
        gamma_distribution 伽马分布
        weibull_distribution 威布尔分布
        extreme_value_distribution 极值分布

        正态分布相关：
        normal_distribution        正态分布
        chi_squared_distribution卡方分布
        cauchy_distribution       柯西分布
        fisher_f_distribution      费歇尔F分布
        student_t_distribution t分布

        分段分布相关：
        discrete_distribution离散分布
        piecewise_constant_distribution分段常数分布
        piecewise_linear_distribution分段线性分布
*/

int main()
{
    default_random_engine random(time(NULL));

    //随机数的范围为[]
    uniform_int_distribution<> uniform(1, 100);
    cout << "uniform_int_distribution " << endl;
    for (int i = 0; i < 5; i++)
    {
        cout << uniform(random) << endl;
    }

    uniform_real_distribution<> uniform2(0.0, 1.0);
    cout << "uniform_real_distribution " << endl;
    for (int i = 0; i < 5; i++)
    {
        cout << uniform2(random) << endl;
    }

    cin.get();
    return 0;
}

