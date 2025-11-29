#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
检查数据库中的用户数据
"""

from app import create_app, db
from app.modules.user.models import User

# 创建应用实例
app = create_app('development')

# 在应用上下文中查询数据库
with app.app_context():
    try:
        # 查询所有用户
        users = User.query.all()
        print('用户数量:', len(users))
        
        # 打印用户信息
        for user in users:
            print(f'用户ID: {user.id}')
            print(f'  学号: {user.student_id}')
            print(f'  用户名: {user.username}')
            print(f'  邮箱: {user.email}')
            print(f'  创建时间: {user.created_at}')
            print('-' * 50)
            
    except Exception as e:
        print(f'查询出错: {str(e)}')