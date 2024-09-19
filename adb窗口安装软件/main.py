import os
import subprocess
import tkinter as tk
from tkinterdnd2 import TkinterDnD, DND_FILES

# 全局变量存储拖放的路径
dragged_path_install = ""
dragged_path_push = ""

def adb_install(apk_path):
    """执行 adb install 命令"""
    try:
        result = subprocess.run(['adb', 'install', apk_path], capture_output=True, text=True)
        if result.returncode == 0:
            output_label.config(text=f"成功安装: {apk_path}")
        else:
            output_label.config(text=f"安装失败: {apk_path}\n{result.stderr}")
    except Exception as e:
        output_label.config(text=f"执行出错: {str(e)}")

def adb_push(file_path):
    """执行 adb push 命令，将文件推送到 /sdcard/Download"""
    try:
        result = subprocess.run(['adb', 'push', file_path, '/sdcard/Download'], capture_output=True, text=True)
        if result.returncode == 0:
            output_label.config(text=f"成功推送: {file_path} 到 /sdcard/Download")
        else:
            output_label.config(text=f"推送失败: {file_path}\n{result.stderr}")
    except Exception as e:
        output_label.config(text=f"执行出错: {str(e)}")

def install_apk_from_folder(folder_path):
    """遍历文件夹中的所有 .apk 文件并安装"""
    installed_count = 0
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.apk'):
                apk_path = os.path.join(root, file)
                adb_install(apk_path)
                installed_count += 1
    if installed_count == 0:
        output_label.config(text="没有找到任何APK文件")

def on_drop_install(event):
    """处理拖拽的APK文件或文件夹"""
    global dragged_path_install
    path = event.data.strip("{}")
    if os.path.isdir(path) or (os.path.isfile(path) and path.endswith('.apk')):
        dragged_path_install = path
        output_label.config(text=f"文件/文件夹已选中: {path}")
    else:
        output_label.config(text="无效的文件或文件夹，请拖放APK文件或包含APK的文件夹")

def on_drop_push(event):
    """处理拖拽的文件"""
    global dragged_path_push
    path = event.data.strip("{}")
    if os.path.isfile(path):
        dragged_path_push = path
        output_label.config(text=f"文件已选中: {path}")
    else:
        output_label.config(text="无效的文件，请拖放文件")

def adb_install_handler():
    """处理 ADB 安装，根据拖拽的文件或文件夹进行安装"""
    if not dragged_path_install:
        output_label.config(text="请先拖放APK文件或文件夹")
        return
    
    if os.path.isdir(dragged_path_install):
        install_apk_from_folder(dragged_path_install)
    elif os.path.isfile(dragged_path_install) and dragged_path_install.endswith('.apk'):
        adb_install(dragged_path_install)

def adb_push_handler():
    """处理 ADB Push，将文件推送到 /sdcard/Download"""
    if not dragged_path_push:
        output_label.config(text="请先拖放文件")
        return
    
    if os.path.isfile(dragged_path_push):
        adb_push(dragged_path_push)

def open_install_window():
    """打开安装 APK 的窗口"""
    install_window = TkinterDnD.Tk()
    install_window.title("APK 安装工具")
    install_window.geometry("400x300")
    
    label = tk.Label(install_window, text="请拖放APK文件或包含APK文件的文件夹", font=("Arial", 12))
    label.pack(pady=20)

    global output_label
    output_label = tk.Label(install_window, text="", font=("Arial", 10))
    output_label.pack(pady=10)

    install_window.drop_target_register(DND_FILES)
    install_window.dnd_bind('<<Drop>>', on_drop_install)

    install_button = tk.Button(install_window, text="ADB 安装", command=adb_install_handler, font=("Arial", 12))
    install_button.pack(pady=20)

    install_window.mainloop()

def open_push_window():
    """打开文件推送的窗口"""
    push_window = TkinterDnD.Tk()
    push_window.title("文件推送工具")
    push_window.geometry("400x300")
    
    label = tk.Label(push_window, text="请拖放要推送的文件", font=("Arial", 12))
    label.pack(pady=20)

    global output_label
    output_label = tk.Label(push_window, text="", font=("Arial", 10))
    output_label.pack(pady=10)

    push_window.drop_target_register(DND_FILES)
    push_window.dnd_bind('<<Drop>>', on_drop_push)

    push_button = tk.Button(push_window, text="ADB Push", command=adb_push_handler, font=("Arial", 12))
    push_button.pack(pady=20)

    push_window.mainloop()

# 创建主窗口
root = tk.Tk()
root.title("ADB 工具")
root.geometry("300x200")

# 创建进入安装界面的按钮
start_install_button = tk.Button(root, text="进入安装界面", command=open_install_window, font=("Arial", 14))
start_install_button.pack(pady=20)

# 创建进入文件推送界面的按钮
start_push_button = tk.Button(root, text="进入文件推送界面", command=open_push_window, font=("Arial", 14))
start_push_button.pack(pady=20)

root.mainloop()
