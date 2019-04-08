# -*- coding: utf-8 -*-

import jwt
import json
from flask import (
    request,
    current_app
)
from datetime import datetime
from flask_socketio import emit, join_room, leave_room, \
    close_room, disconnect

from  .. import socketio, redis
from ..utils.time_utils import datetime_to_str
from ..models import UsedCarDealerUser


ACCESS_TOKEN_EXPIRE_NAME = 2*60*60

def _get_auction_room_name(room_id):
    if not room_id:
        return None

    return 'auction_room_' + str(room_id)


@socketio.on('connect', namespace='/auction_car')
def socket_connect():
    access_token = request.args.get('access_token')
    if not access_token:
        current_app.logger.error('websocket connect failed: access_token lost')
        return False

    try:
        data = jwt.decode(access_token, current_app.config.get('SECRET_KEY'))
    except Exception as e:
        current_app.logger.error(
            'fail to decode access_token: %s. \nerro_info: %s', access_token, e)
        return False

    user_id = data.get('user_id')
    if not user_id:
        current_app.logger.error('websocket connect failed: token missed user related param')
        return False

    dealer_user = UsedCarDealerUser.query.get(int(user_id))
    if dealer_user is None:
        current_app.logger.error('websocket connect failed: dealer[%s] not exist', user_id)
        return False

    connect_info = {
        'user_id': user_id,
        'connect_time': datetime_to_str(datetime.now())
    }
    redis.set(request.sid, json.dumps(connect_info), ex=ACCESS_TOKEN_EXPIRE_NAME)
    current_app.logger.info('client:%s connect success, correspond user_info:[id: %s, name:%s]',
                            request.sid, dealer_user.id, dealer_user.name)

    emit('sync_resp_info', {'code': 0, 'message': 'connection success', 'data':{'event': 'connect'}})

    print('----socketio- connect success--------', request.sid)


@socketio.on('join_auction_room', namespace='/auction_car')
def join_auction_room(message):
    print(message)
    room_name = _get_auction_room_name(message['room_id'])
    join_room(room_name)
    current_app.logger.info('auction_room: dealer[%s] enter room[%s]', request.sid, room_name)
    emit('sync_resp_info', {'code': 0, 'message': 'enter room success', 'data':{'event': 'join_auction_room'}})


@socketio.on('leave_auction_room', namespace='/auction_car')
def leave_auction_room(message):
    print(message)
    room_name = _get_auction_room_name(message['room_id'])
    leave_room(room_name)
    current_app.logger.info('auction_room: dealer[%s] leave room[%s]', request.sid, room_name)
    emit('sync_resp_info', {'code': 0, 'message': 'leave room success', 'data':{'event': 'leave_auction_room'}})


@socketio.on('close_auction_room', namespace='/auction_car')
def close_auction_room(message):
    room_name = _get_auction_room_name(message['room_id'])
    close_room(room_name)
    current_app.logger.info('auction_room: close room[%s]', room_name)


@socketio.on('disconnect', namespace='/auction_car')
def disconnect_request():
    disconnect()


@socketio.on('ping_time', namespace='/auction_car')
def ping_pong():
    emit('pong_time', {'data':{'server_time': datetime_to_str(datetime.now())}})


@socketio.on('bid_info_broadcast', namespace='/auction_car')
def bid_info_broadcast(message):
    room_name = _get_auction_room_name(message['room_id'])
    emit('auction_bid_info_broadcast', {'data': message['data']}, room=room_name, broadcast=True)