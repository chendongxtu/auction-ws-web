# -*- coding: utf-8 -*-
from datetime import datetime
from . import db


class UsedCarDealerUser(db.Model):
    '''车商员工在系统的账号'''

    FIRST_DEPOSIT_AMOUNT = 500000

    __tablename__ = 'used_car_dealer_users'

    id = db.Column(db.BigInteger, primary_key=True, nullable=False)
    status = db.Column(db.SmallInteger, nullable=False, default=0)

    province = db.Column(db.String(32), nullable=True)
    province_code = db.Column(db.String(20), nullable=True)
    city = db.Column(db.String(32), nullable=True)
    city_code = db.Column(db.String(20), nullable=False)

    # 车商的邀请门店改为一对多的关系，故此列废除
    store_id = db.Column(db.BigInteger, nullable=True)

    name = db.Column(db.String(128), nullable=False)
    # NOTE 不同4S店推荐的车商手机号不应该重复
    mobile_number = db.Column(db.String(11), nullable=False, unique=True)

    # 银行信息(支行/卡号)
    bank_name = db.Column(db.String(256), nullable=False)
    bank_card_number = db.Column(db.String(256), nullable=False)
    bank_card_front_image = db.Column(db.String(256), nullable=False)
    id_number = db.Column(db.String(18), nullable=False)
    id_card_front_image = db.Column(db.String(256), nullable=False )
    id_card_back_image = db.Column(db.String(256), nullable=False)
    user_contract_front_image = db.Column(db.String(256), nullable=True)
    user_contract_back_image = db.Column(db.String(256), nullable=True)

    property_mask = db.Column(db.BigInteger, nullable=False, default=0)

    last_logged_in_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
    updated_at = db.Column(
            db.DateTime,
            nullable=False,
            default=datetime.now,
            onupdate=datetime.now)


class UsedCarAuctionStatus:
    '''重新设计后的拍卖状态'''

    UNKNOWN = 0
    PENDING = 1 # 待开拍
    BIDDING = 2 # 拍卖中
    SOLD = 3 # 已拍出
    UNSOLD = 4 # 已经流拍
    COMPLETED = 5 # 已成交
    CLOSED = 6 # 已关闭(拍出后交易失败)
    DELETED = 7 # 已取消

    NAMES = {
        UNKNOWN: '未知',
        PENDING: '待开拍',
        BIDDING: '竞拍中',
        SOLD: '已拍出',
        UNSOLD: '流拍',
        COMPLETED: '已成交',
        CLOSED: '已关闭',
        DELETED: '已删除',
    }

    # 注意，codes中对应的名字用來作为广播事件的类型，請不要隨意改动名字
    # 前端需要拿它的名字用來通信，如果一定要改，必須告知相关人員（包括前后端）
    CODES = {
        UNKNOWN: 'unknown',
        PENDING: 'pending',
        BIDDING: 'bidding',
        SOLD: 'sold',
        UNSOLD: 'unsold',
        COMPLETED: 'completed',
        CLOSED: 'closed',
        DELETED: 'deleted',
    }

    CODE_STATUS = {v: k for k, v in CODES.items()}

    @classmethod
    def name_of(cls, status):
        return cls.NAMES.get(status, cls.NAMES[cls.UNKNOWN])

    @classmethod
    def code_of(cls, status):
        return cls.CODES.get(status, cls.CODES[cls.UNKNOWN])
