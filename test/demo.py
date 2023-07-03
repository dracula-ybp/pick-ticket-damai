import asyncio
from pyppeteer import connect


async def main():
    browser = await connect(browserURL=f"http://127.0.0.1:9223")
    pages = await browser.pages()
    page = pages[0]

    # 执行自定义的JavaScript代码，发送POST请求
    resp = await page.evaluate('''
    fetch('https://mtop.damai.cn/h5/mtop.trade.order.build.h5/4.0/?jsv=2.7.2&appKey=12574478&t=1688371001404&sign=ab66592dbbc519c615774e20321efe05&type=originaljson&dataType=json&v=4.0&H5Request=true&AntiCreep=true&AntiFlood=true&api=mtop.trade.order.build.h5&method=POST&ttid=%23t%23ip%23%23_h5_2014&globalCode=ali.china.damai&tb_eagleeyex_scm_project=20190509-aone2-join-test&requestStart=1688371001402', {
        method: 'POST',
        headers: {
        },
    });
    ''')
    print(resp)
    # await browser.close()

asyncio.get_event_loop().run_until_complete(main())