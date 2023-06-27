# pick-ticket-damai
大麦捡漏/pyppeteer

### pyppeteer模拟购票，直接请求不会解决bx-ua

- 配置：下载谷歌浏览器，安装后在浏览器地址栏输入`chrome://version`复制"可执行文件路径"，终端启动浏览器并登录：
  ```shell
  C:\Users\chrome.exe --remote-debugging-port=9222 --user-data-dir="D:\Test"
  可执行文件路径                             默认端口                自定义文件
  ```
- 选票：可在项目(damai)同级或用户根目录添加"config.yaml", 详解见damai.configs.default_configs.py
- 运行：python run.py

### ps
- 在项目包__init__.py有些注解。
- 提前登录, 提前在大麦app中添加观影人及收货地址电话。
- 开抢前几分钟找个售票中演出，点击到订单页面一直刷新把滑动验证码先刷出来并划过
