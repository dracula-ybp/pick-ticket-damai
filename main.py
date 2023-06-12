import asyncio

from damai.orderview import OrderView
from damai.performer import Performance


async def run():
    order = OrderView()
    # test: 720545258599, 5016701340284
    # 714956979854 5199272746117
    url = order.make_order_url(714956979854, 4997413588173, 1)
    instant = Performance()
    await asyncio.create_task(instant.init_browser())
    await asyncio.create_task(instant.submit(url, instant.browser.newPage, 1))


if __name__ == '__main__':
    asyncio.run(run())
