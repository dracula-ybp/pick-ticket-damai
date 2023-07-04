import asyncio

from damai.performer import WebDriverPerform, ApiFetchPerform


ITEM_ID = 721234813852
SUK_ID = 5190876482301
TICKETS = 1


async def run():
    instant = WebDriverPerform()
    # instant = ApiFetchPerform()
    await asyncio.create_task(instant.init_browser())
    await asyncio.create_task(instant.submit(ITEM_ID, SUK_ID, TICKETS))


asyncio.run(run())
