import time
from collections import Counter

counter = Counter()


data = ["库存不足", "库存不足", "库存不足", "库存不足", "哎呦喂，挤爆", "挤爆", "挤爆", "过期"]
for d in data:
    counter.update([d])
print(counter)


s = all(counter.get(i, 0) < 5 for i in ('挤爆', '库存不足'))
print(s)
