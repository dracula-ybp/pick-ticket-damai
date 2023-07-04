import asyncio

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from damai.performer import WebDriverPerform

# 薛之谦合肥 714956979854, 5199272746119, 1
# 720336645935, 5033748485634, 1
ARGS = (721234813852, 5190876482301, 1)
TRIGGER = dict(hour=10, minute=59, second=59)


def main():
    scheduler = AsyncIOScheduler(timezone='Asia/Shanghai')
    instant = WebDriverPerform()
    # instant = ApiFetchPerform()
    asyncio.get_event_loop().run_until_complete(instant.init_browser())
    scheduler.add_job(instant.submit, "cron", args=ARGS, **TRIGGER)
    scheduler.start()
    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass


main()
