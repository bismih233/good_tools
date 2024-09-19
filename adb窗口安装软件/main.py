import os
import subprocess
import tkinter as tk
from tkinterdnd2 import TkinterDnD, DND_FILES

# 全局变量存储拖放的路径
dragged_path = ""

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

def on_drop(event):
    """处理拖拽的文件或文件夹"""
    global dragged_path
    path = event.data.strip("{}")
    if os.path.isdir(path) or (os.path.isfile(path) and path.endswith('.apk')):
        dragged_path = path
        output_label.config(text=f"文件/文件夹已选中: {path}")
    else:
        output_label.config(text="无效的文件或文件夹，请拖放APK文件或包含APK的文件夹")

def adb_install_handler():
    """处理ADB安装，根据拖拽的文件或文件夹进行安装"""
    if not dragged_path:
        output_label.config(text="请先拖放APK文件或文件夹")
        return
    
    if os.path.isdir(dragged_path):
        # 如果是文件夹，安装文件夹中的所有APK文件
        install_apk_from_folder(dragged_path)
    elif os.path.isfile(dragged_path) and dragged_path.endswith('.apk'):
        # 如果是单个APK文件，直接安装
        adb_install(dragged_path)

def open_install_window():
    """点击按钮后打开安装界面"""
    install_window = TkinterDnD.Tk()
    install_window.title("APK 安装工具")
    install_window.geometry("400x300")
    
    # 提示标签
    label = tk.Label(install_window, text="请拖放APK文件或包含APK文件的文件夹", font=("Arial", 12))
    label.pack(pady=20)

    # 显示结果的标签
    global output_label
    output_label = tk.Label(install_window, text="", font=("Arial", 10))
    output_label.pack(pady=10)

    # 设置窗口支持拖拽文件
    install_window.drop_target_register(DND_FILES)
    install_window.dnd_bind('<<Drop>>', on_drop)

    # 添加ADB安装按钮
    install_button = tk.Button(install_window, text="ADB 安装", command=adb_install_handler, font=("Arial", 12))
    install_button.pack(pady=20)

    install_window.mainloop()

# 创建主窗口
root = tk.Tk()
root.title("ADB APK 安装器")
root.geometry("300x200")

# 创建进入安装界面的按钮
start_button = tk.Button(root, text="点击进入安装界面", command=open_install_window, font=("Arial", 14))
start_button.pack(pady=50)

root.mainloop()
