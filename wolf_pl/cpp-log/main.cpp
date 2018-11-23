#include <iostream>
#include <string>
#include <vector>

/*
#include "easylogging++.h"
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
*/

#include "log4z.h"
#include <time.h>

int main()
{
	zsummer::log4z::ILog4zManager *log4z = zsummer::log4z::ILog4zManager::getPtr();
	std::string logpath("E:\\worker\\gitwork\\wolf-ai\\wolf_pl\\cpp-log");
	log4z->setLoggerPath(log4z->findLogger("Main"), logpath.c_str());
	log4z->setLoggerDisplay(log4z->findLogger("Main"), true);
	log4z->setLoggerLimitsize(log4z->findLogger("Main"), 100);	//设置为100M

	log4z->createLogger("Main");
	log4z->createLogger("engine");

	log4z->start();
	while (true) {
		LOGFMTI("this is %s", "LOGFMTI");
		LOGFMTF("this is %s", "LOGFMTF");
		Sleep(500);
	}
	std::cin.get();
	return 0;
}
