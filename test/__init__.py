# async def place_order1(self, url, page, ticket_num: int = 1):
#     """选取实名观影人，提交订单"""
#     page: Page = await page() if callable(page) else await page
#     # 第一个while True点击太快会触发网络拥堵，可以手动刷新，确保任务不被结束。
#     while True:
#         await asyncio.wait([page.goto(url), page.waitForNavigation()])
#         try:
#             await page.waitForSelector('i.iconfont', timeout=3000)
#         except TimeoutError:
#             title = await page.title()
#             # 本次抢票未登录，重新登录抢票没啥戏了，直接结束
#             if title == "登录":
#                 return
#             continue
#
#         # 选择观影人
#         items = await page.querySelectorAll('i.iconfont')
#         for num in range(0, ticket_num):
#             await items[num].click()
#         await page.waitFor(500)
#
#         items = await page.querySelectorAll('#dmOrderSubmitBlock_DmOrderSubmitBlock div[view-name=TextView]')
#
#         while True:
#             try:
#                 # 提交订单
#                 await items[-1].click()
#                 await page.waitFor(500)
#             except Exception:
#                 break
#
#             # 抢票成功
#             if await page.title() in {"payment", "支付宝付款"}:
#                 print('抢票成功')
#                 await page.goto('https://orders.damai.cn/orderList')
#                 return
#
#             # 此处可能会出现库存不足，有订单未支付等。目前先这样设计，可能有回流票。
#             confirm_content = await page.querySelectorAll('#confirmContent')
#             if confirm_content:
#                 text = await (await confirm_content[0].getProperty('textContent')).jsonValue()
#                 # 抢票成功，有未支付订单提示
#                 if "未支付订单" in text:
#                     print('抢票成功')
#                     await page.goto('https://orders.damai.cn/orderList')
#                     return
#                 cancel = await page.xpath('//div[@id="confirmContent"]/../following-sibling::div/div[1]')
#                 await cancel[0].click()
#
#                 # 网络拥堵，网络重试div
#                 await page.waitFor(400)
#                 if await page.querySelectorAll('.bannar'):
#                     break
