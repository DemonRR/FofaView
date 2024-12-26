import sys
import os

def resource_path(relative_path):
    """ 获取资源文件的绝对路径 """
    try:
        base_path = sys._MEIPASS  # PyInstaller 打包时的路径
    except AttributeError:
        base_path = os.path.abspath(".")  # 运行时的当前路径
    return os.path.join(base_path, relative_path)
