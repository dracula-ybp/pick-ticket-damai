import asyncio
import time

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from damai.orderview import OrderView
from damai.performer import Performance


def main():
    scheduler = AsyncIOScheduler(timezone='Asia/Shanghai')
    order = OrderView()
    # 薛之谦合肥 714956979854, 5199272746119, 1
    # 721216860314, 5023638889416
    url = order.make_order_url(720288564028, 5189134934172, 1)
    instant = Performance()
    asyncio.get_event_loop().run_until_complete(instant.init_browser())
    time.sleep(1)
    scheduler.add_job(instant.submit, "cron",
                      hour=19, minute=26, second=59, args=(url, instant.browser.newPage, 1))
    scheduler.start()
    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass


main()
