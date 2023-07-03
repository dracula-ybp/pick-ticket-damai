import hashlib
import json
import time


def make_ticket_params(order_build_data):
    params = {}
    data_field = ['dmContactName', 'dmContactEmail', 'dmContactPhone', 'dmViewer',
                  'dmDeliverySelectCard', 'dmDeliveryAddress', 'dmPayType',
                  'confirmOrder_1', 'dmEttributesHiddenBlock_DmAttributesBlock', 'item']
    data = order_build_data["data"]
    data_dict = {key: data[key] for field in data_field for key in data.keys() if
                 field == key or field == key.split('_')[0]}

    viewer = next(key for key in data_dict.keys() if key.split('_')[0] == "dmViewer")
    data_dict[viewer]["fields"]["selectedNum"] = 1
    data_dict[viewer]["fields"]["viewerList"][1]["isUsed"] = True
    params['data'] = dumps(data_dict).replace('"true"', 'true')

    linkage = order_build_data["linkage"]
    linkage_dict = {field: linkage[field] for field in ['common', 'signature']}
    linkage_dict['common'].pop('queryParams', None)
    linkage_dict['common'].pop('structures', None)
    params['linkage'] = dumps(linkage_dict)

    hierarchy = order_build_data["hierarchy"]
    hierarchy_dict = {field: hierarchy[field] for field in ['structure']}
    params['hierarchy'] = dumps(hierarchy_dict)

    feature = dumps(
        {"subChannel": "damai@damaih5_h5",
         "returnUrl": "https://m.damai.cn/damai/pay-success/index.html?spm=a2o71.orderconfirm.bottom.dconfirm&sqm=dianying.h5.unknown.value",
         "serviceVersion": "2.0.0", "dataTags": "sqm:dianying.h5.unknown.value"
         }
    )

    return dumps({"params": dumps(params), "feature": feature})


def dumps(obj):
    return json.dumps(obj, separators=(",", ":"), ensure_ascii=False)


def get_sign(token, t, app_key, data):
    md5 = hashlib.md5()
    md5.update((token + '&' + str(t) + '&' + str(app_key) + '&' + data).encode('utf-8'))
    return md5.hexdigest()


def timestamp():
    return int(time.time() * 1000)
