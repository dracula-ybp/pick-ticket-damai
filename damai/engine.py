from typing import Union, Optional

from damai.performer import Performance
from damai.orderview import OrderView
from tasks import TaskManager


class ExecutionEngine:

    def __init__(self):
        self.task = TaskManager()
        self.order = OrderView()
        self.perform: Optional[Performance] = None

    def create_perform(self, **config) -> Performance:
        self.perform = Performance(**config)

    def add_task(self, name: Union[int, str], concert_num: int,
                 price_num: int, ticket_num: int):
        """添加异步任务至管理器

        name: 取决于在OrderView.add的参数
        concert_num，price_num：分别代表场次和价位，以下标的方式取出目标属性
        ticket_num：需购数量
        """
        bind = self.order.views[name]
        item = bind[concert_num][price_num]
        url = self.order.make_order_url(item["itemId"], item["skuId"], ticket_num)
        self.task.bind_task(name, (self.perform.place_order,
                                   (url, self.perform.browser.newPage, ticket_num)))

    async def run_task(self, name):
        await self.task.run_tasks(name)


# engine = ExecutionEngine()
# engine.create_perform()
# engine.order.add(718335834447, '薛之谦-深圳站')
# engine.add_task('薛之谦-深圳站', 0, 1, 1)
# print(engine.order.views)
# print(engine.task.tasks)
