# -- coding:utf-8 --

import asyncio
import re
import time
import hashlib
import json

import requests
from pyppeteer.launcher import connect
from pyppeteer.errors import ElementHandleError

from damai.performer import ApiFetchPerform
from damai.utils import make_ticket_data

cookie = '_m_h5_tk=63705290fef50b47cb389167d1c6c874_1688374107651; _m_h5_tk_enc=79c5ece5e9a0d0842066fcbdc5f200c8; cna=01spHfE7mkEBASQOBH1IGazq; _samesite_flag_=true; cookie2=178bc0c8bfbcdf976b60b45e45554620; t=66d4f937c8db0c40e0c90fbb1db31c9f; _tb_token_=7ee76e6eeb86b; xlly_s=1; _hvn_login=18; munb=2216041624308; csg=bc865ed5; usercode=244681378; dm_nickname=%E9%BA%A6%E5%AD%904Y1dD; havanaId=2216041624308; x5sec=7b22617365727665723b32223a223731333734653161393134303133346330666166636331313936393766303462434f662b69615547454e4f433462446974503770775145776735435530774e4141773d3d227d; isg=BCcnC8ksD5w6Y4sQhBC1E5qztlvxrPuOD7Nus_mUBrbd6EWqAX323kApCuj2ANMG; tfstk=dpdwz8OF8fhZew6Emtf28rkkIxfOG_nSmIsfoEYc5GjM5it2oM-oWOM9CpS2YMIMcNfMgZxHotVfhAQ4gM-dlIgOhpW2Ph5XGEAbtH7RAiji6fKBApYlCIO2kS7Don3OcVHBWFCAi0i5gbT9WlXxd4gZn5AyrsmSVbwQ-On1iIgr1MI6kNi8yvWuNEIH_KhdnnEKzGP0iCcAQg7UhSNfsNBwiFXaLoQHSfAvQo2cIwQFV2uE8bfZO; l=fBO-bjdRN-31v4sdBOfwEurza77ttIRVguPzaNbMi9fPOC1p5peOW1s2dJ89CnGVesdpR3ooemR2Bj8HiyhSnxv9-wD2Hg2rFdhyN3pR.'

headers = {
    # 'sec-ch-ua': 'Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114',
    # 'sec-ch-ua-mobile': '?0',
    # 'sec-ch-ua-platform': '"Windows"',
    # 'sec-fetch-dest': 'empty',
    # 'sec-fetch-mode': 'cors',
    # 'sec-fetch-site': 'same-site',
    # 'cache-control': 'no-cache',
    "method": "POST",
    'authority': 'mtop.damai.cn',
    'scheme': 'https',
    "accept": "application/json",
    'accept-encoding': 'gzip,deflate,br',
    "accept-language": "zh-CN,zh;q=0.9",
    "content-type": "application/x-www-form-urlencoded",
    "cookie": cookie,
    "globalcode": "ali.china.damai",
    "origin": "https://m.damai.cn",
    "pragma": "no-cache",
    "referer": "https://m.damai.cn/",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.67"
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


def build(ua, umidtoken, cookies):
    ex = {
        "channel": "damai_app", "damai": '1', "umpChannel": "100031004",
        "subChannel": "damai@damaih5_h5", "atomSplit": 1, "serviceVersion": "2.0.0",
        "customerType": "default"
    }
    d = {
        "buyNow": True, "exParams": json.dumps(ex, separators=(",", ":")),
        "buyParam": "724811045159_1_5036084393602", "dmChannel": "damai@damaih5_h5"
    }
    d = json.dumps(d, separators=(",", ":"))
    t = int(time.time() * 1000)
    sign = _get_tb_sign(TOKEN, t, d)
    url = f'https://mtop.damai.cn/h5/mtop.trade.order.build.h5/4.0/?jsv=2.7.2&appKey=12574478&t={t}&sign={sign}&type=originaljson&dataType=json&v=4.0&H5Request=true&AntiCreep=true&AntiFlood=true&api=mtop.trade.order.build.h5&method=POST&ttid=%23t%23ip%23%23_h5_2014&globalCode=ali.china.damai&tb_eagleeyex_scm_project=20190509-aone2-join-test'
    data = {'data': d, 'bx-ua': ua, 'bx-umidtoken': umidtoken}
    response = requests.post(url, data=data, headers=headers)
    print(response.request.url)
    return response.json()


def create(ua, umidtoken, data1, cookies, submitref):
    t = int(time.time() * 1000)
    print(cookies['_m_h5_tk'])
    tk = cookies['_m_h5_tk'].split('_')[0]
    sign = _get_tb_sign(TOKEN, t, data1)
    querystring = {
        "jsv": "2.7.2", "appKey": "12574478", "t": t,
        "sign": sign, "v": "4.0", "post": "1", "type": "originaljson",
        "timeout": "15000", "dataType": "json", "isSec": "1", "ecode": "1", "AntiCreep": "true",
        "ttid": "#t#ip##_h5_2014", "globalCode": "ali.china.damai",
        "tb_eagleeyex_scm_project": "20190509-aone2-join-test", "H5Request": "true",
        "api": "mtop.trade.order.create.h5", 'submitref': submitref
    }
    url = 'https://mtop.damai.cn/h5/mtop.trade.order.create.h5/4.0/?'
    data = {'data': data1, 'bx-ua': ua, 'bx-umidtoken': umidtoken}
    response = requests.post(url, data=data, headers=headers, params=querystring)
    print(response.request.url)
    print(response.json()['ret'])


async def init():
    browser = await connect(browserURL=f"http://127.0.0.1:9223")
    pages = await browser.pages()
    page = pages[0]
    # print(await page.evaluate('navigator.userAgent'))
    return page


async def get_ua_and_umidtoken(page):
    try:
        bx_ua = await page.evaluate('this.__baxia__.postFYModule.getFYToken()')
        bx_umidtoken = await page.evaluate('this.__baxia__.postFYModule.getUidToken()')
        return bx_ua, bx_umidtoken
    except ElementHandleError:
        raise ValueError('失败')


def is_wx_session():
    t = int(time.time() * 1000)
    data1 = {"source": "h5", "dmChannel": "damai@weixin_weapp"}
    data1 = json.dumps(data1, separators=(",", ":"))
    sign = _get_tb_sign(TOKEN, t, data1)
    url = f'https://mtop.damai.cn/h5/mtop.damai.wireless.user.third.session.get/1.0/?jsv=2.7.2&appKey=12574478&t={t}&sign={sign}&type=originaljson&dataType=json&v=1.0&H5Request=true&AntiCreep=true&AntiFlood=true&api=mtop.damai.wireless.user.third.session.get&tb_eagleeyex_scm_project=20190509-aone2-join-test&requestStart=1688111223107&data=%7B%22source%22%3A%22h5%22%2C%22dmChannel%22%3A%22damai%40weixin_weapp%22%7D'
    response = requests.request("POST", url, headers=headers)
    print(response.json())


async def start(page):
    api = ApiFetchPerform()
    api.update_default_config(dict(COOKIE=cookie))
    response = await api.build_order('724811045159_1_5036084393602')
    print(response["ret"])
    params = make_ticket_data(response["data"])
    response = await api.create_order(params)
    print(response["ret"])
    await api.close()

    # cookies = await page.cookies()
    # cookies = cookie_serialization(cookies)
    # a, b = await get_ua_and_umidtoken(page)
    # response = build(a, b, cookies)
    # print(response["ret"])
    #
    # submitref = response["data"]["global"]["secretValue"]
    # x, y = await get_ua_and_umidtoken(page)
    # create(x, y, make_ticket_params(response["data"]), cookies, submitref)


async def run():
    page = await init()
    await start(page)


def cookie_serialization(cookies_list):
    cookies = {}
    for cd in cookies_list:
        cookies[cd["name"]] = cd["value"]
    return cookies


if __name__ == '__main__':
    asyncio.run(run())
