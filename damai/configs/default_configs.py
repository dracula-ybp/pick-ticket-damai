"""在此项目中，某个类中只要有类属性 DEFAULT_CONFIG 当中的项都能通过此覆盖"""

# CRITICAL_WAIT: 必须设置，由于为异步任务，会造成实名人还未勾选成功，就提交订单。
# 可根据设备及网络调整
CRITICAL_WAIT = 450    # 1000=1s

# 详见damai.performer.Performance.polling
WARN_WAIT = 100

SHUTDOWN = 60 * 10    # 选票持续时间

ITEM_ID = 723122149049

# 目前得使用`2023-07-15`, 添加配置，会优化成str和int都支持选购
CONCERT = "2023-07-15"    # 场次
PRICE = "看台317元"     # 价格串
TICKET = 1       # 票量

RUN_DATE = None    # 抢票时间，为了兼容优先购，有特权或者演出无优先购可不配置，格式：202306191220

BATCH = False    # 批量功能，未启用
BATCH_WAIT = 0    # 如果开启了批量，建议这个设置一个批量 >=100

