#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
直接调用数据库初始化功能的脚本
"""

import os
import sys
from run import app, db, init_db
from flask.cli import with_appcontext

# 确保应用上下文被激活
with app.app_context():
    print("正在初始化数据库...")
    # 直接执行数据库创建
    db.create_all()
    print("数据库表创建完成！")
    print("\n现在你可以运行 'python run.py' 启动后端服务了。")