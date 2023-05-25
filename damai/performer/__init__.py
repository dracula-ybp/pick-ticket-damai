import asyncio
import tkinter

import requests
from pyppeteer.launcher import connect
from pyppeteer.page import Page


class Performance:

    """演唱会购票

    在抢票中发现pc端大部分已不支持抢票，`buy_ticket`可忽略。现在着重更新
    `place_order`函数，利用接口先生成订单url，再调用`place_order`。
    """

    def __init__(self, data: dict, **kw):
        self.data = data
        self.url = "https://detail.damai.cn/item.htm?id={}"
        asyncio.get_event_loop().run_until_complete(self._init_browser(**kw))

    async def _init_browser(self, **kw_config) -> None:
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

    async def place_order(self, page: Page = None, direct=True, url=None):
        """选取实名观影人，提交订单"""
        page = page or await self.page
        if not direct:
            if url is None:
                raise ValueError('direct=True, url!=None')
            await asyncio.wait([
                page.goto(url),
                page.waitForNavigation(),
            ])
        await page.waitFor(850)
        items = await page.querySelectorAll('i.iconfont')
        for num in range(0, self.data.get('数量', 0)):
            await items[num].click()

        await page.waitFor(300)
        items = await page.querySelectorAll('#dmOrderSubmitBlock_DmOrderSubmitBlock div[view-name=TextView]')
        await items[-1].click()

    @property
    def window_size(self):
        tk = tkinter.Tk()
        width, height = tk.winfo_screenwidth(), tk.winfo_screenheight()
        tk.quit()
        return {'width': width, 'height': height}

    async def buy_ticket(self, id_, page=None):
        """购票"""
        print('后续将删除此函数')

    async def ticket_quantity(self, page: Page = None):
        print('后续将删除此函数')
        for num in range(1, self.data.get('数量', 1)):
            await page.click('a.cafe-c-input-number-handler.cafe-c-input-number-handler-up')


def get_web_socket_debugger_url():
    """获取webSocketDebuggerUrl，交给pyppeteer初始化配置中"""
    response = requests.get("http://127.0.0.1:9222/json/version")
    return response.json()["webSocketDebuggerUrl"]
