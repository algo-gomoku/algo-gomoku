#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import json
import time
import getopt
import subprocess
import itertools
import logging


logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] %(asctime)s -- %(message)s',
                    filemode='a+')


# 假设终端背景是黑色
BLACK_PIECE_CHAR = '○'
WHITE_PIECE_CHAR = '●'
EMPTY_CHAR = ' '


def main():
    """入口"""
    board = Board(19, 19)
    player1 = Player(board, BLACK_PIECE_CHAR, get_player_name(1))
    player2 = Player(board, WHITE_PIECE_CHAR, get_player_name(2))

    table_id = OptUtils.parse_table_id()
    game_table = GameTable(table_id, board, player1, player2)

    while True:

        time.sleep(1)

        player1.play(player2.piece_char)
        if player1.wined():
            game_table.result = '%s win!' % (player1.short_name,)
            game_table.dump()
            sys.exit(0)

        if board.full():
            game_table.result = 'Draw!'
            game_table.dump()
            sys.exit(0)

        game_table.next = {
            'piece_char': player1.piece_char,
            'position': {
                'x': player1.last_pos[0],
                'y': player1.last_pos[1],
            }
        }
        game_table.dump()

        time.sleep(1)

        player2.play(player1.piece_char)
        if player2.wined():
            game_table.result = '%s win!' % (player2.short_name,)
            game_table.dump()
            sys.exit(0)

        if board.full():
            game_table.result = 'Draw!'
            game_table.dump()
            sys.exit(0)

        game_table.next = {
            'piece_char': player2.piece_char,
            'position': {
                'x': player2.last_pos[0],
                'y': player2.last_pos[1],
            }
        }
        game_table.dump()


class Player(object):
    """玩家"""

    last_pos = None

    def __init__(self, board, piece_char, player_name):
        self.board = board
        self.piece_char = piece_char
        self.name = player_name

    def play(self, enemy_piece_char):
        """下子，该接口会调用命令行传输过来的算法文件，并生成下个子的位置"""
        info = {
            'data': self.board.data,
            'width': self.board.width,
            'height': self.board.height,
            'my_piece_char': self.piece_char,
            'enemy_piece_char': enemy_piece_char,
            'empty_char': EMPTY_CHAR,
        }

        next_pos_str = subprocess.check_output([self.name, json.dumps(info)])
        next_pos = json.loads(next_pos_str)
        x, y = next_pos['x'], next_pos['y']
        self.board.set(x, y, self.piece_char)

        self.last_pos = (x, y)

    def wined(self):
        """根据游戏规则判断是否赢得胜利"""
        width = self.board.width
        height = self.board.height

        for i, j in itertools.product(range(height), range(width)):

            # 检测是否有横向五个相连的棋子
            if self.board.is_piece(i, range(j, j+5), self.piece_char):
                return True

            # 检测是否有竖向五个相连的棋子
            if self.board.is_piece(range(i, i+5), j, self.piece_char):
                return True

            # 检测是否有左上到右下斜向五个相连的棋子
            if self.board.is_piece(range(i, i+5), range(j, j+5),
                                   self.piece_char):
                return True

            # 检测是否有左下到右上斜向五个相连的棋子
            if self.board.is_piece(range(i, i-5, -1), range(j, j+5),
                                   self.piece_char):
                return True

        return False

    @property
    def short_name(self):
        """根据传入的文件名获取basename"""
        return os.path.basename(self.name)


class Board(object):
    """棋盘"""

    def __init__(self, width, height, data=None):
        """创建一个棋盘"""
        self.width = width
        self.height = height

        self.data = []
        for i in range(self.height):
            line = []
            for j in range(self.width):
                if data is not None and len(data) > i and len(data[i]) > j:
                    line.append(data[i][j])
                else:
                    line.append(' ')
            self.data.append(line)

    def full(self):
        """是否已填充满"""
        for i in range(self.height):
            for j in range(self.width):
                if self.data[i][j] == ' ':
                    return False

        return True

    def get(self, x, y):
        """获取某个位置的棋子"""
        if not (0 <= x < self.height and 0 <= y < self.width):
            return None
        else:
            return self.data[x][y]

    def set(self, x, y, piece_char):
        """放子"""
        char = self.get(x, y)
        if char is None:
            sys.exit(1)
        elif char != ' ':
            sys.exit(2)
        else:
            self.data[x][y] = piece_char

    def is_piece(self, x, y, piece_char):
        """判断某个位置或某些位置是否是我们的棋子
        is_piece([(0, 1), (0, 2), (0, 3), (0, 4)])
        is_piece(0, 0)
        is_piece([0, 1, 2], 0)
        is_piece(0, [0, 1, 2])
        """
        if y is None:
            positions = x
        else:
            if isinstance(x, int) and isinstance(y, int):
                positions = [(x, y)]
            elif isinstance(x, list) and isinstance(y, int):
                positions = [(i, y) for i in x]
            elif isinstance(x, int) and isinstance(y, list):
                positions = [(x, j) for j in y]
            elif isinstance(x, list) and isinstance(y, list):
                positions = zip(x, y)
            else:
                raise Exception('is_piece(%r, %r) unimplement!' % (type(x),
                                                                   type(y)))

        return all([self.get(xx, yy) == piece_char for (xx, yy) in positions])


class GameTable(object):
    """模拟游戏桌的概念，支持多个棋局同时对战"""

    table_id = None

    board = None
    player1 = None
    player2 = None

    result = None
    players = None
    chessboard = None
    next = None

    def __init__(self, table_id, board=None, player1=None, player2=None):
        self.table_id = table_id

        if board is not None:
            self.board = board
        if player1 is not None:
            self.player1 = player1
        if player2 is not None:
            self.player2 = player2

        # 从文件装载内容到该对象
        table_info = self.info
        if table_info is not None:
            self.result = table_info.get('result')
            self.players = table_info.get('players')
            self.chessboard = table_info.get('chessboard')
            self.next = table_info.get('next')

    @property
    def data_file_path(self):
        """获取该桌对应的数据文件"""
        data_path = 'data/%s.json' % (self.table_id,)

        return data_path

    def is_ongoing(self):
        """判断该桌是否正在进行中。一张桌，只有在一局完成后过10s才可用。"""
        if self.result == 'ongoing' or self.mtime > time.time() - 10:
            return True
        else:
            return False

    def reserve(self):
        """预订该桌"""
        info = {
            'result': 'ongoing'
        }

        json.dump(info, open(self.data_file_path, 'w+'))

    @property
    def info(self):
        """获取table文件内保存的信息。如果文件不存在，返回None"""
        if os.path.exists(self.data_file_path):
            return json.load(open(self.data_file_path))
        else:
            return None

    @property
    def mtime(self):
        """获取table文件最后修改时间"""
        if os.path.exists(self.data_file_path):
            return os.stat(self.data_file_path).st_mtime
        else:
            return None

    def dump(self):
        """更新数据文件"""
        assert self.board is not None
        assert self.player1 is not None
        assert self.player2 is not None

        if self.players is None:
            self.players = [
                    {
                        'name': os.path.basename(self.player1.name),
                        'piece_char': self.player1.piece_char,
                        'used_time': 0.0,
                    },
                    {
                        'name': os.path.basename(self.player2.name),
                        'piece_char': self.player2.piece_char,
                        'used_time': 0.0,
                    }
            ]

        if self.result is None:
            self.result = 'ongoing'

        self.chessboard = []
        for i in range(19):
            line = []
            for j in range(19):
                line.append(self.board.get(i, j))
            self.chessboard.append(line)

        json.dump({
            'players': self.players,
            'chessboard': self.chessboard,
            'result': self.result,
            'next': self.next,
        }, open(self.data_file_path, 'w+'), indent=4)


class OptUtils(object):
    """参数工具类"""

    @staticmethod
    def get_args():
        """获取玩家算法文件"""
        opts, args = getopt.getopt(sys.argv[1:], 'w:')

        return args

    @staticmethod
    def parse_table_id():
        """是否使用web模式"""
        opts, args = getopt.getopt(sys.argv[1:], 'w:')

        for k, v in opts:
            if k == '-w':
                return v

        return None


def get_player_name(id_):
    """获取某个玩家的名字"""
    name = OptUtils.get_args()[id_-1]

    return name


if __name__ == '__main__':
    main()
