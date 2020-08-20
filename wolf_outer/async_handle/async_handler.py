import asyncio
import time
import requests

"""
    https://www.jianshu.com/p/ac27b68a8fa3      python asyncio实现
    https://www.lizenghai.com/archives/20409.html       asyncio源码分析之基本执行流程
"""


async def get_url():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36"
    }
    get = lambda: requests.get('https://github.com/', headers=headers)
    inner_loop = asyncio.get_event_loop()
    res = await inner_loop.run_in_executor(None, get)
    return res.status_code


async def show(n):
    print('begin n={}'.format(n))
    # await asyncio.sleep(1)
    res = await get_url()
    print('end n={} {}'.format(n, res))

start = time.time()
tasks = [asyncio.ensure_future(show(i)) for i in range(1, 6)]
loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(tasks))
print('cost {}'.format(time.time() - start))


begin = time.time()
for i in range(1, 6):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36"
    }
    requests.get('https://github.com/', headers=headers)
print('cost={}'.format(time.time()-begin))


class AsyncioEvent(object):
    def __init__(self):
        pass

    async def init(self):
        pass

    async def run(self):
        pass





