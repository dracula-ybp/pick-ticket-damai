import asyncio
from typing import Union

from damai.performer import Performance
from damai.orderview import OrderView
from tasks import TaskManager


class ExecutionEngine:

    def __init__(self):
        self.task = TaskManager()
        self.order = OrderView()
        self.perform = None

    def create_perform(self):
        self.perform = Performance()

    async def add_task(self, name: Union[int, str], concert_num: int,
                       price_num: int, ticket_num: int):
        """添加异步任务至管理器

        name: 取决于在OrderView.add的参数
        concert_num，price_num：分别代表场次和价位，以下标的方式取出目标属性
        ticket_num：需购数量
        """
        bind = self.order.views[name]
        print(self.order.views)
        print(bind)
        print(type(bind))
        print(bind.__dict__)
        print(type(bind[concert_num]))
        item = bind[concert_num][price_num]
        url = self.order.make_order_url(item.itemId, item.itemId, ticket_num)
        self.task.tasks[name] = url
        self.task.bind_task(name, asyncio.create_task(
            self.perform.place_order(url, await self.perform.browser.newPage(), ticket_num)
        ))

    async def run_task(self, name):
        await self.task.run_tasks(name)


engine = ExecutionEngine()
print(engine.order.views)
engine.order.add(719062769469)
asyncio.run(engine.add_task(719062769469, 0, 1, 1))
print(engine.order.views)
print(engine.task.tasks)

