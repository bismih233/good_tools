import os
import subprocess
import tkinter as tk
from tkinterdnd2 import TkinterDnD, DND_FILES

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
    path = event.data.strip("{}")
    if os.path.isdir(path):
        # 如果是文件夹，安装文件夹中的所有APK文件
        install_apk_from_folder(path)
    elif os.path.isfile(path) and path.endswith('.apk'):
        # 如果是单个APK文件，直接安装
        adb_install(path)
    else:
        output_label.config(text="无效的文件或文件夹，请拖放APK文件或包含APK的文件夹")

# 创建主窗口
root = TkinterDnD.Tk()
root.title("APK 安装工具")
root.geometry("400x200")

# 提示标签
label = tk.Label(root, text="请拖放APK文件或包含APK文件的文件夹", font=("Arial", 12))
label.pack(pady=20)

# 显示结果的标签
output_label = tk.Label(root, text="", font=("Arial", 10))
output_label.pack(pady=10)

# 设置窗口支持拖拽文件
root.drop_target_register(DND_FILES)
root.dnd_bind('<<Drop>>', on_drop)

# 运行主窗口循环
root.mainloop()
