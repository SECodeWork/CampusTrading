#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
数据库设置脚本
设置环境变量并运行迁移命令
"""

import os
import sys
import subprocess

# 设置Flask应用环境变量
os.environ['FLASK_APP'] = 'app'

print("===== 数据库设置脚本 =====")
print("正在设置环境变量...")
print(f"FLASK_APP = {os.environ['FLASK_APP']}")


def run_command(command):
    """运行命令并显示输出"""
    print(f"\n执行命令: {command}")
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        if result.stdout:
            print("输出:")
            print(result.stdout)
        
        if result.stderr:
            print("错误:")
            print(result.stderr)
        
        return result.returncode == 0
    except Exception as e:
        print(f"命令执行失败: {str(e)}")
        return False


def main():
    """主函数"""
    # 步骤1: 检查migrations目录是否存在，如果存在则删除
    migrations_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'migrations')
    if os.path.exists(migrations_dir):
        print(f"删除已存在的迁移目录: {migrations_dir}")
        import shutil
        shutil.rmtree(migrations_dir)
    
    # 步骤2: 初始化迁移仓库
    if not run_command('flask db init'):
        print("初始化迁移仓库失败!")
        return 1
    
    # 步骤3: 创建初始迁移
    if not run_command('flask db migrate -m "Initial migration"'):
        print("创建初始迁移失败!")
        return 1
    
    # 步骤4: 应用迁移
    if not run_command('flask db upgrade'):
        print("应用迁移失败!")
        return 1
    
    print("\n===== 数据库设置完成 =====")
    print("您可以通过运行 'python run.py' 启动后端服务。")
    return 0


if __name__ == '__main__':
    sys.exit(main())