"""目前仅支持一次添加一个任务"""

import asyncio
import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from loguru import logger

from damai.configs import Configs
from damai.engine import ExecutionEngine


class Runner:

    def __init__(self, configs=None):
        if isinstance(configs, dict) or configs is None:
            self.configs = Configs(configs)

        self.engine = ExecutionEngine()
        self.engine.perform.update_default_config(self.configs)

        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.engine.perform.init_browser())

        self._scheduler = AsyncIOScheduler(timezone='Asia/Shanghai')
        self.single = False

    def start(self):
        self._execute_accord_to_config()
        if self.single:
            self._scheduler.start()
            try:
                asyncio.get_event_loop().run_forever()
            except (KeyboardInterrupt, SystemExit):
                pass

    def _execute_accord_to_config(self):
        item_id = self.configs["ITEM_ID"]
        self.engine.order.add(item_id)
        self.engine.add_task(item_id, self.configs["CONCERT"],
                             self.configs["PRICE"], self.configs["TICKET"])
        name, date = self.engine.order.get_sell_item(item_id)

        d = self.configs.get("RUN_DATE", None)
        if d:
            date = datetime.datetime.strptime(str(d), "%Y%m%d%H%M").timestamp()

        run_date = datetime.datetime.fromtimestamp(int(date) - 1)
        if run_date >= datetime.datetime.now():
            self.single = True
            self._scheduler.add_job(self.engine.run_task, 'date', run_date=run_date,
                                    args=(item_id, ), name=name)
            logger.info(f'\n{name}\n抢票时间：{run_date}\n场次：{self.configs["CONCERT"]}\n'
                        f'价格：{self.configs["PRICE"]}\n数量：{self.configs["TICKET"]}')
        else:
            asyncio.get_event_loop().run_until_complete(self.engine.run_task(item_id))



