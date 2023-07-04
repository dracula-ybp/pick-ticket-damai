import asyncio

from damai import ExecutionEngine
from damai.configs import Configs

"""只会复制ITEM_ID时，task目前最好就添加一个吧，目前是单线程多个任务也是交替执行。
但是反正都是辅助捡漏票，交替也没啥关系。没试过！
"""

ITEM_ID = 720288564028

loop = asyncio.get_event_loop()

engine = ExecutionEngine(Configs())
loop.run_until_complete(engine.perform.init_browser())

engine.order.add(ITEM_ID)
print(engine.order.views)

engine.add_task(ITEM_ID, '2023-07-22', '看台517元', 1)
engine.add_task(ITEM_ID, '2023-07-23', '看台317元', 1)

loop.create_task(engine.run_task(ITEM_ID))
print(engine.task.tasks)
