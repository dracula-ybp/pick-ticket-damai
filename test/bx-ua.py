import asyncio
import sys
import time
from typing import Optional
import execjs

from pyppeteer.launcher import connect

import random
import time
import hashlib
import json

import requests

TOKEN = '61a1292c4e5bc0171542748ad422e8a2'  # cookie中的_m_h5_tk
T = int(time.time() * 1000)
APP_KEY = '12574478'

ex = {"channel": "damai_app", "damai": 1, "umpChannel": 100031004, "subChannel": "damai@damaih5_h5", "atomSplit": 1,
      "serviceVersion": "2.0.0", "customerType": "default"}
d = {"buyNow": True,
     "exParams": ex,
     "buyParam": "724734360054_1_5032380472311", "dmChannel": "damai@damaih5_h5"}
d3 = json.dumps(d, separators=(",", ":"))

d1 = '{"buyNow":true,"exParams":"{\\"channel\\":\\"damai_app\\",\\"damai\\":\\"1\\",\\"umpChannel\\":\\"100031004\\",\\"subChannel\\":\\"damai@damaih5_h5\\",\\"atomSplit\\":1,\\"serviceVersion\\":\\"2.0.0\\",\\"customerType\\":\\"default\\"}","buyParam":"724734360054_1_5032380472311","dmChannel":"damai@damaih5_h5"}'
print(d1)
print(T)


def _get_tb_sign(data):
    md5 = hashlib.md5()
    w = (TOKEN + '&' + str(T) + '&' + APP_KEY + '&' + data).encode(encoding='utf-8')
    print('w', w)
    md5.update(w)
    return md5.hexdigest()


def get_sign_code(h5_token: str, time_stamp, api_param) -> str:
    """
    返回请求选座信息接口必备的sign信息

    :return:
    """
    node = execjs.get()
    with open(r"C:\Users\lkt\Desktop\signcode.js", 'r', encoding='utf-8') as f:
        js_file = f.read()
    js_exec = node.compile(js_file)
    param1 = '{}&{}&12574478&'.format(h5_token, time_stamp)

    context = param1 + api_param
    sign_code = js_exec.call('calcaulate', context)
    return sign_code


def fetch(ua, umidtoken):
    sign = _get_tb_sign(d1)
    # sign = get_sign_code(TOKEN, T, d1)
    url = f'https://mtop.damai.cn/h5/mtop.trade.order.build.h5/4.0/?jsv=2.7.2&appKey=12574478&t={T}&sign' \
          f'={sign}f&type=originaljson&dataType=json&v=4.0&H5Request=true&AntiCreep=true' \
          f'&AntiFlood=true&api=mtop.trade.order.build.h5&method=POST&ttid=%23t%23ip%23%23_h5_2014&globalCode=ali' \
          f'.china.damai&tb_eagleeyex_scm_project=20190509-aone2-join-test'
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "Cookie": 't=f9f110457b5bc27c1579f4ce6ed5a18d; cna=X9YWHbUe6kACAduG3XxFaYhw; munb=2216041624308; xlly_s=1; _samesite_flag_=true; cookie2=1aa0453f888981f35178fdf44a0fb119; _tb_token_=49737ea6e718; _hvn_login=18; csg=439ffa1d; l=fBrrSI9RNmppqr2KBO5ahurza77OfQAf5OVzaNbMiIEGa6NRtES8GNC1Ila9SdtjgTfvmexrip0J_dFk-ozLROkDBeYBerBEMc99-iQWnr1..; tfstk=d-G9DXgV5HxihcLvslpHg5yFoNTHEf3w9cu5ioqGhDnKjqTNslVmD-gzxjYZSdRxpmi3fRDioInnYDoiSq0fkri31-kgmlqYMqoJ-3AkZVuag-tkqQ4XSaNvNe4jW40t7SPXqdrZP83Z4dzlKGBDdUJOM1EZZP9b206FWr7-WRESJL5cgnzdqk3_fs1b1rXaXbcJESIu2rX9JeBV3RaEgNv3z; usercode=244681378; dm_nickname=%E9%BA%A6%E5%AD%904Y1dD; havanaId=2216041624308; _m_h5_tk=61a1292c4e5bc0171542748ad422e8a2_1687951625761; _m_h5_tk_enc=8f26c8d63e73120785d84c64f28c23fd; isg=BMnJJL-ryeNsL7WGUpel3Y4k2PUjFr1IWdbCdWs-RbDvsunEs2bNGLcz9hYE0FWA',
        "globalcode": "ali.china.damai",
        "origin": "https://m.damai.cn",
        "pragma": "no-cache",
        "referer": "https://m.damai.cn/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
    }
    # print(ua, umidtoken)
    data = {'data': d1,
            'bx-ua': ua,
            'bx-umidtoken': umidtoken
            }

    response = requests.request("POST", url, data=data, headers=headers)
    print(response.request.url)
    print(response.request.body)

    print(response.text)
    # print(json.dumps(d, separators=(",", ":")))


async def main():
    browser = await connect(
        browserURL=f"http://127.0.0.1:9222")
    page = await browser.newPage()
    await page.goto(
        "https://m.damai.cn/app/dmfe/h5-ultron-buy/index.html?buyParam=724734360054_1_5032380472311&buyNow=true&exParams=%257B%2522channel%2522%253A%2522damai_app%2522%252C%2522damai%2522%253A%25221%2522%252C%2522umpChannel%2522%253A%2522100031004%2522%252C%2522subChannel%2522%253A%2522damai%2540damaih5_h5%2522%252C%2522atomSplit%2522%253A1%257D&spm=a2o71.project.0.bottom&sqm=dianying.h5.unknown.value")
    await asyncio.sleep(1)
    bx_ua = await page.evaluate('window.__baxia__.getFYModule.getFYToken()')
    bx_umidtoken = await page.evaluate('window.__baxia__.getFYModule.getUidToken()')
    fetch(bx_ua, bx_umidtoken)


asyncio.get_event_loop().run_until_complete(main())
