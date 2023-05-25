import asyncio

from pyppeteer.page import Page

from damai.performer import Performance as Base


class Performance(Base):
    """薛之谦演唱会购票

    在抢票中发现pc端大部分已不支持抢票，`buy_ticket`可忽略。现在着重更新
    `place_order`函数，利用接口先生成订单url，再调用`place_order`。
    """

    async def buy_ticket(self, id_, page=None):
        page = page or await self.page
        await page.setViewport(self.window_size)
        await page.goto(self.url.format(id_))
        await self.select_level(page)
        await asyncio.wait([
            page.click('div.buy-link'),
            page.waitForNavigation(),
        ])
        await page.waitFor(400)
        await self.place_order(page)

    async def select_level(self, page: Page):
        """选取档次，场次，数量，不支持选座"""
        items = await page.querySelectorAll('div.perform__order__select')
        for item in items:
            left = await item.querySelectorEval('div.select_left', 'el => el.textContent')
            right_list = await item.querySelectorAll(
                'div.select_right > div.select_right_list > div.select_right_list_item'
            )
            if right_list:
                p = right_list[self.data.get(left, 1) - 1]
                await p.click()
                await page.waitFor(400)  # 场次会决定票档选项列表
        await self.ticket_quantity(page)


