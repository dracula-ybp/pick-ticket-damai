import asyncio
import time

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from damai.orderview import OrderView
from damai.performer import Performance


def main():
    async_scheduler = AsyncIOScheduler(timezone='Asia/Shanghai')
    order = OrderView()
    # 720288564028 2 5189134934172
    # 317 718335834447 5012364593187
    # 517 718335834447 5012364593188
    # 薛之谦深圳 718335834447, 5012364593189, 2 17:17,   hour=17, minute=16,  second=59
    url = order.make_order_url(721894781282, 5192625934218, 1)
    print(url)
    per = Performance()
    asyncio.get_event_loop().run_until_complete(per.init_browser())
    time.sleep(1)
    async_scheduler.add_job(per.place_order1, "cron",
                            hour=10, minute=59, second=59, args=(url, per.browser.newPage, 1))

    async_scheduler.start()
    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass


async def run():
    order = OrderView()
    # 317 718335834447 5012364593187
    # 517 718335834447 5012364593188 720288564028_1_5189134934171
    # 721894781282，5192625934218
    url = order.make_order_url(721894781282, 5192625934218, 1)
    print(url)
    per = Performance()
    await asyncio.create_task(per.init_browser())
    await asyncio.create_task(per.place_order1(url, per.browser.newPage, 1))


if __name__ == '__main__':
    # main()
    asyncio.run(run())

