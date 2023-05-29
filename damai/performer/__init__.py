import asyncio
import time
import tkinter

import requests
from pyppeteer.launcher import connect
from pyppeteer.page import Page
from pyppeteer.errors import TimeoutError


class Performance:
    """演唱会购票

    在抢票中发现pc端大部分已不支持抢票，`buy_ticket`可忽略。现在着重更新
    `place_order`函数，利用接口先生成订单url，再调用`place_order`。
    """

    def __init__(self, **config):
        asyncio.get_event_loop().run_until_complete(self.init_browser(**config))

    async def init_browser(self, **kw_config):
        """初始化配置"""
        connect_params = {
            'browserWSEndpoint': get_web_socket_debugger_url(),
        }
        self.browser = await connect(connect_params, **kw_config)

    @property
    async def page(self) -> Page:
        """默认标签页，新标签使用browser.newPage"""
        pages = await self.browser.pages()
        return pages[0]

    async def place_order(self, url, page, ticket_num: int = 1):
        """选取实名观影人，提交订单"""
        print(url)
        page = page or self.page
        page: Page = await page() if callable(page) else await page
        num = 60 * 20
        start = time.time()
        while True:
            await asyncio.wait([page.goto(url), page.waitForNavigation()])
            try:
                await page.waitForSelector('i.iconfont', timeout=3000)
            except TimeoutError:
                print(f"<title>{await page.title()}</title>")
                break

            items = await page.querySelectorAll('i.iconfont')
            for num in range(0, ticket_num):
                await items[num].click()

            await page.waitFor(500)
            items = await page.querySelectorAll('#dmOrderSubmitBlock_DmOrderSubmitBlock div[view-name=TextView]')
            await items[-1].click()

            await page.waitForNavigation()
            print(f"<title>{await page.title()}</title>")
            if await page.title() == "payment" or time.time() - start > num:
                break
        await page.close()

    @property
    def window_size(self):
        tk = tkinter.Tk()
        width, height = tk.winfo_screenwidth(), tk.winfo_screenheight()
        tk.quit()
        return {'width': width, 'height': height}


def get_web_socket_debugger_url():
    """获取webSocketDebuggerUrl，交给pyppeteer初始化配置中"""
    try:
        response = requests.get("http://127.0.0.1:9222/json/version", timeout=2)
    except requests.exceptions.ConnectionError:
        raise SystemExit('检查是否已经配置或开启调式谷歌浏览器')
    else:
        return response.json()["webSocketDebuggerUrl"]
