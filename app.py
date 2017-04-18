#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import json

import flask


app = flask.Flask(__name__)


@app.route('/')
def index():
    return open('index.html').read()


@app.route('/chessboards/<id>/')
def chessboard(id):
    """获取某局对战信息"""
    data_path = 'data/%s.json' % (id,)
    if not os.path.exists(data_path):
        pass            # 不存在，新开一局

    info = json.load(open(data_path))
    if info['result'] != 'ongoing':
        pass            # 已结束，新开一局

    # 正在对战，返回对战信息
    return flask.jsonify(info)


if __name__ == '__main__':
    app.run()
