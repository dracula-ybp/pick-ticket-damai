import asyncio

from damai.orderview import OrderView
from damai.performer import Performance

"""两个id都会复制，定时任务意外结束，就使用这个"""

ITEM_ID = 721234813852
SUK_ID = 5190876482301
TICKET_NUM = 1
# 720336645935, 5033748485634


async def run():
    order = OrderView()
    url = order.make_order_url(ITEM_ID, SUK_ID, TICKET_NUM)
    instant = Performance()
    await asyncio.create_task(instant.init_browser())
    await asyncio.create_task(instant.submit(url, instant.browser.newPage, 1))


asyncio.run(run())
