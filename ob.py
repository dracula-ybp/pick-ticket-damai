a = [{
    "2023-06-21": [
        {
            "itemId": "719062769469",
            "skuId": "5183936506985",
            "priceName": "317元看台",
            "price": "317.00"
        },
        {
            "itemId": "719062769469",
            "skuId": "5183936506986",
            "priceName": "517元看台",
            "price": "517.00"
        },
    ]
}]


class Storage:

    def __init__(self, data):
        self.data = data

    def __getitem__(self, value):
        if isinstance(value, int):
            return self.data[list(self.data.keys())[value]]
        elif isinstance(value, str):
            return self.data[value]


s = Storage(a)
print(s[1])
print(s["2023-06-21"])