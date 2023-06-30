# -- coding:utf-8 --
import asyncio
import re
import time
import hashlib
import json

import requests
from pyppeteer.launcher import connect
from pyppeteer.errors import ElementHandleError

from damai.performer import ApiFetch
from damai.utils import make_ticket_params

cookie = 'cna=X9YWHbUe6kACAduG3XxFaYhw; _samesite_flag_=true; cookie2=145c5b96e06510670cdf50cd70e83466; t=f3cb8c84289bba51ba0fe5c79a53f367; _tb_token_=ebeeb9716bde3; xlly_s=1; _m_h5_tk=0b89395bc4a800b644124e0851d96ad1_1688122201632; _m_h5_tk_enc=a526c417002f9c7f56b1e627a18ccc9b; _hvn_login=18; munb=2216041624308; csg=8d14da2e; l=fBxzxh9rN2K7qQidBO5aourza77ToIRfGsPzaNbMiIEGa1WRtFGOUNC1LffBSdtjgTCjYexrip0J_dHe-9aKNxDDBeAHjt4KDxvO0MP9K; tfstk=dkJvcGxac40D1EntnZhoQq-3r0ootKKqeE-QINb01ULJohi4nZXMW1tFrdm2mjk9wFTllsADjALkzU8Dmhx_XGTlh1RcSZbOBh8Kq2DnKn-VQ1gn-vDA4sB90G1vxTx20OWsg--I9nStwX3hfxmrGPw_Uaphcf_PeR7Tg3SAMNeGzRpJFJfRRHb8C29RQhpHpXXT-wIgM0n8_55f4drmZM5..; usercode=244681378; dm_nickname=%E9%BA%A6%E5%AD%904Y1dD; havanaId=2216041624308; isg=BLu7Tr6uW1wsUWf8FNGXVxB6Sp8lEM8St_iwb614nLr7DNvuNeGiYmmNJqxCLCcK'
headers = {
    'accept': 'application/json',
    'accept-encoding': 'gzip,deflate,br',
    "content-type": "application/x-www-form-urlencoded",
    "Cookie": cookie,
    "origin": "https://m.damai.cn",
    "referer": "https://m.damai.cn/",
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
}
h = {
    "content-type": "application/x-www-form-urlencoded",
    "cookie": cookie,
    "globalcode": "ali.china.damai",
    "origin": "https://m.damai.cn",
    "pragma": "no-cache",
    "referer": "https://m.damai.cn/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF XWEB/8237"

}
# 725553760446_1_5208365938301

TOKEN = re.search(r'_m_h5_tk=(.*?)_', cookie).group(1)

T = int(time.time() * 1000)
APP_KEY = '12574478'


def _get_tb_sign(token, t, data):
    md5 = hashlib.md5()
    string = token + '&' + str(t) + '&' + APP_KEY + '&' + data
    string = string.encode('utf-8')
    md5.update(string)
    return md5.hexdigest()


def build(ua, umidtoken):
    ex = {"channel": "damai_app", "damai": "1", "umpChannel": "100031004", "subChannel": "damai@damaih5_h5",
          "atomSplit": '1',
          "serviceVersion": "2.0.0", "customerType": "default"}
    d = {"buyNow": True,
         "exParams": json.dumps(ex, separators=(",", ":")),
         "buyParam": "725553760446_1_5208365938301", "dmChannel": "damai@damaih5_h5"}

    # d = {
    #     "buyNow": True,
    #     "exParams": json.dumps(
    #         {"channel": "damai_app", "damai": "1", "umpChannel": "100031002", "subChannel": "damai@weixin_weapp",
    #          "atomSplit": '1', "serviceVersion": "2.0.0", "customerType": "default"},
    #         separators=(",", ":")),
    #     "buyParam": "725553760446_1_5208365938301", "dmChannel": "damai@weixin_weapp"}
    d = json.dumps(d, separators=(",", ":"))
    t = int(time.time() * 1000)
    sign = _get_tb_sign(TOKEN, t, d)
    url = f'https://mtop.damai.cn/h5/mtop.trade.order.build.h5/4.0/?jsv=2.7.2&appKey=12574478&t={t}&sign={sign}&type=originaljson&dataType=json&v=4.0&H5Request=true&AntiCreep=true&AntiFlood=true&api=mtop.trade.order.build.h5&method=POST&ttid=%23t%23ip%23%23_h5_2014&globalCode=ali.china.damai&tb_eagleeyex_scm_project=20190509-aone2-join-test'
    data = {'data': d, 'bx-ua': ua, 'bx-umidtoken': umidtoken}
    response = requests.request("POST", url, data=data, headers=h)

    return response.json()


def create(ua, umidtoken, data1):
    t = int(time.time() * 1000)
    sign = _get_tb_sign(TOKEN, t, data1)
    url = f'https://mtop.damai.cn/h5/mtop.trade.order.create.h5/4.0/?jsv=2.7.2&appKey=12574478&t={t}&sign={sign}&v=4' \
          f'.0&post=1&type=originaljson&timeout=15000&dataType=json&isSec=1&ecode=1&AntiCreep=true&ttid=%23t%23ip%23' \
          f'%23_h5_2014&globalCode=ali.china.damai&tb_eagleeyex_scm_project=20190509-aone2-join-test&H5Request=true' \
          f'&api=mtop.trade.order.create.h5'
    data = {'data': data1, 'bx-ua': ua, 'bx-umidtoken': umidtoken}
    response = requests.request("POST", url, data=data, headers=h)
    print(response.json()['ret'])


async def init():
    browser = await connect(browserURL=f"http://127.0.0.1:9222")
    pages = await browser.pages()
    page = pages[0]
    return page


async def get_ua_and_umidtoken(page):
    try:
        bx_ua = await page.evaluate('this.__baxia__.getFYModule.getFYToken()')
        bx_umidtoken = await page.evaluate('this.__baxia__.getFYModule.getUidToken()')
        return bx_ua, bx_umidtoken
    except ElementHandleError:
        raise ValueError('SHIBAI')


def is_wx_session():
    t = int(time.time() * 1000)
    data1 = {"source": "h5", "dmChannel": "damai@weixin_weapp"}
    data1 = json.dumps(data1, separators=(",", ":"))
    sign = _get_tb_sign(TOKEN, t, data1)
    url = f'https://mtop.damai.cn/h5/mtop.damai.wireless.user.third.session.get/1.0/?jsv=2.7.2&appKey=12574478&t={t}&sign={sign}&type=originaljson&dataType=json&v=1.0&H5Request=true&AntiCreep=true&AntiFlood=true&api=mtop.damai.wireless.user.third.session.get&tb_eagleeyex_scm_project=20190509-aone2-join-test&requestStart=1688111223107&data=%7B%22source%22%3A%22h5%22%2C%22dmChannel%22%3A%22damai%40weixin_weapp%22%7D'
    response = requests.request("POST", url, headers=h)
    print(response.json())


async def start(page):
    ua, token = await get_ua_and_umidtoken(page)
    api = ApiFetch()
    api.update_default_config(dict(COOKIE=cookie))
    await api.open()
    response = await api.build_order('725553760446_1_5208365938301', ua, token)
    print(response["ret"])
    ua, token = await get_ua_and_umidtoken(page)
    params = make_ticket_params(response["data"])
    response = await api.create_order(params, ua, token)
    print(response["ret"])
    await api.close()

    # response = build(a, b)
    # print(response["ret"])
    # await asyncio.sleep(1)
    # # is_wx_session()
    # x, y = await get_ua_and_umidtoken(page)
    # create(x, y, make_ticket_params(response["data"]))


async def run():
    page = await init()
    await start(page)


if __name__ == '__main__':
    asyncio.run(run())
