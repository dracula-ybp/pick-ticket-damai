import tkinter as tk
from tkinter import ttk

from damai.engine import ExecutionEngine


def callback(entry):
    return entry.get()


class App(tk.Tk):

    def __init__(self, *args, **kwargs):
        self.server = ExecutionEngine()
        # self.server.create_perform()
        super().__init__(*args, **kwargs)
        self.title('App')
        self.geometry('1100x650')

        # 创建主视图和侧边导航栏
        self.main_frame = tk.Frame(self, bg="#f9f9f9")
        sidebar = tk.Frame(self, bg='#f4f4f4', width=100, height=self.winfo_screenheight())

        style = ttk.Style()
        style.configure("RoundedButton.TButton", relief="flat",
                        borderwidth=0, foreground="#323232", font=("黑体", 15))
        style.map("RoundedButton.TButton", background=[("active", "#fafcfd")], foreground=[("active", "#ff4867")])
        btn1 = ttk.Button(sidebar, text='抢票需知', command=self.need_to_know, style='RoundedButton.TButton')
        btn2 = ttk.Button(sidebar, text='选票', command=self.choose_ticket, style='RoundedButton.TButton')

        # 布局侧边导航栏
        btn1.pack(pady=(30, 0), fill='x', padx=10)
        btn2.pack(pady=(30, 0), fill='x', padx=10)
        sidebar.pack(side='left', fill='y')

        # 布局主界面
        self.main_frame.pack(side='right', fill='both', expand=True)
        ttk.Label(self.main_frame, text='Welcome', font=('Arial', 30)).pack()

    def need_to_know(self):
        """显示抢票需知"""
        self.destroy()
        text = """
        1.21321の2rwefsdggwgaweawfeefsef对方违法
        2.dwqdqdq啊哇打网球
        3.文法问法二v啊vVERb
        """
        lbl = ttk.Label(self.main_frame, text=text, font=('楷体', 19))
        lbl.pack(fill='both', expand=True)

    def choose_ticket(self):
        self.destroy()
        search = tk.Frame(self.main_frame, height=10, bg="#e5e5e5", pady=10, padx=5)
        search.pack(side="top", pady=20)
        tk.Label(search, text="演出ID:", font=('楷体', 13), bg="#e5e5e5").pack(side="left")
        entry = tk.Entry(search, font=('方正姚体', 11))
        entry.pack(side="left")
        tk.Button(search, text="搜索", font=('楷体', 10), bg="#ffecef", command=lambda: self.show_menu(entry)).pack(
            side="left",
            padx=10)
        tk.Button(self.main_frame, text="创建任务", font=('楷体', 10), bg="#ffecef").pack(side="right", padx=10, pady=40)
        tk.Entry(self.main_frame, width=8, font=('方正姚体', 11)).pack(side="right", pady=40)
        tk.Label(self.main_frame, text="开抢时间:", font=('楷体', 13)).pack(side="right", pady=40)

        self.log_text = tk.Text(self.main_frame, height=15)
        self.log_text.pack(side='bottom', fill='x')

    def show_menu(self, entry):
        # 715121254118
        if hasattr(self, 'menu'):
            self.menu.destroy()
        _id = entry.get()
        self.log_text.insert(tk.END, f'id:{_id},演出信息加载中...\n')
        self.server.order.add(_id)
        date = {j["performName"].split()[0] for i in self.server.order.views[_id] for j in i}
        ticket = {j["priceName"] for i in self.server.order.views[_id] for j in i}
        # date = ['2023-07-01', '2023-07-02']
        # ticket = ['看台317元', '内场3217元', '看台6577元', '看台31E7元', '21321', '看台317元']
        self.menu = tk.Frame(self.main_frame, width=600, height=350, bg='#fafafa')
        self.menu.pack(padx=20, pady=20, expand=True, fill='both')

        tk.Label(self.menu, text="场次", font=('楷体', 13), bg='#f4f4f4', foreground="#ff4867").grid(row=0, column=0,
                                                                                                 sticky=tk.W, padx=10,
                                                                                                 pady=30)
        for i, label in enumerate(date):
            var = tk.BooleanVar()
            cb = tk.Checkbutton(self.menu, text=label, variable=var, font=('楷体', 10), bg="#ffffff",
                                foreground="#131a36")
            cb.grid(row=1, column=i, pady=5, padx=2, sticky=tk.W)

        tk.Label(self.menu, text="票档", font=('楷体', 13), bg='#f4f4f4', foreground="#ff4867").grid(row=2, column=0,
                                                                                                 sticky=tk.W, padx=10,
                                                                                                 pady=30)
        for i, label in enumerate(ticket):
            var = tk.BooleanVar()
            cb = tk.Checkbutton(self.menu, text=label, variable=var, font=('楷体', 10), bg="#ffffff",
                                foreground="#131a36")
            cb.grid(row=3, column=i, pady=5, padx=5, sticky=tk.W)

    def destroy(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()


if __name__ == '__main__':
    app = App()
    app.mainloop()
