#include <iostream>
#include "easylogging++.h"
#include <string>
#include <vector>

INITIALIZE_EASYLOGGINGPP

int main()
{ 
    //el::Logger* defaultLogger = el::Loggers::getLogger("D:\\opensource\\scrapy-work\\wolf_pl\\cpp-log\\default.log");
    el::Logger* defaultLogger = el::Loggers::getLogger("default");
    int32_t a = 100;
    std::string b("10086");
    defaultLogger->info("%d, %s", a, b.c_str());
 
    std::cin.get();
    return 0;
}
