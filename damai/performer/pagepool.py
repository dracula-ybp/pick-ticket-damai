import asyncio
from pyppeteer import launch


class PagePool:
    def __init__(self, pool_size=5):
        self.pool_size = pool_size
        self.pool = asyncio.LifoQueue(maxsize=pool_size)
        self.browser = None

    async def get_page(self):
        if self.pool.empty():
            return await self.browser.newPage()
        return await self.pool.get()

    async def release_page(self, page):
        await self.pool.put(page)


# 示例用法
async def main():
    pool = PagePool(pool_size=3)

    # 初始化池
    await pool.initialize()

    # 使用页面
    page1 = await pool.get_page()
    # 使用 page1 执行任务
    await page1.goto('https://www.example.com')
    # 任务完成后释放页面
    await pool.release_page(page1)

    # 获取另一个页面并执行任务
    page2 = await pool.get_page()
    await page2.goto('https://www.example.com')
    await pool.release_page(page2)

    # 关闭池
    await pool.close()

# 运行示例
asyncio.get_event_loop().run_until_complete(main())
