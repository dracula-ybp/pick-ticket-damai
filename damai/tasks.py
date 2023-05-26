import asyncio


class TaskManager:
    def __init__(self):
        self.tasks = {}

    def bind_task(self, name, task):
        if name not in self.tasks:
            self.tasks[name] = []
        self.tasks[name].append(task)

    def unbind_task(self, name):
        if name in self.tasks:
            del self.tasks[name]

    async def run_tasks(self, name):
        if name in self.tasks:
            tasks = self.tasks[name]
            done, _ = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
            for task in done:
                task.result()
            self.unbind_task(name)
            for task in tasks:
                if not task.done():
                    task.cancel()


async def task1():
    print("Task 1 started")
    await asyncio.sleep(3)
    print("Task 1 completed")


async def task2():
    print("Task 2 started")
    await asyncio.sleep(5)
    print("Task 2 completed")


async def task3():
    print("Task 3 started")
    await asyncio.sleep(2)
    print("Task 3 completed")


async def main():
    task_manager = TaskManager()
    task_manager.bind_task("john", asyncio.create_task(task1()))
    task_manager.bind_task("john", asyncio.create_task(task2()))
    task_manager.bind_task("john", asyncio.create_task(task3()))

    await task_manager.run_tasks("john")
