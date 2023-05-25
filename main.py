import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from damai import OrderView
from damai.performer import Performance

config = dict(场次=1, 票档=3, 数量=1)
"""
测试 
【济南】张信哲未来式2.0世界巡回演唱会-济南站
时间：2023.06.10 周六 19:30
场馆：济南市 | 济南奥体中心体育场 
开售时间：05月24日 13:14
id=710437066929
"""


def main():
    async_scheduler = AsyncIOScheduler(timezone='Asia/Shanghai')
    order = OrderView()
    url = order.make_order_url(719062769469, 5183936506987, 1)
    print(url)

    per = Performance(config)
    async_scheduler.add_job(per.place_order, "cron",
                            hour=17, minute=17, kwargs=dict(direct=False, url=url))

    async_scheduler.start()
    print([str(job) for job in async_scheduler.get_jobs()])
    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass


if __name__ == '__main__':
    # main()
    order = OrderView()
    url = order.make_order_url(719062769469, 5183936506987, 1)
    print(url)

    p = Performance(config)
    asyncio.get_event_loop().run_until_complete(p.place_order(direct=False, url=url))
