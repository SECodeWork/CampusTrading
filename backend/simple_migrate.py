#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
简化的数据库迁移脚本
直接执行Flask-Migrate命令，避免复杂的Python导入
"""

import os
import sys
import subprocess
import shutil

# 设置Flask应用环境变量
os.environ['FLASK_APP'] = 'app'

print("===== 简化数据库迁移脚本 =====")
print("正在设置环境变量...")
print(f"FLASK_APP = {os.environ['FLASK_APP']}")

# 删除现有的migrations目录以避免冲突
migrations_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'migrations')
if os.path.exists(migrations_dir):
    print(f"删除已存在的迁移目录: {migrations_dir}")
    shutil.rmtree(migrations_dir)

# 定义要执行的命令序列
commands = [
    ['flask', 'db', 'init'],
    ['flask', 'db', 'migrate', '-m', 'Initial migration'],
    ['flask', 'db', 'upgrade']
]

# 执行每个命令
for cmd in commands:
    print(f"\n执行命令: {' '.join(cmd)}")
    try:
        result = subprocess.run(
            cmd,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        if result.stdout:
            print("输出:")
            print(result.stdout[:1000] + ("... (截断)" if len(result.stdout) > 1000 else ""))
        
        if result.stderr:
            print("错误:")
            print(result.stderr[:1000] + ("... (截断)" if len(result.stderr) > 1000 else ""))
        
        if result.returncode != 0:
            print(f"命令执行失败，退出码: {result.returncode}")
            sys.exit(1)
            
    except Exception as e:
        print(f"命令执行异常: {str(e)}")
        sys.exit(1)

print("\n===== 数据库迁移完成 =====")
print("数据库已成功初始化并应用迁移。")
print("您可以通过运行 'python run.py' 启动后端服务。")