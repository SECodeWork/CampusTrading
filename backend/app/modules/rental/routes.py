from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, timedelta
from app import db
from app.modules.item.models import Item
from app.modules.transaction.models import Transaction
from app.modules.user.models import User
from app.modules.rental.models import RentalContract

rental_bp = Blueprint('rental', __name__)

@rental_bp.route('/', methods=['GET'])
def get_rental_items():
    """获取可租赁商品列表"""
    # 复用item_bp的逻辑，但只获取transaction_type为rent的商品
    campus_id = request.args.get('campus_id', type=int)
    category_id = request.args.get('category_id', type=int)
    keyword = request.args.get('keyword')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # 构建查询，只获取租赁类型的商品
    query = Item.query.filter_by(transaction_type='rent', status='active')
    
    # 其他筛选条件...
    if campus_id:
        query = query.join(User).filter(User.campus_id == campus_id)
    if category_id:
        query = query.filter_by(category_id=category_id)
    if keyword:
        query = query.filter(Item.name.like(f'%{keyword}%') | Item.description.like(f'%{keyword}%'))
    
    # 分页
    pagination = query.order_by(Item.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    items = pagination.items
    
    # 格式化结果...
    result = []
    for item in items:
        item_dict = item.to_dict()
        # 添加卖家信息
        item_dict['seller'] = {
            'id': item.user.id,
            'username': item.user.username,
            'campus': item.user.campus.name if item.user.campus else None
        }
        result.append(item_dict)
    
    return jsonify({
        'items': result,
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': pagination.page
    })

@rental_bp.route('/request', methods=['POST'])
@jwt_required()
def request_rental():
    """请求租赁商品"""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    item_id = data.get('item_id')
    rental_days = data.get('rental_days', 1)
    start_date = datetime.strptime(data.get('start_date'), '%Y-%m-%d')
    meeting_location = data.get('meeting_location')
    
    # 检查商品
    item = Item.query.get_or_404(item_id)
    if item.status != 'active' or item.transaction_type != 'rent':
        return jsonify({'error': '该商品不可租赁'}), 400
    
    if item.user_id == user_id:
        return jsonify({'error': '不能租赁自己的商品'}), 400
    
    # 计算租赁费用和押金
    if rental_days <= 7:
        rental_price = item.rental_price_day * rental_days
    elif rental_days <= 30:
        rental_price = item.rental_price_week * (rental_days // 7) + item.rental_price_day * (rental_days % 7)
    else:
        rental_price = item.rental_price_month * (rental_days // 30) + item.rental_price_day * (rental_days % 30)
    
    deposit = item.deposit
    total_amount = rental_price + deposit
    
    # 检查余额
    user = User.query.get(user_id)
    if user.coins < total_amount:
        return jsonify({'error': '虚拟币余额不足'}), 400
    
    # 创建交易记录
    transaction = Transaction(
        buyer_id=user_id,
        seller_id=item.user_id,
        item_id=item_id,
        amount=total_amount,
        status='pending',
        transaction_type='rent',
        rental_days=rental_days,
        start_date=start_date,
        end_date=start_date + timedelta(days=rental_days),
        deposit_paid=deposit,
        meeting_location=meeting_location
    )
    
    # 创建租赁合同
    contract = RentalContract(transaction=transaction)
    
    try:
        db.session.add(transaction)
        db.session.add(contract)
        item.status = 'rented'  # 更新商品状态为已出租
        db.session.commit()
        
        return jsonify({
            'message': '租赁请求已提交',
            'transaction_id': transaction.id,
            'total_amount': total_amount,
            'rental_price': rental_price,
            'deposit': deposit
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@rental_bp.route('/<int:transaction_id>/confirm', methods=['POST'])
@jwt_required()
def confirm_rental(transaction_id):
    """确认租赁交易（卖家确认）"""
    user_id = get_jwt_identity()
    
    # 获取交易记录
    transaction = Transaction.query.get_or_404(transaction_id)
    
    # 检查权限
    if transaction.seller_id != user_id:
        return jsonify({'error': '无权限操作此交易'}), 403
    
    if transaction.status != 'pending':
        return jsonify({'error': '交易状态不正确'}), 400
    
    # 更新交易状态
    transaction.status = 'paid'
    transaction.paid_at = datetime.utcnow()
    
    # 转移虚拟币
    buyer = User.query.get(transaction.buyer_id)
    seller = User.query.get(transaction.seller_id)
    
    # 租金转给卖家，押金暂时不转
    seller.coins += transaction.amount - transaction.deposit_paid
    buyer.coins -= transaction.amount
    
    try:
        db.session.commit()
        return jsonify({'message': '交易已确认'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@rental_bp.route('/<int:transaction_id>/return', methods=['POST'])
@jwt_required()
def return_item(transaction_id):
    """归还商品"""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    transaction = Transaction.query.get_or_404(transaction_id)
    
    # 检查权限（只有买家可以归还商品）
    if transaction.buyer_id != user_id:
        return jsonify({'error': '无权限操作此交易'}), 403
    
    contract = transaction.rental_contract
    if not contract:
        return jsonify({'error': '找不到租赁合同'}), 404
    
    # 更新合同状态
    contract.return_status = 'returned'
    contract.actual_return_date = datetime.utcnow()
    contract.item_condition_after = data.get('item_condition_after')
    
    # 如果有损坏描述，设置相应状态
    if data.get('damage_description'):
        contract.damage_description = data.get('damage_description')
        contract.is_breach = True
        contract.breach_reason = '商品损坏'
    
    # 更新交易状态为已完成
    transaction.status = 'completed'
    transaction.completed_at = datetime.utcnow()
    
    # 更新商品状态为可租赁
    item = Item.query.get(transaction.item_id)
    item.status = 'active'
    
    # 退还押金（如果没有损坏）
    buyer = User.query.get(transaction.buyer_id)
    if not contract.is_breach:
        buyer.coins += transaction.deposit_paid
    else:
        # 有损坏，押金转给卖家作为赔偿
        seller = User.query.get(transaction.seller_id)
        seller.coins += transaction.deposit_paid
    
    try:
        db.session.commit()
        return jsonify({
            'message': '商品已归还',
            'deposit_refunded': not contract.is_breach
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# 其他API如获取租赁记录、延长租期等