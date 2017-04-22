#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import json

import flask

from core import gomoku


app = flask.Flask(__name__)


@app.route('/')
def index():
    return open('index.html').read()


@app.route('/chessboards/<table_id>/')
def chessboard(table_id):
    """获取某局对战信息"""
    game_table = gomoku.GameTable(table_id)
    if not game_table.is_ongoing():
        game_table.reserve()
        os.system(('nohup python core/gomoku.py -w %s '
                   './players/pysnow530 ./players/random1 '
                   '>>log/gomoku.out&') % (table_id,))
        return flask.jsonify(None)

    return flask.jsonify(game_table.info)


if __name__ == '__main__':
    app.run(debug=True)
