import os
import time


def path_to_cmd(exe_path):
    if exe_path.startswith('.') or exe_path.startswith('/'):
        cmd = exe_path
    else:
        cmd = os.path.join('.', exe_path)
    return cmd


def print_time():
    print(time.strftime('%a %b %d %Y %H:%M:%S UTC%z', time.localtime()))
