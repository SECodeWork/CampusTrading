from app import create_app, db

# 创建应用实例
app = create_app('development')

# 在应用上下文中创建数据库表
with app.app_context():
    print('开始创建数据库表...')
    db.create_all()
    print('数据库表创建完成！')