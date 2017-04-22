#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import json

import flask

import gomoku


app = flask.Flask(__name__)


@app.route('/')
def index():
    return open('index.html').read()


@app.route('/chessboards/<id>/')
def chessboard(id):
    """获取某局对战信息"""
    game_table = gomoku.Table(id)
    if not game_table.is_ongoing():
        game_table.reserve()
        os.system('nohup ./gomoku -w %s ./players/{pysnow530,random1}&' % (id,))
        return flask.jsonify(None)

    return flask.jsonify(game_table.info)


if __name__ == '__main__':
    app.run()
