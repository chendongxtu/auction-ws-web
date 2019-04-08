# -*- coding:utf-8 -*-

from flask import render_template
from . import test

@test.route('/', methods=['GET', 'POST'])
def index():
    print('---------------test---------')
    return render_template('index.html')


