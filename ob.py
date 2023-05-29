import tkinter as tk
from tkinter import ttk


class ExampleApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 设置窗口标题和大小
        self.title('Example App')
        self.geometry('800x600')

        # 创建主视图和侧边导航栏
        self.main_frame = tk.Frame(self)
        sidebar = tk.Frame(self, bg='#242424', width=100, height=self.winfo_screenheight())

        # 添加按钮和标签到侧边导航栏，并绑定回调函数
        style = ttk.Style()
        style.configure('TButton', borderwidth=0, foreground='#e95787', font=('黑体', 14), padding=10,
                        background='#283593')
        btn1 = ttk.Button(sidebar, text='抢票需知', command=self.need_to_know, style='TButton')
        btn2 = ttk.Button(sidebar, text='选票', command=self.choose_ticket, style='TButton')

        # 布局侧边导航栏
        btn1.pack(pady=(10, 0), fill='x', padx=10)
        btn2.pack(pady=(10, 0), fill='x', padx=10)
        sidebar.pack(side='left', fill='y')

        # 布局主界面
        self.main_frame.pack(side='right', fill='both', expand=True)

        # 创建一个字典，存储数据以生成多选框、单选框和下拉框
        data = {
            'Fruit': ['Apple', 'Banana', 'Cherry', 'Durian'],
            'Animal': ['Dog', 'Cat', 'Bird', 'Fish'],
            'Color': ['Red', 'Green', 'Blue', 'Yellow']
        }

        # 添加多个组合框供选择
        for key in data:
            lbl = ttk.Label(self.main_frame, text=key, font=('Arial', 12))
            lbl.pack(fill='both', expand=True, pady=10)
            options = ttk.Combobox(self.main_frame, values=data[key], state='readonly')
            options.pack(fill='both', expand=True, padx=10, pady=10)

    def need_to_know(self):
        """显示抢票需知"""
        self.destroy()
        text = """
        1.21321の2rwefsdggwgaweawfeefsef对方违法
        2.dwqdqdq啊哇打网球
        3.文法问法二v啊vVERb
        """
        lbl = ttk.Label(self.main_frame, text='2312', font=('楷体', 19))
        lbl.pack(fill='both', expand=True)

    def choose_ticket(self):
        self.destroy()

        search = tk.Frame(self.main_frame, pady=20, width=600)
        search.pack(side="top")
        tk.Label(search, text="演出ID:", font=('楷体', 13)).pack(side="left")
        tk.Entry(search).pack(side="left", padx=15)
        tk.Label(search, text="抢票时间:", font=('楷体', 13)).pack(side="left")
        tk.Entry(search).pack(side="left")
        tk.Button(search, text="搜索", font=('楷体', 10), bg="#F16B6F").pack(side="left", padx=10)

        search = tk.Frame(self.main_frame, pady=30, width=600)
        search.pack(side="top")

        search2 = tk.Frame(self.main_frame, pady=30, width=600)
        search2.pack(side="top")

        # 初始数据
        options = ['Option A', 'Option B', 'Option C']

        for i, label in enumerate(options):
            var = tk.BooleanVar()  # 创建BooleanVar变量，用于保存复选框的状态
            cb = tk.Checkbutton(search, text=label, variable=var)
            cb.pack(anchor="w", side="left")  # 放置复选框

        for i, label in enumerate(options):
            var = tk.BooleanVar()  # 创建BooleanVar变量，用于保存复选框的状态
            cb = tk.Checkbutton(search2, text=label, variable=var)
            cb.pack(anchor="w", side="left")  # 放置复选框

        def quei():
            for widget in search2.winfo_children():
                widget.destroy()
            for widget in search.winfo_children():
                widget.destroy()
            self.choose_ticket()

        sw = tk.Frame(self.main_frame, pady=20, width=600)
        tk.Button(sw, text="12312", font=('楷体', 10), bg="#F16B6F", command=quei).pack(side="left", padx=10)
        sw.pack(side='left', fill='y')

    def destroy(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()


if __name__ == '__main__':
    app = ExampleApp()
    app.mainloop()
