from datetime import datetime
from app import db

class RentalContract(db.Model):
    """租赁合同模型"""
    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.Integer, db.ForeignKey('transaction.id'), nullable=False, unique=True)
    
    # 合同状态
    contract_status = db.Column(db.String(20), default='active')  # active(进行中), completed(已完成), broken(已违约)
    
    # 归还状态
    return_status = db.Column(db.String(20))  # pending(待归还), returned(已归还), overdue(逾期)
    actual_return_date = db.Column(db.DateTime)  # 实际归还日期
    
    # 商品状态检查
    item_condition_before = db.Column(db.Text)  # 出租前商品状态
    item_condition_after = db.Column(db.Text)   # 归还后商品状态
    damage_description = db.Column(db.Text)     # 损坏描述
    
    # 违约信息
    is_breach = db.Column(db.Boolean, default=False)  # 是否违约
    breach_reason = db.Column(db.Text)  # 违约原因
    penalty_amount = db.Column(db.Integer)  # 违约金
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    transaction = db.relationship('Transaction', backref='rental_contract', uselist=False)