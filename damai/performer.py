import asyncio
import re

import aiohttp
import json
import sys
import time
from typing import Optional

from aiohttp import TCPConnector
from pyppeteer.browser import Browser
from pyppeteer.launcher import connect
from pyppeteer.page import Page
from pyppeteer.errors import TimeoutError, ElementHandleError
from loguru import logger

from damai.errors import LoginError, NotElementError, CongestionError
from damai.utils import get_sign, timestamp, make_ticket_params


class Performance:

    DEFAULT_CONFIG = dict(PORT=9222)

    def __init__(self):
        self.browser: Optional[Browser] = None

    def update_default_config(self, configs=None):
        if configs:
            for key in self.DEFAULT_CONFIG.keys():
                if key in configs:
                    self.DEFAULT_CONFIG[key] = configs[key]

    async def init_browser(self, **config):
        self.browser = await connect(
            browserURL=f"http://127.0.0.1:{self.DEFAULT_CONFIG['PORT']}", **config
        )

    @property
    async def page(self) -> Page:
        pages = await self.browser.pages()
        return pages[0]

    def submit(self, *args, **kwargs):
        raise NotImplementedError()


class WebDriverPerformance:

    """模拟浏览器购票

    在开票后一直点击提交订单，会出现“请勿重复提交订单”，然后出现“网络拥堵“提示。
    几次开票测试中，出现“网络拥堵”，关闭后点击提交立马又出现，出现后几秒内刷新都没用。
    在捡漏成功时，感觉每次都没出现“请勿重复提交订单”，可能疯狂发送请求过去其实没啥用。
    出现网络拥堵，立即刷新页面，再次提交订单，反正直接捡漏成功。

    推荐把浏览器缩放50%，后面发现页面被修改了，不缩放可能造成无法勾选实名观演人
    """

    DEFAULT_CONFIG = dict(
        CRITICAL_WAIT=450, WARN_WAIT=100, SUBMIT_FREQUENCY=2,
        SHUTDOWN=60 * 10
    )

    def __init__(self):
        self.browser: Optional[Browser] = None

    async def submit(self, url: str, page, ticket_num: int = 1):
        start = time.time()
        page: Page = await page() if callable(page) else await page
        while True:
            logger.info('刷新一下')
            try:
                await asyncio.wait([page.goto(url), page.waitForNavigation()])
                await self.select_real_name(page, ticket_num)
                await page.waitFor(self.DEFAULT_CONFIG['CRITICAL_WAIT'])
                await self.polling(page)
            except (CongestionError, NotElementError) as e:
                logger.error(e)
                continue
            except LoginError:
                break
            except Exception as e:
                logger.error(e)

            if time.time() - start > 60 * 8:
                return

    async def select_real_name(self, page, ticket_num: int = 1):
        """选择实名制观演人，根据ticket_num勾选人数，默认勾选第一个。

        使用waitForSelector后， 网页元素改变和网络原因会抛出TimeoutError。
        """
        selector = "i.iconfont.icondanxuan-weixuan_"
        try:
            await page.waitForSelector(selector, timeout=2000)
        except TimeoutError:
            # 本次抢票未登录，直接结束。
            if await page.title() == "登录":
                raise LoginError('未登录，重新登录启动吧，可能捡到.')
            raise NotElementError(f'`{selector}`未找到，网络问题、出现提示框、标签改了其一')
        items = await page.querySelectorAll(selector)
        for num in range(0, ticket_num):
            await items[num].click()

    async def polling(self, page):
        # 需要优化
        selector = '#dmOrderSubmitBlock_DmOrderSubmitBlock div[view-name=TextView]'
        items = await page.querySelectorAll(selector)
        if not items:
            raise NotElementError(f'`{selector}`未找到')

        button = items[-1]
        while True:
            # 实测点击多了并没用，基本连续点击三次出现"网络拥堵"提示
            for _ in range(self.DEFAULT_CONFIG['SUBMIT_FREQUENCY']):
                await button.click()
                logger.info('提交订单')
                # 存在bug,买票提交且成功还在加载但是下一个异步任务已经开始，
                # 导致page.title取到的还是提交页面的title
                # 不设置也行，但是程序不会按时结束，但是可以加速抢票流程
                await page.waitFor(self.DEFAULT_CONFIG["WARN_WAIT"])
                if await page.title() in {"payment", "支付宝付款"}:
                    logger.info('polling 抢票成功，进入手机App订单管理付款')
                    sys.exit()
                await self.confirm_content_tip(page)

            if await self.is_refresh(page):
                await page.waitFor(2000)
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


class ApiFetchPerformance(Performance):

    DEFAULT_CONFIG = dict(
        **Performance.DEFAULT_CONFIG,
        CHANNEL="damai@damaih5_h5", APP_KEY=12574478, COOKIE=None,
        USER_AGENT="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko)"
                   " Chrome/112.0.0.0 Safari/537.36"
    )

    @property
    def headers(self):
        return {
            "content-type": "application/x-www-form-urlencoded",
            "cookie": self.DEFAULT_CONFIG["COOKIE"],
            "globalcode": "ali.china.damai",
            "origin": "https://m.damai.cn",
            "referer": "https://m.damai.cn/",
            "user-agent": self.DEFAULT_CONFIG["USER_AGENT"]
        }

    @property
    def token(self):
        return re.search(r'_m_h5_tk=(.*?)_', self.DEFAULT_CONFIG["COOKIE"]).group(1)

    def update_default_config(self, configs=None):
        super().update_default_config(configs)
        if not self.DEFAULT_CONFIG["COOKIE"]:
            raise ValueError(f"{self}需要配置COOKIE")

    async def open(self):
        self.session = aiohttp.ClientSession(headers=self.headers, connector=TCPConnector(ssl=False))

    async def close(self):
        await self.session.close()

    async def submit(self, buy_parma):
        await self.open()
        response = await self.build_order(buy_parma)
        print(response["ret"])
        params = make_ticket_params(response["data"])
        response = await self.create_order(params)
        print(response["ret"])
        await self.close()

    async def build_order(self, buy_parma):
        ep = {
            "channel": "damai_app", "damai": "1", "umpChannel": "100031004",
            "subChannel": self.DEFAULT_CONFIG["CHANNEL"], "atomSplit": '1',
            "serviceVersion": "2.0.0", "customerType": "default"
        }
        data = {
            "buyNow": True, "exParams": json.dumps(ep, separators=(",", ":")),
            "buyParam": buy_parma, "dmChannel": self.DEFAULT_CONFIG["CHANNEL"]
        }
        data = json.dumps(data, separators=(",", ":"))
        t = timestamp()
        sign = get_sign(self.token, t, self.DEFAULT_CONFIG["APP_KEY"], data)
        url = f'https://mtop.damai.cn/h5/mtop.trade.order.build.h5/4.0/?'
        params = {
            "jsv": "2.7.2", "appKey": self.DEFAULT_CONFIG["APP_KEY"], "t": t, "sign": sign,
            "type": "originaljson", "dataType": "json", "v": "4.0", "H5Request": "true",
            "AntiCreep": "true", "AntiFlood": "true", "api": "mtop.trade.order.build.h5",
            "method": "POST", "ttid": "#t#ip##_h5_2014", "globalCode": "ali.china.damai",
            "tb_eagleeyex_scm_project": "20190509-aone2-join-test"
        }
        bx_ua, bx_umidtoken = await self.ua_and_umidtoken()
        data = {'data': data, 'bx-ua': bx_ua, 'bx-umidtoken': bx_umidtoken}
        response = await self.session.post(url, params=params, data=data)
        return await response.json()

    async def create_order(self, data):
        t = timestamp()
        sign = get_sign(self.token, t, self.DEFAULT_CONFIG["APP_KEY"], data)
        url = 'https://mtop.damai.cn/h5/mtop.trade.order.create.h5/4.0/?'
        params = {
            "jsv": "2.7.2", "appKey": self.DEFAULT_CONFIG["APP_KEY"], "t": t, "sign": sign, "v": "4.0",
            "post": "1", "type": "originaljson", "timeout": "15000", "dataType": "json",
            "isSec": "1", "ecode": "1", "AntiCreep": "true", "ttid": "#t#ip##_h5_2014",
            "globalCode": "ali.china.damai", "tb_eagleeyex_scm_project": "20190509-aone2-join-test",
            "H5Request": "true", "api": "mtop.trade.order.create.h5"
        }
        bx_ua, bx_umidtoken = await self.ua_and_umidtoken()
        data = {'data': data, 'bx-ua': bx_ua, 'bx-umidtoken': bx_umidtoken}
        response = await self.session.post(url, params=params, data=data)
        return await response.json()

    async def ua_and_umidtoken(self) -> tuple:
        """目前使用默认页面"""
        page = await self.page
        try:
            bx_ua = await page.evaluate('this.__baxia__.postFYModule.getFYToken()')
            bx_umidtoken = await page.evaluate('this.__baxia__.postFYModule.getUidToken()')
            return bx_ua, bx_umidtoken
        except ElementHandleError:
            raise SystemExit('目前bx_ua, umidtoken需要在订单页面, 切换标签页')


async def main():
    cookie = 'cna=01spHfE7mkEBASQOBH1IGazq; _samesite_flag_=true; cookie2=178bc0c8bfbcdf976b60b45e45554620; t=66d4f937c8db0c40e0c90fbb1db31c9f; _tb_token_=7ee76e6eeb86b; xlly_s=1; _hvn_login=18; munb=2216041624308; csg=a1568246; _m_h5_tk=7c45e498f6fa6df924e58ec3526d7671_1688389533167; _m_h5_tk_enc=a4b5f42d0cd48a83cc32d13096305dfc; dm_nickname=%E9%BA%A6%E5%AD%904Y1dD; usercode=244681378; havanaId=2216041624308; isg=BHFxLnEesaJeJx22ruJbHZCBgP0LXuXQ1eGYVVOGhjhXepTMlq52oFDbnQ4ck30I; l=fBO-bjdRN-31vyb0BO5alurza77T5IRfCOVzaNbMiIEGa69dtFMDmNC10jm9SdtxgTCbvEKrqYn2gdUpJGadNxDDBeAHjt4KnxvO0MP9K; tfstk=d3f2cZ1yzSFVYbpzjdANzS5Ys6Av_BECo1t6SNbMlnxchCOwjNbMcFt1SFRNVG7XIoQ141SfVZZAfIia_g-5ff_f_ThNJNCbkCavMZd9skZQOC7AkCnC9_yWMLfx40EQAWNCN3Zzfk1_L8lFfoK8a2GWpX_9qsW6GZrnJhxrsX0p-KcRuAGET_823G7cQ6o9rZVc6toiIKYJzHazzzPHg71..'
    api = ApiFetchPerformance()
    api.update_default_config(dict(COOKIE=cookie))
    await api.init_browser()
    await api.submit('724811045159_1_5036084393602')


if __name__ == '__main__':
    asyncio.run(main())
