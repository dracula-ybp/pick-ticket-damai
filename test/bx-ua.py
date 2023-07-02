# -- coding:utf-8 --
import asyncio
import re
import time
import hashlib
import json

import requests
from pyppeteer.launcher import connect
from pyppeteer.errors import ElementHandleError

# from damai.performer import ApiFetch
from damai.utils import make_ticket_params

cookie = 'cna=ZswmHTjTwUsCAXF24M+/Q9no; _samesite_flag_=true; cookie2=1a908c8541aed36023e5947e457b1170; t=989952bd5628a243958aacd2895b2620; _tb_token_=f48ed5387eb87; xlly_s=1; _hvn_login=18; munb=2216041624308; csg=09823ffc; _m_h5_tk=44fe3fe3fec282b05a17e001858751c5_1688207117313; _m_h5_tk_enc=d62d823ed0a800996b596997dab8d0a6; l=fBgWXarnN2WmEP2OBO5aKurza77TBIdfCsPzaNbMiIEGa6GdtFZR7NC1KSg9SdtjgTCUU3tyTBTBzdUpJg4ZixDDBeAHjt4KnxvO0MP9K; tfstk=dxGvcL6AwUQxCmL9iopk_q0P6b8kKj32wmuCslqcC0n-mVTVioViXRgUqfYqoKRteciuc-DmSCno40omoV01WPiuGRk0joqT6VoprHAHtqu4_StHxB2YElPi6Pwx-70qu5P63suBpqz9FTX5Xe_cKixlTul3ldaQOgNNOna8HkgJLt6vRrj3XqZR11ZYkOlStXpj1MqLStLJyOWahzRuvDRG.; usercode=244681378; dm_nickname=%E9%BA%A6%E5%AD%904Y1dD; havanaId=2216041624308; isg=BFFRjTx40f8BXT3rffCU5WdnYFvrvsUw3DGzoTPkH5g32nIsew5yADb7fK48Ul1o'
headers = {
    'accept-encoding': 'gzip,deflate,br',
    # "content-type": "application/x-www-form-urlencoded",
    "origin": "https://m.damai.cn",
    "referer": "https://m.damai.cn/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
}
h = {
    # 'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
    # 'sec-ch-ua-mobile': '?0',
    # 'sec-ch-ua-platform': 'macOS',
    # 'sec-fetch-dest': 'empty',
    # 'sec-fetch-mode': 'cors',
    # 'sec-fetch-site': 'same-site',
    # "accept": "application/json",
    "accept-language": "zh-CN,zh;q=0.9",
    "content-type": "application/x-www-form-urlencoded",
    # "cookie": cookie,
    # "globalcode": "ali.china.damai",
    "origin": "https://m.damai.cn",
    # "pragma": "no-cache",
    "referer": "https://m.damai.cn/",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
    # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF XWEB/8237"
}
# 725553760446_1_5208365938301

TOKEN = re.search(r'_m_h5_tk=(.*?)_', cookie).group(1)
APP_KEY = '12574478'


def _get_tb_sign(token, t, data):
    md5 = hashlib.md5()
    string = token + '&' + str(t) + '&' + APP_KEY + '&' + data
    string = string.encode('utf-8')
    md5.update(string)
    return md5.hexdigest()


def build(ua, umidtoken, c):
    print(ua)
    print(umidtoken)
    ex = {"channel": "damai_app", "damai": '1', "umpChannel": "100031004", "subChannel": "damai@damaih5_h5",
          "atomSplit": 1, "serviceVersion": "2.0.0", "customerType": "default"}
    d = {"buyNow": True,
         "exParams": json.dumps(ex, separators=(",", ":")),
         "buyParam": "725553760446_1_5208365938301", "dmChannel": "damai@damaih5_h5"}
    d = json.dumps(d, separators=(",", ":"))
    t = int(time.time() * 1000)
    tok = c['_m_h5_tk'].split('_')[0]
    sign = _get_tb_sign(tok, t, d)
    print('sign', sign)
    url = f'https://mtop.damai.cn/h5/mtop.trade.order.build.h5/4.0/?jsv=2.7.2&appKey=12574478&t={t}&sign={sign}&type=originaljson&dataType=json&v=4.0&H5Request=true&AntiCreep=true&AntiFlood=true&api=mtop.trade.order.build.h5&method=POST&ttid=%23t%23ip%23%23_h5_2014&globalCode=ali.china.damai&tb_eagleeyex_scm_project=20190509-aone2-join-test'
    data = {'data': d, 'bx-ua': ua, 'bx-umidtoken': umidtoken}
    response = requests.post(url, data=data, headers=h, cookies=c)
    print(response.request.url)
    return response.json()


def create(ua, umidtoken, data1, c):
    print(ua)
    print(umidtoken)
    print(data1)
    t = int(time.time() * 1000)
    print(c['_m_h5_tk'])
    tok = c['_m_h5_tk'].split('_')[0]
    sign = _get_tb_sign(tok, t, data1)
    print('sign', sign)
    querystring = {
        "jsv": "2.7.2", "appKey": "12574478", "t": t,
        "sign": sign, "v": "4.0", "post": "1", "type": "originaljson",
        "timeout": "15000", "dataType": "json", "isSec": "1", "ecode": "1", "AntiCreep": "true",
        "ttid": "#t#ip##_h5_2014", "globalCode": "ali.china.damai",
        "tb_eagleeyex_scm_project": "20190509-aone2-join-test", "H5Request": "true",
        "api": "mtop.trade.order.create.h5",
    }
    url = f'https://mtop.damai.cn/h5/mtop.trade.order.create.h5/4.0/?jsv=2.7.2&appKey=12574478&t={t}&sign={sign}&v=4.0&post=1&type=originaljson&timeout=15000&dataType=json&isSec=1&ecode=1&AntiCreep=true&ttid=%23t%23ip%23%23_h5_2014&globalCode=ali.china.damai&tb_eagleeyex_scm_project=20190509-aone2-join-test&H5Request=true&api=mtop.trade.order.create.h5'
    # &submitref=fc20c72e67fbe5fabc6ea68b34221e06b27b85bd3379f4179852c1f9dbb0929f
    # url = 'https://mtop.damai.cn/h5/mtop.trade.order.create.h5/4.0/?'
    data = {'data': data1, 'bx-ua': ua, 'bx-umidtoken': umidtoken}
    response = requests.post(url, data=data, headers=h, cookies=c)
    print(response.request.url)
    print(response.json())


async def init():
    browser = await connect(browserURL=f"http://127.0.0.1:9222")
    pages = await browser.pages()
    page = pages[0]
    print(await page.evaluate('navigator.userAgent'))
    return page


async def get_ua_and_umidtoken(page):
    try:
        bx_umidtoken = await page.evaluate('this.__baxia__.postFYModule.getUidToken()')
        bx_ua = await page.evaluate('this.__baxia__.postFYModule.getFYToken()')
        return bx_ua, bx_umidtoken
    except ElementHandleError:
        raise ValueError('失败')


def is_wx_session():
    t = int(time.time() * 1000)
    data1 = {"source": "h5", "dmChannel": "damai@weixin_weapp"}
    data1 = json.dumps(data1, separators=(",", ":"))
    sign = _get_tb_sign(TOKEN, t, data1)
    url = f'https://mtop.damai.cn/h5/mtop.damai.wireless.user.third.session.get/1.0/?jsv=2.7.2&appKey=12574478&t={t}&sign={sign}&type=originaljson&dataType=json&v=1.0&H5Request=true&AntiCreep=true&AntiFlood=true&api=mtop.damai.wireless.user.third.session.get&tb_eagleeyex_scm_project=20190509-aone2-join-test&requestStart=1688111223107&data=%7B%22source%22%3A%22h5%22%2C%22dmChannel%22%3A%22damai%40weixin_weapp%22%7D'
    response = requests.request("POST", url, headers=h)
    print(response.json())


async def start(page):
    # ua, token = await get_ua_and_umidtoken(page)
    # api = ApiFetch()
    # api.update_default_config(dict(COOKIE=cookie))
    # await api.open()
    # response = await api.build_order('725553760446_1_5208365938301', ua, token)
    # print(response["ret"])
    # ua, token = await get_ua_and_umidtoken(page)
    # params = make_ticket_params(response["data"])
    # response = await api.create_order(params, ua, token)
    # print(response["ret"])
    # await api.close()

    cookies = await page.cookies()
    cookies = cookie_serialization(cookies)
    a, b = await get_ua_and_umidtoken(page)
    response = build(a, b, cookies)
    print(response["ret"])

    x, y = await get_ua_and_umidtoken(page)
    create(x, y, make_ticket_params(response["data"]), cookies)


async def run():
    page = await init()
    await start(page)


def cookie_serialization(cookie_dict):
    """cookie序列化处理
    :return: type: dict cookie
    """
    cookies = {}
    for cd in cookie_dict:
        cookies[cd["name"]] = cd["value"]
    return cookies


async def init2():
    browser = await connect(browserURL=f"http://127.0.0.1:9222")
    pages = await browser.pages()
    page = pages[0]
    c = await page.cookies()
    print(cookie_serialization(c))
    await page.reload()
    c = await page.cookies()
    print(cookie_serialization(c))
    return page


if __name__ == '__main__':
    asyncio.run(run())
