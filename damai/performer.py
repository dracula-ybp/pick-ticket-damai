import asyncio
import sys
from typing import Optional

import requests
from pyppeteer.browser import Browser
from pyppeteer.launcher import connect
from pyppeteer.page import Page
from pyppeteer.errors import TimeoutError
from loguru import logger

from damai.errors import LoginError, NotElementError, CongestionError


class Performance:
    """演唱会捡票

    在开票后一直点击提交订单，会出现“请勿重复提交订单”，然后出现“网络拥堵“提示。
    几次开票测试中，出现“网络拥堵”，关闭后点击提交立马又出现，出现后几秒内刷新都没用。
    在捡漏成功时，感觉每次都没出现“请勿重复提交订单”，可能疯狂发送请求过去其实没啥用。
    出现网络拥堵，立即刷新页面，再次提交订单，反正直接捡漏成功。
    不知道是不是分批放票，每次捡漏成功，创建订单的时间也是在开票将近20s了。
    薛之谦深圳场17s创建订单，那么多人估计17s已经无了吧。也有2s创建订单成功的。

    薛之谦合肥场失败还没找出原因，实名制原因吗？
    """

    def __init__(self):
        self.browser: Optional[Browser] = None

    async def init_browser(self, **config):
        """初始化配置"""
        self.browser = await connect(browserWSEndpoint=get_web_socket_debugger_url(), **config)

    @property
    async def page(self) -> Page:
        """默认标签页，新标签使用browser.newPage"""
        pages = await self.browser.pages()
        return pages[0]

    async def submit(self, url: str, page, ticket_num: int = 1):
        page: Page = await page() if callable(page) else await page
        while True:
            logger.info('刷新一下')
            try:
                await asyncio.wait([page.goto(url), page.waitForNavigation()])
                await self.select_real_name(page, ticket_num)
                await page.waitFor(500)
                await self.polling(page)
            except (CongestionError, NotElementError) as e:
                logger.error(e)
                continue
            except LoginError:
                break
            except Exception as e:
                logger.error(e)

    async def select_real_name(self, page, ticket_num: int = 1):
        """选择实名制观演人，根据ticket_num勾选人数，默认勾选第一个。

        使用waitForSelector后， 网页元素改变和网络原因会抛出TimeoutError。
        """
        try:
            await page.waitForSelector('i.iconfont', timeout=2000)
        except TimeoutError:
            # 本次抢票未登录，直接结束。
            if await page.title() == "登录":
                raise LoginError('未登录，重新登录启动吧，可能捡到.')
            raise NotElementError('`i.iconfont`未找到，网络问题、出现提示框、标签改了其一')
        items = await page.querySelectorAll('i.iconfont')
        for num in range(0, ticket_num):
            await items[num].click()

    async def polling(self, page):
        select = '#dmOrderSubmitBlock_DmOrderSubmitBlock div[view-name=TextView]'
        items = await page.querySelectorAll(select)
        if not items:
            raise NotElementError(f'`{select}`未找到')

        button = items[-1]
        while True:
            # 2：提交两次订单，实测点击多了并没用，基本连续点击三次出现"网络拥堵"提示
            for _ in range(2):
                await button.click()
                logger.info('提交订单')
                # 存在bug,买票提交且成功还在加载但是下一个异步任务已经开始，
                # 导致page.title取到的还是提交页面的title，设置为450吧。
                # 不设置也行，但是程序不会按时结束，但是可以加速抢票流程
                await page.waitFor(450)
                if await page.title() in {"payment", "支付宝付款"}:
                    logger.info('polling 抢票成功，进入手机App订单管理付款')
                    sys.exit()
                await self.confirm_content_tip(page)

            if await self.is_refresh(page):
                raise CongestionError("网络拥堵")

    async def confirm_content_tip(self, page):
        """处理点击提交订单后弹出的提示
        "出现库存不足"：开票前几分钟内出现这个可以继续捡票
        "有订单未支付"：在手机app中抢票成功；在前次抢票成功后，没有及时结束程序
        """
        confirm_content = await page.querySelectorAll('#confirmContent')
        if confirm_content:
            text = await (await confirm_content[0].getProperty('textContent')).jsonValue()
            logger.info(text)
            # 如有未支付订单提示
            if "未支付订单" in text:
                logger.info('confirm_content_tip 抢票成功，进入手机App订单管理付款')
                sys.exit()
            cancel = await page.xpath('//div[@id="confirmContent"]/../following-sibling::div/div[1]')
            await cancel[0].click()

    async def is_refresh(self, page):
        frames = page.frames
        if len(frames) > 1:
            frame = frames[1]
            warn_element = await frame.querySelector('div.warnning-text')
            text = await (await warn_element.getProperty('textContent')).jsonValue()
            text = text.replace("\n", "")
            logger.info(text)
            return "网络" in text


def get_web_socket_debugger_url():
    try:
        # 端口可以修改成配置项，但是得开多进程，或者启动两次程序达到多个票档一起捡票。
        response = requests.get("http://127.0.0.1:9222/json/version", timeout=2)
    except requests.exceptions.ConnectionError:
        raise SystemExit('检查是否已经配置或开启调式谷歌浏览器')
    else:
        return response.json()["webSocketDebuggerUrl"]

