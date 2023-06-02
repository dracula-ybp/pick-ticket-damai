import os
import subprocess


def command_chrome(chrome_exe_path, user_data_dir, port):
    subprocess.Popen(f'{chrome_exe_path} --remote-debugging-port={port} --user-data-dir={user_data_dir}')


import os
import json


def check_config():
    # 获取用户根目录
    home_dir = os.path.expanduser("~")

    folder_path = os.path.join(home_dir, ".damai")
    file_path = os.path.join(folder_path, "config.json")
    user_dir = os.path.join(folder_path, "chrome")

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    if not os.path.exists(user_dir):
        os.makedirs(user_dir)

    if os.path.exists(file_path):
        with open(file_path) as f:
            data = json.load(f)
            return data

    # 如果配置文件不存在，则返回一个空的字典
    return {}


check_config()

