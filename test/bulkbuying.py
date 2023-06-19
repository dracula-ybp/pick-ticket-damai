import asyncio

from damai.performer import Performance


async def test_batch():
    """批量选取多档次，未解决，一个浏览器实例好像不能真正意义上的并行捡票"""
    url = "https://m.damai.cn/app/dmfe/h5-ultron-buy/index.html?" \
          "exParams=%7B%22damai%22%3A%221%22%2C%22channel%22%3A%22damai_app%22%2C%22umpChannel%22%3A%2210002%22%2C" \
          "%22atomSplit%22%3A%221%22%2C%22serviceVersion%22%3A%221.8.5%22%7D&buyParam=711520310316_1_5196307218232" \
          "&buyNow=true&privilegeActId="
    instant = Performance()
    await asyncio.create_task(instant.init_browser())
    tasks = [instant.submit(url, instant.browser.newPage, 1), instant.submit(url, instant.browser.newPage, 1)]
    await asyncio.wait(tasks)


asyncio.run(test_batch())
