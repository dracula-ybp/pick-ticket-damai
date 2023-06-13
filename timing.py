import asyncio
import time

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from damai.orderview import OrderView
from damai.performer import Performance

# 薛之谦合肥 714956979854, 5199272746119, 1

ARGS = (720288564028, 5189134934172, 1)
TRIGGER = dict(hour=19, minute=26, second=59)


def main():
    scheduler = AsyncIOScheduler(timezone='Asia/Shanghai')
    order = OrderView()
    url = order.make_order_url(*ARGS)
    instant = Performance()
    asyncio.get_event_loop().run_until_complete(instant.init_browser())
    time.sleep(1)
    scheduler.add_job(instant.submit, "cron", args=(url, instant.browser.newPage, 1), **TRIGGER)
    scheduler.start()
    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass


main()
