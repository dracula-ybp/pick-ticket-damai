import asyncio

from damai.orderview import OrderView
from damai.performer import Performance


async def run():
    order = OrderView()
    # 5199272746118 5199272746117
    url = order.make_order_url(714956979854, 4997413588173, 1)
    instant = Performance()
    await asyncio.create_task(instant.init_browser())
    await asyncio.create_task(instant.submit(url, instant.browser.newPage, 1))


if __name__ == '__main__':
    # asyncio.run(run())

    print('https://m.damai.cn/app/dmfe/h5-ultron-buy/index.html?exParams=%7B%22damai%22%3A%221%22%2C%22channel%22%3A%22damai_app%22%2C%22umpChannel%22%3A%2210002%22%2C%22atomSplit%22%3A%221%22%2C%22serviceVersion%22%3A%221.8.5%22%2C%22umidToken%22%3A%22T2gAYUMgPrnfJSbLEayyE4DQCYcoHDCE-W6UwE7KE5PP-YsM_b8oS8TqChLDv2PKO-w%3D%22%2C%22ua%22%3A%22140%23QpfDxJnIzzP8qzo23zOz4pN8s77r1Zfo4F9RlVm1Mc0Ijs7fSqTb724iAIOnY7LbUVM466hqzzns0E4Dzb%2BzzZDgba7qlQzx2DD3VthqzFd22XU%2BllfzzPziVW1cug8I1wba7X53z9nViy4koztFPiunGokMqV7GIQeAWXgP7QNQsldW2TF1EQC1DK1UFc780KJpHFBSyTaFd9DyptCxrA%2FWezFb0VTiz%2BFIc7Hxkqj%2BeiYc6u6EcoTSXbHJ%2Figug9k1jGHu0WjttHT4XIFMLweT9WAO6S21hJQWahGged3il28eI0zEDr47auQrYWTugruTrGMuK6C7bab3i4ZC2THpdAuW9%2BoIVaqUYqeHZMpxiDQlW4iFT3rOrM6EesISn7C0uS5%2FiAaqh6RaUabLxFFKLoztLOK68lIaAiwQRG0sAOg2xObig5b%2F4O6DnUSM8%2FE6n1YIL8TqalQONnkwDD2%2Bg%2BbG4cAhdvaJJcvjip%2Fh%2F0Fzp4YCjveyPIxNr6YPEC1aB5pPdc0Tm7JsaQrPHj%2FbOk2Y4TboabNUnvAmP0UCKH6BatOBpekjs7BwLdlD1C3vY1yVvGkw%2FJvO4X61pBUhp%2FHeQLYzvVBN8iXLgV5ETcGy6UQwFWqYDGLPZLiON7YtES7HWGcB0uZoyQT4XiR2zwPnKq5eUHO8n3ehVMHwni%2FLczo8TYa1mzI2U0zZ0DZvG7FpVOg95KzNxxA8JpopFNwm4eu8xbC4JvX7zojn42Reo7wl%2FO7AMFrvmQVlleoesCmh1oLTUPGBGCnIWB1XX9SfECX4TJxAP0a6RQwOBVUwsQ43V7oQBKj80AnbcFDw8jMsxghEomaeRqMIOFZLiPnBH8mLCCcfzsZVNmUKTYZSODnEJdCUkJTzqMS7QCbxWdNUU5MmLlMUbHoKIQbWmJxl48yqMoKMIY3%2FJZglzLn07X18gAv9uaE9rp7Mw%2BIomLYVdOGGNFSZ6EHdEi9daprmC%2BXkidgQxn7xa4Eb1ZGpzZ1FZWGg1K%2BPcn40rzaB91XMxMaIWtroCEw%2FZBxj0b%3D%3D%22%7D&buyParam=720545258599_1_5016701340284&buyNow=true&privilegeActId=')
    print('https://m.damai.cn/app/dmfe/h5-ultron-buy/index.html?exParams=%7B%22damai%22%3A%221%22%2C%22channel%22%3A%22damai_app%22%2C%22umpChannel%22%3A%2210002%22%2C%22atomSplit%22%3A%221%22%2C%22serviceVersion%22%3A%221.8.5%22%2C%22umidToken%22%3A%22T2gAHw1r7GAtavV8IfjbKjRrT1rvfLMQ48dzsVbvL5DaslK-_6k4LN-rSYGh0CSCSnQ%3D%22%2C%22ua%22%3A%22140%23/gToG6jwzzPW0Qo23zaF4pN8s77oMNzqYasU/fwSuYnIM0j%2ByKXl%2BxzVamhb/QGm0VQ4q3hqzznsQqOTm81zzjVw9jWqlbrz2DD3V3gqzPMi228%2BtCfxzDrb3z//EHmijDapVrMn79/QCGKQA44d/Q72lQpGncnlAH7CFZW0NXrrU%2BPf3rxaT9V7hPScGL/mXpZ2TNzCIiZGmqCJ6K1js3sKL7hjEtzuFJ3efCvfvQfujhx9AqKwuzlbXMDnKxyKLzz%2BbQiXrJTsTSUuZ3vc%2B74mCg2QC%2BzDfEnuvRCx4fyHXxp4/SFBZYKzzN/CftLj/6nQuum1CrbmvXdCl1mpcNb5T4X6co5mvjtc2DiTxsRtYzvV1iXZJLCSYepRGXvREkcRjxxUYjmQxvp8%2BdCWovPkyuBBecwiWA2kpemwVC1Jx%2BXRijpgmLhhfp2y9fdIgqWfNBAvGWUjtdx/QfdfmHsxRmQMcsGug/%2ByP8KPO4iDLO2WrdSbxNC8oan9EiiKElmIAG3kMa0tNAe97EN8lRVMJfbxw3yAbioeYstliCL1HiPoY/gZlq4znnf7Otqka9e%2BRuD2%2BjhdYw7h3avO8cj2nkaSkWMAYlVevysOLdezDQDTFOaEz485eFr%2B0lsydSRDJjKYvVSUQvREJM4thg%2BgK08yUTyM3PjdG1Lz2LKYuckpR96BtncMN4kUxmJ2DSwASy4%2BVgWOSMLxJc3Cwgd7VR5PuTqgDNZ116bb0FRFto1%2BMdnyVCbk5P4p23TpG5AK3mpEhsuWGfNPkV/o7VbL%2B6jSFfm7vhqAeIHJNNKvjYM/6sIDYVL8wK/69fKcoMeZXT6ExOy3V87d64XT/jcISDT//F08V3vMTlC3jwc91EHy5R2ugb/X8wZ/a3tQTTquQvhLG7OKmw2RKU35nWdCaEJEt3FPgkrOHRPb14bi9F%3D%3D%22%7D&buyParam=714956979854_1_5199272746119&buyNow=true&privilegeActId=')
    print()
