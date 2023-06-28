import asyncio

from pyppeteer.launcher import connect

import time
import hashlib
import json

import requests

TOKEN = '6f92aab94ad95d9368dd2a6e527220f0'  # cookie中的_m_h5_tk
T = int(time.time() * 1000)
APP_KEY = '12574478'

ex = {"channel": "damai_app", "damai": "1", "umpChannel": "100031004", "subChannel": "damai@damaih5_h5", "atomSplit": 1,
      "serviceVersion": "2.0.0", "customerType": "default"}
d = {"buyNow": True,
     "exParams": json.dumps(ex, separators=(",", ":")),
     "buyParam": "724734360054_1_5032380472311", "dmChannel": "damai@damaih5_h5"}
print('d', d)
d3 = json.dumps(d, separators=(",", ":"))
print('d3', d3)

d1 = '{"buyNow":true,"exParams":"{\\"channel\\":\\"damai_app\\",\\"damai\\":\\"1\\",\\"umpChannel\\":\\"100031004\\",\\"subChannel\\":\\"damai@damaih5_h5\\",\\"atomSplit\\":1,\\"serviceVersion\\":\\"2.0.0\\",\\"customerType\\":\\"default\\"}","buyParam":"724734360054_1_5032380472311","dmChannel":"damai@damaih5_h5"}'
print('d1', d1)


def _get_tb_sign(data):
    md5 = hashlib.md5()
    w = (TOKEN + '&' + str(T) + '&' + APP_KEY + '&' + data).encode(encoding='utf-8')
    print('w', w)
    md5.update(w)
    return md5.hexdigest()


def fetch(ua, umidtoken):
    sign = _get_tb_sign(d3)
    # sign = get_sign_code(TOKEN, T, d1)
    url = f'https://mtop.damai.cn/h5/mtop.trade.order.build.h5/4.0/?jsv=2.7.2&appKey=12574478&t={T}&sign={sign}&type=originaljson&dataType=json&v=4.0&H5Request=true&AntiCreep=true&AntiFlood=true&api=mtop.trade.order.build.h5&method=POST&ttid=#t#ip##_h5_2014&globalCode=ali.china.damai&tb_eagleeyex_scm_project=20190509-aone2-join-test'
    url = f'https://mtop.damai.cn/h5/mtop.trade.order.build.h5/4.0/?jsv=2.7.2&appKey=12574478&t={T}&sign={sign}&type=originaljson&dataType=json&v=4.0&H5Request=true&AntiCreep=true&AntiFlood=true&api=mtop.trade.order.build.h5&method=POST&ttid=%23t%23ip%23%23_h5_2014&globalCode=ali.china.damai&tb_eagleeyex_scm_project=20190509-aone2-join-test'
    headers = {
        'accept': 'application/json',
        'accept-encoding': 'gzip,deflate,br',
        "content-type": "application/x-www-form-urlencoded",
        "Cookie": 'cna=eAQDHQt0azoCAXFbKVFTSzyd; t=33651982899bc5fdab89511fb23945c9; damai.cn_nickName=lktlkt; destCity=%u6DF1%u5733; _samesite_flag_=true; cookie2=1549f3660de917de9e6c52ed235e9b21; _tb_token_=e5e3e0768ee5e; xlly_s=1; _hvn_login=18; munb=2215736075515; csg=eb23d3d1; _m_h5_tk=6f92aab94ad95d9368dd2a6e527220f0_1687959472720; _m_h5_tk_enc=babf403fb0af5b42500d0732ace335b9; dm_nickname=lktlkt; usercode=230582068; havanaId=2215736075515; tfstk=dxqDcNjv6bOQQD7MMjnfDcmSr5b-lIisi5Kt6chNzbl7HfQjMfyaaRKt71_bjcVxwo3t0-IgSSUSXjEYkP4uGJuYsR6jQfPasfUAyMebhciN95jdv-6K_H6pBVy0i-msb6Cphjan-cNFximhfKBDTRXUDF0ttdcrcMEM9rlU3jyYnu-EuEwrZFT_qrucQx8y8bawfYWTqFTsuYMo90noEvC..; l=fBE4AQunNcxgFl3YBO5alurza77OBIRfGPVzaNbMiIEGa1u5tFaBLNC1p_DBSdtjgTCUbe-yTBTBzd39-9UZixDDBeAHjt4K4xvO0MP9K; isg=BCAgn9CGUP9NWOwbXFlYSrSD8SjyKQTzK7a1w5ox7DvOlcC_QjnUg_a3KzsVPrzL',
        "origin": "https://m.damai.cn",
        "referer": "https://m.damai.cn/",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
    }
    # print(ua, umidtoken)
    data = {'data': d3,
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
    pages = await browser.pages()
    page = pages[0]
    # await page.goto(
    #     "https://m.damai.cn/app/dmfe/h5-ultron-buy/index.html?buyParam=724734360054_1_5032380472311&buyNow=true&exParams=%257B%2522channel%2522%253A%2522damai_app%2522%252C%2522damai%2522%253A%25221%2522%252C%2522umpChannel%2522%253A%2522100031004%2522%252C%2522subChannel%2522%253A%2522damai%2540damaih5_h5%2522%252C%2522atomSplit%2522%253A1%257D&spm=a2o71.project.0.bottom&sqm=dianying.h5.unknown.value")
    # await asyncio.sleep(1)
    bx_ua = await page.evaluate('this.__baxia__.getFYModule.getFYToken()')
    bx_umidtoken = await page.evaluate('this.__baxia__.getFYModule.getUidToken()')
    fetch(bx_ua, bx_umidtoken)


asyncio.get_event_loop().run_until_complete(main())
