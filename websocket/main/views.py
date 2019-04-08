# -*- coding: utf-8 -*-
'''
auction-we-web.main.views
------------------

main相关视图 仅支持根目录的url_for
'''

from . import main


@main.route('/')
def index():
    return '<h1>hello there</h1>'


@main.route('/health')
def health():
    return 'OK'