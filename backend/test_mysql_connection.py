#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试MySQL数据库连接和用户表
"""

from app import create_app, db
from app.modules.user.models import User
from sqlalchemy import text

# 创建应用实例
app = create_app('development')

with app.app_context():
    print("正在测试MySQL数据库连接...")
    try:
        # 测试数据库连接
        db.session.execute(text('SELECT 1'))
        print("✅ 数据库连接成功！")
        
        # 检查用户表是否存在
        print("\n正在检查用户表...")
        users = User.query.all()
        print(f"✅ 用户表存在，当前用户数量: {len(users)}")
        
        if users:
            print("\n用户列表:")
            for user in users:
                print(f"  - 用户ID: {user.id}, 学号: {user.student_id}, 用户名: {user.username}")
        else:
            print("\n注意: 当前没有用户记录")
            
    except Exception as e:
        print(f"❌ 数据库操作失败: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        db.session.remove()