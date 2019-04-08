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

    organization_id = db.Column(
        db.BigInteger,
        db.ForeignKey('used_car_dealer_organizations.id'), nullable=False)
    organization = db.relationship(
        'UsedCarDealerOrganization',
        backref=db.backref('users', lazy='dynamic'))

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

    # NOTE account_id 对应 Account 的记录 且 account_type 为 master
    # 在创建 dealer_user 的时候就需要初始化完毕
    account_id = db.Column(
        db.BigInteger, db.ForeignKey('accounts.id'), nullable=False)
    account = db.relationship(
        'Account', backref=db.backref('dealer_user', uselist=False))

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


class UsedCarAuction(db.Model):

    AUCTION_FROZEN_AMOUNT = 200000
    FINISH_OVER_TIME = 20

    __tablename__ = 'used_car_auctions'

    id = db.Column(db.BigInteger, primary_key=True, nullable=False)
    status = db.Column(db.SmallInteger, nullable=False, default=0)

    # city_code已废弃
    city_code = db.Column(db.String(20), nullable=True)

    auction_session_id = db.Column(
        db.BigInteger,
        db.ForeignKey('used_car_auction_sessions.id'), nullable=True)
    auction_session = db.relationship(
        'UsedCarAuctionSession',
        backref=db.backref('auctions', lazy='dynamic'))

    store_id = db.Column(
        db.BigInteger, db.ForeignKey('stores.id'), nullable=False)
    store = db.relationship(
        'Store', backref=db.backref(
            'auctions', lazy='dynamic'))

    auction_car_id = db.Column(
        db.BigInteger, db.ForeignKey('auction_cars.id'), nullable=False)
    auction_car = db.relationship(
        'AuctionCar', backref=db.backref('auctions', lazy='dynamic'))
    # 详情快照
    auction_car_info_id = db.Column(
        db.BigInteger, db.ForeignKey('auction_car_infos.id'), nullable=False)
    auction_car_info = db.relationship(
        'AuctionCarInfo', backref=db.backref('auctions', lazy='dynamic'))

    # NOTE 不再使用
    # editor_id = db.Column(
        # db.BigInteger, db.ForeignKey('employees.id'), nullable=False)
    # editor = db.relationship(
        # 'Employee', backref=db.backref(
            # 'edit_auction_cars', lazy='dynamic'))

    sequence = db.Column(db.Integer, nullable=False)
    contact_name = db.Column(db.String(128), nullable=False)
    contact_number = db.Column(db.String(20), nullable=False)

    minimum_price = db.Column(db.BigInteger, nullable=False, doc='起拍价，单位分')
    reserve_price = db.Column(
        db.BigInteger, nullable=False, doc='保留价（最低成交价），单位分')
    maximum_price = db.Column(db.BigInteger, nullable=False, doc='最高价，单位分')
    quote_increment = db.Column(db.BigInteger, nullable=False, default=10000, server_default='10000', doc='加价幅度，单位分')
    # 记录当前报价
    latest_quote_price = db.Column(db.BigInteger, nullable=True)
    latest_quoter_id = db.Column(db.BigInteger, nullable=True) # 指向最新报价人

    started_at = db.Column(db.DateTime, nullable=True)
    finished_at = db.Column(db.DateTime, nullable=True)
    # NOTE 不再使用
    # edited_at = db.Column(db.DateTime, nullable=True)
    # published_at = db.Column(db.DateTime, nullable=True)

    # NOTE 修正指向
    winner_id = db.Column(
        db.BigInteger,
        db.ForeignKey('used_car_dealer_users.id'), nullable=True, doc='成交人')
    winner = db.relationship(
        'UsedCarDealerUser', backref=db.backref(
            'winner_auctions', lazy='dynamic'))
    # NOTE 不再使用
    # remark = db.Column(db.String(512), nullable=True)

    # 车辆拍出后生成的订单id
    order_id = db.Column(db.BigInteger, nullable=True)

    property_mask = db.Column(db.BigInteger, nullable=False, default=0, server_default='0')

    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.now,
        onupdate=datetime.now)

    version = db.Column(db.Integer, nullable=False, default=0)
    __mapper_args__ = {"version_id_col": version}

