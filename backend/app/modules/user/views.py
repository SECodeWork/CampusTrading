from flask import Blueprint, request, jsonify
from .models import User
from app import db
from flask_jwt_extended import create_access_token

user_bp = Blueprint('user', __name__)

@user_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'Username already registered'}), 400
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'Email already registered'}), 400

    new_user = User(username = data['username'], email = data['email'])
    new_user.set_password(data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created'}), 201

@user_bp.route('/login', methods=['POST'])
def login():
    # 添加调试日志
    print("接收到登录请求")
    data = request.get_json()
    print(f"登录请求数据: {data}")
    
    # 检查请求数据是否包含必要字段
    if not data or 'username' not in data or 'password' not in data:
        print("缺少必要的用户名或密码字段")
        return jsonify({'message': '缺少必要的用户名或密码字段'}), 400
    
    user = User.query.filter_by(username=data['username']).first()
    print(f"查询用户结果: {'找到用户' if user else '未找到用户'}")
    
    if not user or not user.check_password(data['password']):
        print(f"登录失败: {'用户不存在' if not user else '密码错误'}")
        return jsonify({'message': 'Incorrect username or password'}), 401
    
    access_token = create_access_token(identity=user.username)
    print("登录成功，生成访问令牌")
    return jsonify({'access_token': access_token}), 200
