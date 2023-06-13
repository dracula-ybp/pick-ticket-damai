import asyncio

from damai.orderview import OrderView
from damai.performer import Performance

"""两个id都会复制，定时任务意外结束，就使用这个"""

ITEM_ID = 714956979854
SUK_ID = 5199272746119
TICKET_NUM = 1


async def run():
    order = OrderView()
    url = order.make_order_url(ITEM_ID, SUK_ID, TICKET_NUM)
    instant = Performance()
    await asyncio.create_task(instant.init_browser())
    await asyncio.create_task(instant.submit(url, instant.browser.newPage, 1))


asyncio.run(run())
