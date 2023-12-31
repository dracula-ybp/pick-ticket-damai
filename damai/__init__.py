"""
仅供参考，学习。不得不经同意转载。

前提，使用谷歌浏览器或Edge，然后使用浏览器远程调试功能？"
谷歌一下" pyppeteer connect browserWSEndpoint 或者 pyppeteer connect browserURL
示例代码：examples timing.py

H5很多演出已经被禁用，部分必须使用app才能购票的。但是微信小程序支持的演出比
在浏览器中支持的又要多。如果演出在小程序中可以抢票，可以在代码中指定UserAgent,
但是cookie必须是从微信登录的，所以还要添加cookie。
抓包实测，直接调接口也是这个思路

默认使用api购票，可配置`PERFORM`。可自行实现，继承`Perform`,按submit签名
'damai.performer.ApiFetchPerform'
'damai.performer.WebDriverPerform'

WebDriver：
    抢是抢不过直接发请求的，但也不是不能用，主要捡漏。如果是第一次放票应该能捡回流票，
    要是抢的是退票那基本抢不到。

    不知道是不是分批放票。每次捡漏成功，创建订单的时间也是在开票将近20s了，也有2s创建成功的。
    薛之谦深圳场17s创建订单，那么多人估计17s已经无了吧。所以不能直接发请求就用傻点的方法，
    还能处理滑动验证码问题，开票前几分钟随便找个演出点击到订单界面使劲刷新验证码就把验证码滑了，
    后续程序中基本不会出现。

    实测中提交订单并不是疯狂发请求过去，能抢成功基本点击两次就可以了。出现提示框再刷新。
    最近几天的演唱会中几十万想看的基本都捡票成功。

Api：
    **必须配置Cookie

    提前运行程序，调度器准时发送请求，超过抢票时间则直接捡票。但是还是得依赖浏览器。

    开抢会无延迟默认抢两次(可自行配置)，后面请求会加延迟，进入捡票，太频繁会出现验证码。
    可能得加毫秒延迟，测试中第一次导致了生成订单失败(调度器开启生成订单，商品已过期，过快导致了)。

Python3.7.5写的
"""


from damai.engine import ExecutionEngine
from damai.runner import Runner
