"""暂时不要使用，正在更新接口请求，会报错，修改后会尽量按之前的签名"""

import asyncio
import json
import threading
import tkinter as tk
from datetime import datetime
from tkinter import ttk, simpledialog
from tkinter import messagebox

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.date import DateTrigger

from damai.engine import ExecutionEngine
from gui.utils import check_config, config_path, command_chrome
from config import PROMPT


class App(tk.Tk):

    def __init__(self, *args, **kwargs):
        self.server = ExecutionEngine()
        self.scheduler = AsyncIOSchedulerTask()
        asyncio.run_coroutine_threadsafe(self.server.perform.init_browser(), self.scheduler.loop)
        super().__init__(*args, **kwargs)
        self.title('App')
        self.geometry('1100x650')
        self.main_frame = tk.Frame(self, bg="#f9f9f9")
        self.navigation()
        self.main_frame.pack(side='right', fill='both', expand=True)

        entry = tk.Entry(self.main_frame, width=45)
        entry.insert(0, '浏览器下载地址：https://www.google.cn/intl/zh-CN/chrome/')
        entry.configure(state="readonly")
        entry.pack(side="top", pady=30)
        ttk.Button(self.main_frame, text="启动/配置谷歌浏览器", command=self.allocation_browser,
                   style='RoundedButton.TButton').pack(side="top", pady=30, expand=True)

    def navigation(self):
        """侧边导航栏"""
        table = dict(
            抢票须知=self.need_to_know, 选票=self.choose_ticket, 任务视图=self.show_tasks,
            启动谷歌浏览器=self.allocation_browser
        )
        sidebar = tk.Frame(self, bg='#f4f4f4', width=100, height=self.winfo_screenheight())
        style = ttk.Style()
        style.configure("RoundedButton.TButton", relief="flat",
                        borderwidth=0, foreground="#323232", font=("黑体", 15))
        style.map("RoundedButton.TButton", background=[("active", "#fafcfd")], foreground=[("active", "#ff4867")])

        def button(func, text):
            btn = ttk.Button(sidebar, text=text, command=func, style='RoundedButton.TButton')
            btn.pack(pady=(30, 0), fill='x', padx=10)

        for k, v in table.items():
            button(v, k)
        sidebar.pack(side='left', fill='y')

    def allocation_browser(self):
        check_config()
        with open(config_path, 'r', encoding='utf-8') as f:
            data = json.loads(f.read())
        chrome_exe_path = data.get("chrome_exe_path")
        if not chrome_exe_path:
            chrome_exe_path = simpledialog.askstring("Input", prompt='输入本机chrome.exe路径',
                                                     parent=self.main_frame, )
            data['chrome_exe_path'] = chrome_exe_path
            with open(config_path, 'w') as f:
                json.dump(data, f)
        try:
            command_chrome(chrome_exe_path)
            messagebox.showinfo(message="Chrome已经打开，记得登陆帐号！")
        except FileNotFoundError:
            messagebox.showerror(message="Chrome无效，可再次输入！")

    def need_to_know(self):
        """显示抢票须知"""
        self.destroy()
        lbl = ttk.Label(self.main_frame, text=PROMPT, font=('方正姚体', 15))
        lbl.pack(fill='both', expand=True)

    def choose_ticket(self):
        self.destroy()
        search = tk.Frame(self.main_frame, height=10, bg="#e5e5e5", pady=10, padx=5)
        search.pack(side="top", pady=20)
        tk.Label(search, text="演出ID:", font=('楷体', 13), bg="#e5e5e5").pack(side="left")
        entry = tk.Entry(search, font=('方正姚体', 11))
        entry.pack(side="left")
        tk.Button(search, text="搜索", font=('楷体', 10), bg="#ffecef", command=lambda: self.show_menu(entry)).pack(
            side="left", padx=10)

        tk.Button(self.main_frame, text="创建任务", font=('楷体', 10), bg="#ffecef",
                  command=lambda: self.create_task(task_ent, entry)).pack(side="right", padx=10, pady=40)
        task_ent = tk.Entry(self.main_frame, width=13, font=('方正姚体', 11))
        task_ent.pack(side="right", pady=40)
        tk.Label(self.main_frame, text="开抢时间", font=('楷体', 13)).pack(side="right", pady=40)

        self.log_text = tk.Text(self.main_frame, height=10, font=('方正姚体', 10))
        self.log_text.pack(side='bottom', fill='x', padx=20, pady=20)

    def show_menu(self, entry):
        # 721216860314
        # 202306021055
        _id = entry.get()
        if not is_integer(_id):
            messagebox.showerror(message='演出ID错误')
            return
        if hasattr(self, 'menu'):
            self.menu.destroy()

        self.log_text.insert(tk.END, f'id:{_id},演出信息加载中...\n')
        self.server.order.add(_id)
        self.menu = tk.Frame(self.main_frame, width=600, height=350, bg='#fafafa')
        self.menu.pack(padx=20, pady=20, expand=True, fill='both')

        date_frame = tk.Frame(self.menu, bg="#f9f9f9")
        tk.Label(date_frame, text="场次", font=('楷体', 13), bg='#f4f4f4', foreground="#ff4867", width=7,
                 height=1).pack(
            side="left", padx=10, pady=10)

        def show_ticket(obj):
            value = obj.date_rg.var.get()
            for widget in ticket_frame.winfo_children():
                widget.destroy()

            for widget in combobox_frame.winfo_children():
                widget.destroy()

            tk.Label(ticket_frame, text="票档", font=('楷体', 13), bg='#f4f4f4', foreground="#ff4867", width=7,
                     height=1).pack(
                side="left", padx=10, pady=10)
            obj.ticket_rg = RadioGroup(ticket_frame,
                                       [f'{sku["priceName"]}/{sku["price"]}' for sku in data[value]["skuList"]])

            tk.Label(combobox_frame, text="数量", font=('楷体', 13), bg='#f4f4f4', foreground="#ff4867", width=7,
                     height=1).pack(side="left", padx=10, pady=10)
            obj.num_ent = tk.Entry(combobox_frame, width=4, font=('方正姚体', 11))
            obj.num_ent.pack(padx=10, pady=10, side="left")
            tk.Label(combobox_frame, text=f'每笔订单限购{data[value]["limitQuantity"]}张', font=('楷体', 8),
                     foreground="#c51538").pack(padx=10, pady=10, side="left")
            tk.Button(combobox_frame, text="添加至待抢列表", font=('方正姚体', 10), bg="#88dba3",
                      command=lambda: self.add_ticket_list(entry)).pack(side="right", padx=70, pady=10)

        data: dict = self.server.order.views[_id]
        self.date_rg = RadioGroup(date_frame, data.keys(), command=lambda: show_ticket(self))
        date_frame.pack(fill="both", padx=20, pady=15, expand=True)

        ticket_frame = tk.Frame(self.menu, bg="#f9f9f9")
        ticket_frame.pack(fill="both", padx=20, pady=15, expand=True)

        combobox_frame = tk.Frame(self.menu, bg="#f9f9f9")
        combobox_frame.pack(fill="x", padx=15, pady=5, expand=True)

    def destroy(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def create_task(self, task_ent, id_entry):
        id_ = id_entry.get()
        task_time = task_ent.get()
        try:
            run_date = datetime.strptime(task_time, "%Y%m%d%H%M")
        except ValueError:
            messagebox.showerror(message='时间校验出错，格式如：202306011358')
            return
        trigger = DateTrigger(run_date=run_date, timezone='Asia/Shanghai')
        self.scheduler.add_job(self.server.task.run_tasks, trigger=trigger, args=(id_,))
        self.log_text.insert(tk.END, f'已添加任务：{run_date}/{id_}\n')

    def add_ticket_list(self, id_entry):
        num_ent = getattr(self, 'num_ent').get()
        if not is_integer(num_ent):
            messagebox.showerror(message='购票数量有误')
            return
        id_ = id_entry.get()
        date = self.date_rg.var.get()
        ticket = getattr(self, 'ticket_rg').var.get()
        pn = ticket.split('/')[0]
        self.server.add_task(id_, date, pn, int(num_ent))
        self.log_text.insert(tk.END, f'已添加至待抢：{id_}/{date}/{pn}/{num_ent}\n')

    def show_tasks(self):
        self.destroy()
        lbl = ttk.Label(self.main_frame, text=self.scheduler.get_jobs(), font=('楷体', 10))
        lbl.pack(fill='both', expand=True)


class RadioGroup:

    def __init__(self, master, options, command=None, **kwargs):
        self.var = tk.StringVar()
        self.var.set(None)
        for option in options:
            rb = tk.Radiobutton(master, text=option, variable=self.var, font=('方正姚体', 10),
                                value=option, command=command, bg="#f9f9f9")
            rb.pack(side="left", padx=2, **kwargs)


class AsyncIOSchedulerTask:

    def __init__(self):
        self._scheduler = AsyncIOScheduler(timezone='Asia/Shanghai')
        self.loop = asyncio.new_event_loop()
        self._t = threading.Thread(target=self._start)
        self._t.start()

    def _start(self):
        asyncio.set_event_loop(self.loop)
        self._scheduler.start()
        self.loop.run_forever()

    async def _add_job(self, func, **kwargs):
        self._scheduler.add_job(func, **kwargs)

    def add_job(self, func, **kwargs):
        coroutine = self._add_job(func, **kwargs)
        asyncio.run_coroutine_threadsafe(coroutine, self.loop)

    def get_jobs(self, **kwargs):
        return self._scheduler.get_jobs(**kwargs)

    def join(self):
        self._t.join()


def is_integer(param):
    try:
        int(param)
        return True
    except (ValueError, TypeError):
        return False


def run():
    import os
    import signal

    def kill():
        os.kill(os.getpid(), signal.SIGTERM)

    app = App()
    app.protocol("WM_DELETE_WINDOW", kill)
    app.mainloop()


if __name__ == '__main__':
    run()
