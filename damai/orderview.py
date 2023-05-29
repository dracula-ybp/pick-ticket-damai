import json
import time

from urllib import parse

import requests

PREFIX = {
    "damai": "1", "channel": "damai_app", "umpChannel": "10002",
    "atomSplit": "1", "serviceVersion": "1.8.5"
}
UMIDTOKEN = "T2gAHw1r7GAtavV8IfjbKjRrT1rvfLMQ48dzsVbvL5DaslK-_6k4LN-rSYGh0CSCSnQ="
UA = ("140#/gToG6jwzzPW0Qo23zaF4pN8s77oMNzqYasU/fwSuYnIM0j+yKXl+xzVamhb/QGm0VQ4q3hq"
      "zznsQqOTm81zzjVw9jWqlbrz2DD3V3gqzPMi228+tCfxzDrb3z//EHmijDapVrMn79/QCGKQA44d/"
      "Q72lQpGncnlAH7CFZW0NXrrU+Pf3rxaT9V7hPScGL/mXpZ2TNzCIiZGmqCJ6K1js3sKL7hjEtzuFJ3"
      "efCvfvQfujhx9AqKwuzlbXMDnKxyKLzz+bQiXrJTsTSUuZ3vc+74mCg2QC+zDfEnuvRCx4fyHXxp4/"
      "SFBZYKzzN/CftLj/6nQuum1CrbmvXdCl1mpcNb5T4X6co5mvjtc2DiTxsRtYzvV1iXZJLCSYepRGXvR"
      "EkcRjxxUYjmQxvp8+dCWovPkyuBBecwiWA2kpemwVC1Jx+XRijpgmLhhfp2y9fdIgqWfNBAvGWUjtdx/"
      "QfdfmHsxRmQMcsGug/+yP8KPO4iDLO2WrdSbxNC8oan9EiiKElmIAG3kMa0tNAe97EN8lRVMJfbxw3yA"
      "bioeYstliCL1HiPoY/gZlq4znnf7Otqka9e+RuD2+jhdYw7h3avO8cj2nkaSkWMAYlVevysOLdezDQDTF"
      "OaEz485eFr+0lsydSRDJjKYvVSUQvREJM4thg+gK08yUTyM3PjdG1Lz2LKYuckpR96BtncMN4kUxmJ2DSw"
      "ASy4+VgWOSMLxJc3Cwgd7VR5PuTqgDNZ116bb0FRFto1+MdnyVCbk5P4p23TpG5AK3mpEhsuWGfNPkV/o7V"
      "bL+6jSFfm7vhqAeIHJNNKvjYM/6sIDYVL8wK/69fKcoMeZXT6ExOy3V87d64XT/jcISDT//F08V3vMTlC3jw"
      "c91EHy5R2ugb/X8wZ/a3tQTTquQvhLG7OKmw2RKU35nWdCaEJEt3FPgkrOHRPb14bi9F==")


class OrderView:
    """生成演出订单url"""

    def __init__(self):
        self._views = {}
        self.url = ("https://detail.damai.cn/subpage?itemId={}&apiVersion=2.0"
                    "&dmChannel=pc@damai_pc&bizCode=ali.china.damai&scenario=itemsku"
                    "&dataType=&dataId={}&privilegeActId=&callback=__jp0")
        self.headers = {
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh,en-US;q=0.9,en;q=0.8,zh-CN;q=0.7",
            "cache-control": "no-cache",
            "pragma": "no-cache",
            "referer": "https://search.damai.cn/search.htm",
            "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                           " (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36")
        }

    @property
    def views(self):
        return self._views

    def get_calendar(self, id_):
        data = self._make_perform_request(id_)
        calendar = data.get("performCalendar", {}).get("performViews", [])
        return [
            dict(performId=view.get("performId"), performName=view.get("performName"))
            for view in calendar
        ]

    def get_sku_list(self, id_, perform_id=''):
        data = self._make_perform_request(id_, perform_id)
        perform = data.get("perform", {})
        sku_list = perform.get("skuList", [])
        return [
            dict(itemId=sku.get("itemId"), skuId=sku.get("skuId"),
                 priceName=sku.get("priceName"), price=sku.get("price"),
                 performName=perform.get("performName"),
                 performBeginDTStr=perform.get("performBeginDTStr"),
                 )
            for sku in sku_list
        ]

    def _make_perform_request(self, id_, perform_id=''):
        response = requests.get(self.url.format(id_, perform_id), headers=self.headers)
        response.raise_for_status()
        data = json.loads(response.text.replace("__jp0(", "").strip(')'))
        return data

    def add(self, id_, alias=None):
        views = []
        for calendar in self.get_calendar(id_):
            views.append(self.get_sku_list(id_, calendar["performId"]))
            time.sleep(0.5)
        self._views[alias or id_] = views

    @staticmethod
    def make_order_url(id_, sku_id, num_tickets):
        url = "https://m.damai.cn/app/dmfe/h5-ultron-buy/index.html?"
        ex_params = {**PREFIX, 'umidToken': UMIDTOKEN, 'ua': UA}
        ex_params_str = "exParams=" + parse.quote(json.dumps(ex_params, separators=(",", ":")))
        buy_param = f'{id_}_{num_tickets}_{sku_id}'
        params = {'buyParam': buy_param, 'buyNow': "true", 'privilegeActId': ""}
        return f'{url}{ex_params_str}&{parse.urlencode(params)}'


