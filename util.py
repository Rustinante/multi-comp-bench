import os


def path_to_cmd(exe_path):
    if exe_path.startswith('.') or exe_path.startswith('/'):
        cmd = exe_path
    else:
        cmd = os.path.join('.', exe_path)
    return cmd
