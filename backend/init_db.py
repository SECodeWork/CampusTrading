#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
数据库初始化脚本 - 简化版
专注于创建数据库和初始配置
"""

import os
import sys
import pymysql

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 从配置文件导入配置
from config.development import DevelopmentConfig

# 获取数据库配置
db_uri = DevelopmentConfig.SQLALCHEMY_DATABASE_URI
print(f"数据库配置: {db_uri}")


def create_database_if_not_exists():
    """创建数据库（如果不存在）"""
    print("正在检查数据库是否存在...")
    
    if db_uri.startswith('mysql+pymysql://'):
        # 解析连接字符串
        uri_parts = db_uri[len('mysql+pymysql://'):].split('@')
        
        if len(uri_parts) != 2:
            print(f"数据库URI格式错误: {db_uri}")
            return False
            
        user_pass_part, host_db_part = uri_parts
        
        # 提取用户名和密码
        if ':' in user_pass_part:
            username, password = user_pass_part.split(':', 1)
        else:
            username = user_pass_part
            password = ''
            
        # 提取主机、端口和数据库名
        host_port_part, db_name = host_db_part.split('/', 1)
        
        if ':' in host_port_part:
            host, port = host_port_part.split(':', 1)
        else:
            host = host_port_part
            port = '3306'  # 默认端口
        
        print(f"连接信息: 用户名={username}, 主机={host}, 端口={port}, 数据库名={db_name}")
        
        try:
            # 连接到MySQL服务器
            conn = pymysql.connect(
                host=host,
                port=int(port),
                user=username,
                password=password,
                cursorclass=pymysql.cursors.DictCursor
            )
            
            with conn.cursor() as cursor:
                # 检查数据库是否存在
                cursor.execute(f"SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = '{db_name}'")
                result = cursor.fetchone()
                
                if not result:
                    print(f"创建数据库 {db_name}...")
                    cursor.execute(f"CREATE DATABASE {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
                    print(f"数据库 {db_name} 创建成功！")
                else:
                    print(f"数据库 {db_name} 已存在。")
            
            conn.close()
            return True
            
        except Exception as e:
            print(f"数据库操作失败: {str(e)}")
            print("请确保MySQL服务已启动，且连接信息正确。")
            return False
    else:
        print(f"不支持的数据库类型: {db_uri}")
        return False


def display_manual_steps():
    """显示手动运行迁移的步骤"""
    print("\n=== 手动数据库迁移步骤 ===")
    print("1. 初始化迁移仓库:")
    print("   flask db init")
    print("\n2. 创建初始迁移:")
    print("   flask db migrate -m 'Initial migration'")
    print("\n3. 应用迁移:")
    print("   flask db upgrade")
    print("\n4. 启动应用:")
    print("   python run.py")


def main():
    """主函数"""
    print("===== 数据库初始化脚本 =====")
    
    # 1. 创建数据库
    if create_database_if_not_exists():
        print("\n数据库准备完成！")
        display_manual_steps()
        return 0
    else:
        print("\n数据库准备失败，请检查错误信息。")
        return 1


if __name__ == '__main__':
    sys.exit(main())