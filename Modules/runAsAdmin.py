import ctypes
import sys
import os
import subprocess

def is_admin():
    """Проверяет, запущена ли программа от админа"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    """Перезапускает программу с правами администратора"""
    try:
        script_path = os.path.abspath(sys.argv[0])
        
        if getattr(sys, 'frozen', False):
            executable = sys.executable
            params = subprocess.list2cmdline(sys.argv[1:])
        else:
            executable = sys.executable
            params = f'"{script_path}" ' + subprocess.list2cmdline(sys.argv[1:])
        
        ctypes.windll.shell32.ShellExecuteW(None, "runas", executable, params, None, 1)
        return True
    except Exception as e:
        print(f"Ошибка при запросе прав: {e}")
        return False