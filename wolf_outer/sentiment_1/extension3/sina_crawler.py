#coding=utf-8
from functions import *
import requests
import time
import random
import os
import json
import re

# add header for the crawler
headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}

# Add in your search list!
search_list = ["电影"]

# Create url encoded search list based on the word list you have gaven
urlencoded_search_list = url_encoding(search_list)
urls = create_url_list(urlencoded_search_list)

p = re.compile('<[^>]+>')

# loop for none stop run
day_count = 0
while 1:
    # define folder path
    today_folder = os.path.join("WBTestdata", today())

    # Testify if today's folder exist, if not, create
    if not os.path.exists(today_folder):
        print ("Today's first run! Create new folder.")
        os.makedirs(today_folder)

    # start mission, set 0, print out mission information: start time, date of today, how many days this program has run
    word_count = 0
    total_page_count = 0
    today_start_time = datetime.now()
    print("Start time: ", today_start_time)
    print("Today is: " + today())
    print("daycount: ", day_count)

    # loop for every word in the list
    for country in range(len(search_list)):
        word_count += 1
        unico_this_word = search_list[country]  # get current country in UNICODE
        this_baseurl = urls[country]  # create base url: without page number
        initial_page_number = 1  # define start page
        str_initial_page_number = str(initial_page_number)
        exception_count = 0  # exception count
        end_date = days_ago(2)  # Determine the date of when to end, format [03-30]

        this_end_time = 0
        this_file_path = os.path.join("WBTestdata", today(), unico_this_word + today() + "page" + ".txt")
        with open(this_file_path, "ab") as fd:
            for i in range(initial_page_number, initial_page_number + 300):  # Let's say, no more than 300 pages per word
                this_page_number = str(i)
                this_url = this_baseurl + this_page_number  # generate current url with current page number
                print("This is word number", word_count, ", the word is ", unico_this_word, ", this is page ",this_page_number)

                try:
                    req = requests.get(this_url, headers=headers, timeout=4)
                    content = json.loads(req.content.decode('utf-8'))
                    for item in content['data']['cards'][0]['card_group']:
                        try:
                            text = p.sub("", item["mblog"]["text"]).strip()
                            id = item["mblog"]["user"]["id"]
                            src = item["mblog"]['source']
                            this_end_time = item["mblog"]["created_at"]
                            fd.write("{0},{1},{2}\n".format(id,src,text).encode('utf-8'))  # write down data
                        except Exception as e:
                            print("error {0}".format(e))
                    print("total page count: ", total_page_count)
                    total_page_count += 1

                    if end_date > this_end_time:
                        print("current endtime: ", this_end_time)
                        print("We reached 2 days ago's data! Now sleep a while and call for next country!")
                        break
                    else:
                        print("current page's endtime: ", this_end_time)
                        print("Not enough! Sleep a while and continue requesting for next page!")
                        time.sleep(random.randint(30, 50))

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

                        # you can personalize your own report email here
                        # send an email to you when exception received more than 6 time
                        error_title = "Error!"
                        error_report = str(datetime.now())
                        send_email(user, pwd, recipient, error_title, error_report)

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
