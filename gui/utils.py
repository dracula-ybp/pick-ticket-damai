import os
import json
import subprocess

user_dir = os.path.expanduser("~")
folder_path = os.path.join(user_dir, ".damai")
config_path = os.path.join(folder_path, "config.json")
chrome_path = os.path.join(folder_path, "chrome")


def command_chrome(chrome_exe_path):
    cmd = [chrome_exe_path, '--remote-debugging-port=9222', f'--user-data-dir={chrome_path}']
    subprocess.Popen(cmd)


def check_config():
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    if not os.path.exists(chrome_path):
        os.makedirs(chrome_path)

    if not os.path.exists(config_path):
        with open(config_path, 'w') as f:
            json.dump({'chrome_exe_path': ''}, f)


