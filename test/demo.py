from collections import Counter

counter = Counter()

data = ["库存不足", "库存不足", "库存不足", "库存不足", "哎呦喂，挤爆", "挤爆", "挤爆", "过期"]
for d in data:
    counter.update([d])
print(counter)


s = all(counter.get(i, 0) < 5 for i in ('挤爆', '库存不足'))
print(s)

# ---------------------------------

import asyncio


async def doing():
    print('start doing')
    await asyncio.sleep(3)
    print('end doing')
    return 2


async def rest():
    print('start rest')
    await asyncio.sleep(2)
    print('end rest')
    return 1


async def test():
    print('--------')

    results = await asyncio.gather(*[doing(), rest()])
    for result in results:
        print(result)

    print('========')


asyncio.run(test())

# ---------------------------------

loop = asyncio.get_event_loop()
print(loop)
res = loop.run_until_complete(doing())
print(res)
t1 = loop.create_task(doing())
t2 = loop.create_task(rest())
loop.run_until_complete(asyncio.wait([doing(), rest()]))

# ---------------------------------

import aiohttp


class Server:

    def __init__(self):
        self.session = aiohttp.ClientSession()

    async def close(self):
        await self.session.close()

    async def request(self):
        response = await self.session.get("https://www.baidu.com/")
        print(await response.read())


async def fetch():
    server = Server()
    print(server.session, server.session.closed)
    await server.request()
    await server.close()

    await asyncio.sleep(2)

    print(server.session, server.session.closed)
    await server.request()


asyncio.run(fetch())

# ---------------------------------

import asyncio
from pyppeteer import connect


async def main():
    browser = await connect(browserURL=f"http://127.0.0.1:9223")
    pages = await browser.pages()
    page = pages[0]
    resp = await page.evaluate('''
    fetch('https://mtop.damai.cn/h5/mtop.trade.order.build.h5/4.0/?jsv=2.7.2&appKey=12574478&t=1688371001404&sign=ab66592dbbc519c615774e20321efe05&type=originaljson&dataType=json&v=4.0&H5Request=true&AntiCreep=true&AntiFlood=true&api=mtop.trade.order.build.h5&method=POST&ttid=%23t%23ip%23%23_h5_2014&globalCode=ali.china.damai&tb_eagleeyex_scm_project=20190509-aone2-join-test&requestStart=1688371001402', {
        method: 'POST',
        headers: {
        },
    });
    ''')
    print(resp)


asyncio.get_event_loop().run_until_complete(main())

