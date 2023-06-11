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

    async def init_browser(self, **config):
        """初始化配置"""
        self.browser = await connect(browserWSEndpoint=get_web_socket_debugger_url(), **config)

    @property
    async def page(self) -> Page:
        """默认标签页，新标签使用browser.newPage"""
        pages = await self.browser.pages()
        return pages[0]

    async def place_order(self, url, page, ticket_num: int = 1):
        """选取实名观影人，提交订单"""
        page: Page = await page() if callable(page) else await page
        nums = 60 * 20
        start = time.time()
        while True:
            await asyncio.wait([page.goto(url), page.waitForNavigation()])

            try:
                await page.waitForSelector('i.iconfont', timeout=3000)
            except TimeoutError:
                print(f"1 <title>{await page.title()}</title>")
                continue
            items = await page.querySelectorAll('i.iconfont')
            for num in range(0, ticket_num):
                await items[num].click()

            await page.waitFor(500)
            items = await page.querySelectorAll('#dmOrderSubmitBlock_DmOrderSubmitBlock div[view-name=TextView]')
            while True:
                try:
                    await items[-1].click()
                except Exception:
                    break
            # await page.waitForNavigation()
            print(f"2 <title>{await page.title()}</title>")
            if await page.title() in {"payment", "支付宝付款"} or time.time() - start > nums:
                break
        await page.close()

    async def place_order1(self, url, page, ticket_num: int = 1):
        """选取实名观影人，提交订单"""
        page: Page = await page() if callable(page) else await page
        # 第一个while True点击太快会触发网络拥堵，可以手动刷新，确保任务不被结束。
        while True:
            await asyncio.wait([page.goto(url), page.waitForNavigation()])
            try:
                await page.waitForSelector('i.iconfont', timeout=3000)
            except TimeoutError:
                title = await page.title()
                # 本次抢票未登录，重新登录抢票没啥戏了，直接结束
                if title == "登录":
                    return
                continue

            # 选择观影人
            items = await page.querySelectorAll('i.iconfont')
            for num in range(0, ticket_num):
                await items[num].click()
            await page.waitFor(500)

            items = await page.querySelectorAll('#dmOrderSubmitBlock_DmOrderSubmitBlock div[view-name=TextView]')

            while True:
                try:
                    # 提交订单
                    await items[-1].click()
                    await page.waitFor(500)
                except Exception:
                    break

                # 抢票成功
                if await page.title() in {"payment", "支付宝付款"}:
                    print('抢票成功')
                    await page.goto('https://orders.damai.cn/orderList')
                    return

                # 此处可能会出现库存不足，有订单未支付等。目前先这样设计，可能有回流票。
                confirm_content = await page.querySelectorAll('#confirmContent')
                if confirm_content:
                    text = await (await confirm_content[0].getProperty('textContent')).jsonValue()
                    # 抢票成功，有未支付订单提示
                    if "未支付订单" in text:
                        print('抢票成功')
                        await page.goto('https://orders.damai.cn/orderList')
                        return
                    cancel = await page.xpath('//div[@id="confirmContent"]/../following-sibling::div/div[1]')
                    await cancel[0].click()

                    # 网络拥堵，网络重试div
                    await page.waitFor(400)
                    if await page.querySelectorAll('.bannar'):
                        break


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


if __name__ == '__main__':

    async def main():
        url = 'https://m.damai.cn/app/dmfe/h5-ultron-buy/index.html?exParams=%7B%22damai%22%3A%221%22%2C%22channel%22' \
              '%3A%22damai_app%22%2C%22umpChannel%22%3A%2210002%22%2C%22atomSplit%22%3A%221%22%2C%22serviceVersion%22' \
              '%3A%221.8.5%22%2C%22umidToken%22%3A%22T2gAHw1r7GAtavV8IfjbKjRrT1rvfLMQ48dzsVbvL5DaslK-_6k4LN' \
              '-rSYGh0CSCSnQ%3D%22%2C%22ua%22%3A%22140%23/gToG6jwzzPW0Qo23zaF4pN8s77oMNzqYasU/fwSuYnIM0j%2ByKXl' \
              '%2BxzVamhb/QGm0VQ4q3hqzznsQqOTm81zzjVw9jWqlbrz2DD3V3gqzPMi228%2BtCfxzDrb3z//EHmijDapVrMn79/QCGKQA44d' \
              '/Q72lQpGncnlAH7CFZW0NXrrU%2BPf3rxaT9V7hPScGL' \
              '/mXpZ2TNzCIiZGmqCJ6K1js3sKL7hjEtzuFJ3efCvfvQfujhx9AqKwuzlbXMDnKxyKLzz%2BbQiXrJTsTSUuZ3vc%2B74mCg2QC' \
              '%2BzDfEnuvRCx4fyHXxp4/SFBZYKzzN/CftLj' \
              '/6nQuum1CrbmvXdCl1mpcNb5T4X6co5mvjtc2DiTxsRtYzvV1iXZJLCSYepRGXvREkcRjxxUYjmQxvp8' \
              '%2BdCWovPkyuBBecwiWA2kpemwVC1Jx%2BXRijpgmLhhfp2y9fdIgqWfNBAvGWUjtdx/QfdfmHsxRmQMcsGug' \
              '/%2ByP8KPO4iDLO2WrdSbxNC8oan9EiiKElmIAG3kMa0tNAe97EN8lRVMJfbxw3yAbioeYstliCL1HiPoY/gZlq4znnf7Otqka9e' \
              '%2BRuD2%2BjhdYw7h3avO8cj2nkaSkWMAYlVevysOLdezDQDTFOaEz485eFr%2B0lsydSRDJjKYvVSUQvREJM4thg' \
              '%2BgK08yUTyM3PjdG1Lz2LKYuckpR96BtncMN4kUxmJ2DSwASy4%2BVgWOSMLxJc3Cwgd7VR5PuTqgDNZ116bb0FRFto1' \
              '%2BMdnyVCbk5P4p23TpG5AK3mpEhsuWGfNPkV/o7VbL%2B6jSFfm7vhqAeIHJNNKvjYM/6sIDYVL8wK' \
              '/69fKcoMeZXT6ExOy3V87d64XT/jcISDT//F08V3vMTlC3jwc91EHy5R2ugb/X8wZ' \
              '/a3tQTTquQvhLG7OKmw2RKU35nWdCaEJEt3FPgkrOHRPb14bi9F%3D%3D%22%7D&buyParam=721216860314_1_5023638889416' \
              '&buyNow=true&privilegeActId= '
        p = Performance()
        await asyncio.create_task(p.init_browser())
        s = [p.place_order1(url, p.browser.newPage, 2)]

        await asyncio.wait(s)

    asyncio.run(main())
