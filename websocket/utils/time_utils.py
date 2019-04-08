# -*- coding: utf-8 -*-

import re
import six
from datetime import (
    datetime,
    date,
)


def to_text(value, encoding='utf-8'):
    """
    将 value 转为 unicode，默认编码 utf-8
    @param value: 待转换的值
    @param encoding: 编码
    """
    if not value:
        return ''
    if isinstance(value, six.text_type):
        return value
    if isinstance(value, six.binary_type):
        return value.decode(encoding)
    return six.text_type(value)


def obj_to_datetime(obj):
    if obj is None:
        return None

    if type(obj) is date:
        return datetime(obj.year, obj.month, obj.day)

    if type(obj) is datetime:
        return obj

    obj = to_text(obj)
    if re.match('^\d{4,4}-\d{1,2}-\d{1,2}$', obj):
        return datetime.strptime(obj, '%Y-%m-%d')
    elif re.match('^\d{4,4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2}$', obj):
        return datetime.strptime(obj, '%Y-%m-%d %H:%M:%S')
    else:
        return None


def datetime_to_str(d):
    if not d:
        return None

    if isinstance(d, str):
        d = obj_to_datetime(d)

    if d:
        return d.strftime('%Y-%m-%d %H:%M:%S')
    else:
        return None


def date_to_str(d):
    if not d:
        return None

    if isinstance(d, str):
        d = obj_to_date(d)

    if d:
        return d.strftime('%Y-%m-%d')
    else:
        return None


def obj_to_date(obj):
    if obj is None:
        return None

    if type(obj) is date:
        return obj

    if type(obj) is datetime:
        return obj.date()

    obj = to_text(obj)
    if re.match('^\d{4,4}-\d{1,2}-\d{1,2}$', obj):
        return datetime.strptime(obj, '%Y-%m-%d').date()
    elif re.match('^\d{4,4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2}$', obj):
        return datetime.strptime(obj, '%Y-%m-%d %H:%M:%S').date()
    else:
        return None