#coding=utf-8
import requests
import time
import random
import os
import json
import re
import xlrd
from datetime import datetime
from datetime import timedelta
from urllib.parse import quote

"""
    https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D1%26q%3D%E6%9D%A8%E5%B9%82
    http://sinanews.sina.cn/interface/type_of_search.d.html?callback=initFeed&keyword=%E6%98%8E%E6%98%9F&page=30&type=siftWb&size=20&newpage=0&chwm=&imei=&token=&did=&from=&oldchwm=
"""

def today():
    time = str(datetime.now())
    print('time ', time)
    date = time.split(" ")[0]
    day = date[5:]
    print('day ', day)
    return day


def yesterday():
    yest = datetime.now() - timedelta(days=1)
    date = str(yest).split(" ")[0]
    day = date[5:]
    print('day ', day)
    return day

def days_ago(n):
    yest = datetime.now() - timedelta(days=n)
    date = str(yest).split(" ")[0]
    day = date[5:]
    return day


def url_encoding(list):
    url_word_list = []
    for country in list:
        url_word_list.append(quote(country))
    return url_word_list


def create_url_list(list):
    url_list = []
    for country in list:
        this_url = "http://m.weibo.cn/container/getIndex?type=wb&queryVal=" + country + \
          "&luicode=10000011&lfid=106003type%3D1&title=" + country + \
          "&containerid=100103type%3D2%26q%3D" + country + "&page="
        url_list.append(this_url)
        print('this_url ', this_url)
    return url_list



def format_datetime(time):
    this_date = time.split(' ')[0]
    this_time = time.split(' ')[1]
    mon = this_date.split('-')[0]
    day = this_date.split('-')[1]
    hor = this_time.split(':')[0]
    min = this_time.split(':')[1]
    return datetime(2017, int(mon), int(day), int(hor), int(min))


def get_this_endtime_text(content):
    this_data = content
    decoded_data = this_data.decode('utf-8')
    json_data = json.loads(decoded_data)
    try:
        this_endtime_text = json_data['data']['cards'][0]['card_group'][-1]['mblog']['created_at']
    except Exception as e:
        raise
    return this_endtime_text


def sleep_how_long(lag_hour, starttime, endtime):
    during = (endtime - starttime).total_seconds()
    lag_seconds = lag_hour * 3600
    during = lag_seconds - int(during)
    return during


def spider_word(word, end_dates=2):
    # add header for the crawler
    headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}

    # Add in your search list!
    search_list = [word]

    # Create url encoded search list based on the word list you have gaven
    urlencoded_search_list = url_encoding(search_list)
    urls = create_url_list(urlencoded_search_list)

    p = re.compile('<[^>]+>')

    # loop for none stop run
    day_count = 0
    # start mission, set 0, print out mission information: start time, date of today, how many days this program has run
    word_count = 0
    total_page_count = 0
    today_start_time = datetime.now()
    print("Start time: ", today_start_time)

    # loop for every word in the list
    for country in range(len(search_list)):
        word_count += 1
        unico_this_word = search_list[country]  # get current country in UNICODE
        this_baseurl = urls[country]  # create base url: without page number
        initial_page_number = 0  # define start page
        str_initial_page_number = str(initial_page_number)
        exception_count = 0  # exception count
        end_date = days_ago(end_dates)  # Determine the date of when to end, format [03-30]
        print('end_date ', end_date)

        this_end_time = 0
        try:
            if not os.path.exists("WBdata"):
                os.makedirs("WBdata")
        except Exception as e:
            print('error mkdir {0}'.format(e))
        this_file_path = os.path.join("WBdata", unico_this_word + ".csv")
        with open(this_file_path, "ab") as fd:
            for i in range(initial_page_number, initial_page_number + 300):  # Let's say, no more than 300 pages per word
                this_page_number = str(i)
                this_url = this_baseurl + this_page_number  # generate current url with current page number
                print("the word is ", unico_this_word, ", this is page ",this_page_number)

                try:
                    req = requests.get(this_url, headers=headers, timeout=4)
                    content = json.loads(req.content.decode('utf-8'))
                    weibo_start_time = content['data']['cardlistInfo']['starttime']
                    weibo_start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(weibo_start_time)))
                    for item in content['data']['cards'][0]['card_group']:
                        try:
                            text = p.sub("", item["mblog"]["text"]).strip()
                            id = item["mblog"]["user"]["id"]
                            src = item["mblog"]['source']
                            user_name = None
                            try:
                                user_name = item['mblog']['user']['screen_name']
                            except:
                                print('except user_name ', user_name)

                            user_description = None
                            try:
                                user_description = item['mblog']['user']['description']
                            except:
                                print('except user_description ', user_description)

                            this_end_time = item["mblog"]["created_at"]
                            fd.write("{0},{1},{2},{3},{4},{5},{6},{7}\n".format(id,user_name,user_description,weibo_start_time,"","",src,text).encode('utf-8'))  # write down data
                        except Exception as e:
                            print("error {0}".format(e))
                    total_page_count += 1

                    print('end_date {0}, this_end_time {1}'.format(end_date, this_end_time))
                    if end_date > this_end_time:
                        break
                    else:
                        time.sleep(random.randint(10, 20))

                # This situation happens when there is no weibo exist for the word your try to search
                # Pleas double check on the web page
                except IndexError:
                    print("There is no data! to the next country!")
                    break
                # Other than index error, it could also be request rejecting due to high frequency
                except Exception as e:
                    exception_count += 1
                    if exception_count > 6:
                        print("ehhhhh! I have failed 5 times for this country, I got to stop really long! 1 hour!")

                        exception_count = 0  # Set exception count back to 0 and sleep for 1 hour
                        time.sleep(600)

                    print("request has been rejected or failed! Sleep 1 minutes and try next page!")
                    print(e)
                    time.sleep(50)
                    continue
        print("Finish: " + unico_this_word + " sleep 10 seconds")
        time.sleep(10)

    # Print out today's mission information
    print("Finish today's work, sleep for tomorrow...")
    today_end_time = datetime.now()
    sleep_time = sleep_how_long(24, today_start_time, today_end_time)
    print("Today's sleep time is: ", sleep_time)
    print("Today start at: ", today_start_time)
    print("Today end at: ", today_end_time)
    print("Duration: ", today_end_time - today_start_time)
    print("Total page: ", total_page_count)

    day_count += 1
    word_count = 0
    time.sleep(sleep_time)

def main():
    while True:
        ## 接受键盘输入
        keyword = input('Enter the keyword(type \'quit\' to exit ):')
        if keyword == 'quit':
            sys.exit()
        spider_word(keyword)
        print('-----------------------------------------------------')

if __name__ == '__main__':
    main()
