import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from damai import OrderView
from damai.performer import Performance

"""
测试 
"""


def main():
    async_scheduler = AsyncIOScheduler(timezone='Asia/Shanghai')
    order = OrderView()
    url = order.make_order_url(721069251830, 5193339471403, 1)
    print(url)
    per = Performance()
    async_scheduler.add_job(per.place_order, "cron",
                            hour=10, minute=55, args=(url, None))

    async_scheduler.start()
    print([str(job) for job in async_scheduler.get_jobs()])
    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass


if __name__ == '__main__':
    # main()
    order_ = OrderView()
    url_ = order_.make_order_url(721069251830, 5193339471400, 1)
    p = Performance()
    asyncio.get_event_loop().run_until_complete(p.place_order(url_, None))
