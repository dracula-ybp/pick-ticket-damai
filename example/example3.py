import asyncio

from damai.performer import Performance


async def main():
    url = 'https://m.damai.cn/app/dmfe/h5-ultron-buy/index.html?exParams=%7B%22damai%22%3A%221%22%2C%22channel%22' \
          '%3A%22damai_app%22%2C%22umpChannel%22%3A%2210002%22%2C%22atomSplit%22%3A%221%22%2C%22serviceVersion%22' \
          '%3A%221.8.5%22%2C%22umidToken%22%3A%22T2gAHw1r7GAtavV8IfjbKjRrT1rvfLMQ48dzsVbvL5DaslK-_6k4LN' \
          '-rSYGh0CSCSnQ%3D%22%2C%22ua%22%3A%22140%23/gToG6jwzzPW0Qo23zaF4pN8s77oMNzqYasU/fwSuYnIM0j%2ByKXl' \
          '%2BxzVamhb/QGm0VQ4q3hqzznsQqOTm81zzjVw9jWqlbrz2DD3V3gqzPMi228%2BtCfxzDrb3z//EHmijDapVrMn79/QCGKQA44d' \
          '/Q72lQpGncnlAH7CFZW0NXrrU%2BPf3rxaT9V7hPScGL' \
          '/mXpZ2TNzCIiZGmqCJ6K1js3sKL7hjEtzuFJ3efCvfvQfujhx9AqKwuzlbXMDnKxyKLzz%2BbQiXrJTsTSUuZ3vc%2B74mCg2QC' \
          '%2BzDfEnuvRCx4fyHXxp4/SFBZYKzzN/CftLj' \
          '/6nQuum1CrbmvXdCl1mpcNb5T4X6co5mvjtc2DiTxsRtYzvV1iXZJLCSYepRGXvREkcRjxxUYjmQxvp8' \
          '%2BdCWovPkyuBBecwiWA2kpemwVC1Jx%2BXRijpgmLhhfp2y9fdIgqWfNBAvGWUjtdx/QfdfmHsxRmQMcsGug' \
          '/%2ByP8KPO4iDLO2WrdSbxNC8oan9EiiKElmIAG3kMa0tNAe97EN8lRVMJfbxw3yAbioeYstliCL1HiPoY/gZlq4znnf7Otqka9e' \
          '%2BRuD2%2BjhdYw7h3avO8cj2nkaSkWMAYlVevysOLdezDQDTFOaEz485eFr%2B0lsydSRDJjKYvVSUQvREJM4thg' \
          '%2BgK08yUTyM3PjdG1Lz2LKYuckpR96BtncMN4kUxmJ2DSwASy4%2BVgWOSMLxJc3Cwgd7VR5PuTqgDNZ116bb0FRFto1' \
          '%2BMdnyVCbk5P4p23TpG5AK3mpEhsuWGfNPkV/o7VbL%2B6jSFfm7vhqAeIHJNNKvjYM/6sIDYVL8wK' \
          '/69fKcoMeZXT6ExOy3V87d64XT/jcISDT//F08V3vMTlC3jwc91EHy5R2ugb/X8wZ' \
          '/a3tQTTquQvhLG7OKmw2RKU35nWdCaEJEt3FPgkrOHRPb14bi9F%3D%3D%22%7D&buyParam=714956979854_1_5199272746116' \
          '&buyNow=true&privilegeActId='
    # url = 'https://m.damai.cn/app/dmfe/h5-ultron-buy/index.html?buyParam=714956979854_1_5199272746116&buyNow=true&exParams=%257B%2522channel%2522%253A%2522damai_app%2522%252C%2522damai%2522%253A%25221%2522%252C%2522umpChannel%2522%253A%2522100031004%2522%252C%2522subChannel%2522%253A%2522damai%2540damaih5_h5%2522%252C%2522atomSplit%2522%253A1%257D&spm=a2o71.project.0.bottom&sqm=dianying.h5.unknown.value'
    instant = Performance()
    await asyncio.create_task(instant.init_browser())
    tasks = [instant.submit(url, instant.browser.newPage, 1)]
    await asyncio.wait(tasks)


asyncio.run(main())
