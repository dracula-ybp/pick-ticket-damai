import hashlib
import json
import time


def make_ticket_params(order_build_data):
    print('=============')
    params = {}
    data_field = ['dmViewer', 'dmContactName', 'dmContactEmail', 'dmContactPhone',
                  'dmDeliverySelectCard', 'dmDeliveryAddress', 'dmPayType', 'item',
                  'confirmOrder_1', 'dmEttributesHiddenBlock_DmAttributesBlock']
    data = order_build_data["data"]
    data_dict = {key: data[key] for field in data_field for key in data.keys() if
                 field == key or field == key.split('_')[0]}

    viewer = next(key for key in data_dict.keys() if key.split('_')[0] == "dmViewer")
    data_dict[viewer]["fields"]["selectedNum"] = 1
    data_dict[viewer]["fields"]["viewerList"][0]["isUsed"] = True
    params['data'] = dumps(data_dict)

    linkage = order_build_data["linkage"]
    linkage_dict = {field: linkage[field] for field in ['common', 'signature']}
    params['linkage'] = dumps(linkage_dict)

    hierarchy = order_build_data["hierarchy"]
    hierarchy_dict = {field: hierarchy[field] for field in ['structure']}
    params['hierarchy'] = dumps(hierarchy_dict)

    feature = dumps({"subChannel": "damai@damaih5_h5",
                     "returnUrl": "https://m.damai.cn/damai/pay-success/index.html?spm=a2o71.orderconfirm.bottom.dconfirm&sqm=dianying.h5.unknown.value",
                     "serviceVersion": "2.0.0", "dataTags": "sqm:dianying.h5.unknown.value"})

    # feature = dumps({"feature":
    #      {"subChannel": "damai@weixin_weapp",
    #       "returnUrl": "https://m.damai.cn/damai/pay-success/index.html?spm=a2o71.orderconfirm.bottom.dconfirm&uid=230582068&token=oetgX0fAni2i5gND44TBFth8LX48&pc_i=wx23c87fe0-5926-449f-a446-6d2332f9d389&pu_i=230582068&scene_id=1001&citysite_id=440300&sqm=undefined",
    #       "serviceVersion": "2.0.0", "wxOpenId": "oetgX0fAni2i5gND44TBFth8LX48"}})

    return dumps({"params": dumps(params), "feature": feature})


def dumps(obj):
    return json.dumps(obj, separators=(",", ":"), ensure_ascii=False)


def get_sign(token, t, app_key, data):
    md5 = hashlib.md5()
    md5.update((token + '&' + str(t) + '&' + str(app_key) + '&' + data).encode('utf-8'))
    return md5.hexdigest()


def timestamp():
    return int(time.time() * 1000)
