import asyncio
from typing import Union, Optional

from damai.performer import Performance
from damai.orderview import OrderView
from damai.tasks import TaskManager


class ExecutionEngine:

    def __init__(self):
        self.task = TaskManager()
        self.order = OrderView()
        self.perform: Optional[Performance] = Performance()

    def add_task(self, name: Union[int, str], concert: str,
                 price: str, ticket_num: int):
        """添加异步任务至管理器

        name: 取决于在OrderView.add的参数
        concert_num，price_num：分别代表场次和价位
        ticket_num：需购数量
        """
        bind = self.order.views[name]
        sku_list = bind[concert]["skuList"]
        for sku in sku_list:
            if price == sku["priceName"]:
                url = self.order.make_order_url(sku["itemId"], sku["skuId"], ticket_num)
                self.task.bind_task(name, (self.perform.place_order,
                                           (url, self.perform.browser.newPage, ticket_num)))

    async def run_task(self, name):
        await self.task.run_tasks(name)


if __name__ == '__main__':
    engine = ExecutionEngine()
    engine.perform.init_browser()
    engine.order.add(718335834447)
    print(engine.order.views)
    engine.add_task(718335834447, '2023-07-28', '看台517元', 1)
    engine.add_task(718335834447, '2023-07-28', '看台317元', 1)
    print(engine.task.tasks)
    asyncio.get_event_loop().run_until_complete(engine.run_task(718335834447))
    print(engine.task.tasks)
