#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import subprocess
import tempfile
import json
import itertools


# 假设我们的终端背景是黑色
BLACK_PIECE_CHAR = '○'
WHITE_PIECE_CHAR = '●'
EMPTY_CHAR = ' '


def main():
    """入口"""
    board = Board(19, 19)
    player1 = Player(board, BLACK_PIECE_CHAR, get_player_name(1))
    player2 = Player(board, WHITE_PIECE_CHAR, get_player_name(2))

    while True:

        player1.play(player2.piece_char)
        if player1.win():
            print >>sys.stderr, '%s win!' % (player1.name,)
            sys.exit()

        if board.full():
            print >>sys.stderr, 'Draw!'
            sys.exit()

        player2.play(player1.piece_char)
        if player2.win():
            print '%s win!' % (player2.name,)
            sys.exit()

        if board.full():
            print >>sys.stderr, 'Draw!'
            sys.exit()


def get_player_name(id_):
    """获取某个玩家的名字"""
    try:
        name = sys.argv[id_]
    except IndexError:
        print >>sys.stderr, '\n'.join([
            'Error: 玩家%d不存在',
            '',
            'Usage: gomoku PLAYER1 PLAYER2',
            'NOTE: 其中PLAYER是可执行算法文件的文件路径'
        ]) % (id_,)
        sys.exit(-1)
    else:
        return name


class Player(object):
    """玩家"""

    def __init__(self, board, piece_char, player_name):
        self.board = board
        self.piece_char = piece_char
        self.name = player_name

    def play(self, enemy_piece_char):
        """下子，该接口会调用命令行传输过来的算法文件，并生成下个子的位置"""
        info = {
            'data': self.board.grids,
            'width': self.board.width,
            'height': self.board.height,
            'my_piece_char': self.piece_char,
            'enemy_piece_char': enemy_piece_char,
            'empty_char': EMPTY_CHAR,
        }

        board_context_file = tempfile.mktemp()
        json.dump(info, open(board_context_file, 'w+'))

        next_pos_str = subprocess.check_output([self.name, board_context_file])
        next_pos = json.loads(next_pos_str)
        x, y = next_pos['x'], next_pos['y']
        print '%s put (%d, %d) %s!' % (self.name, x, y, self.piece_char)
        self.board.set(x, y, self.piece_char)

    def win(self):
        """根据游戏规则判断是否赢得胜利"""
        width = self.board.width
        height = self.board.height
        grids = self.board.grids

        # 检测是否有横向五个相连的棋子
        for i, j in itertools.product(range(height-4), range(width-4)):
            if all([grids[ii][jj] == self.piece_char
                    for ii, jj in [(i, j), (i, j+1), (i, j+2),
                                   (i, j+3), (i, j+4)]]):
                return True

        # 检测是否有竖向五个相连的棋子
        for i, j in itertools.product(range(height-4), range(width-4)):
            if all([grids[ii][jj] == self.piece_char
                    for ii, jj in [(i, j), (i+1, j), (i+2, j),
                                   (i+3, j), (i+4, j)]]):
                return True

        # 检测是否有左上到右下斜向五个相连的棋子
        for i, j in itertools.product(range(height-4), range(width-4)):
            if all([grids[ii][jj] == self.piece_char
                    for ii, jj in [(i, j), (i+1, j+1), (i+2, j+2),
                                   (i+3, j+3), (i+4, j+4)]]):
                return True

        # 检测是否有左下到右上斜向五个相连的棋子
        for i, j in itertools.product(range(4, height), range(width-4)):
            if all([grids[ii][jj] == self.piece_char
                    for ii, jj in [(i, j), (i-1, j+1), (i-2, j+2),
                                   (i-3, j+3), (i-4, j+4)]]):
                return True

        return False


class Board(object):
    """棋盘"""

    def __init__(self, width, height):
        """创建一个棋盘"""
        self.width = width
        self.height = height

        self.grids = []
        for i in range(self.height):
            line = []
            for j in range(self.width):
                line.append(' ')
            self.grids.append(line)

    def full(self):
        """是否已填充满"""
        for i in range(self.height):
            for j in range(self.width):
                if self.grids[i][j] == ' ':
                    return False

        return True

    def set(self, x, y, piece_char):
        """放子"""
        if self.grids[x][y] != ' ':
            print >>sys.stderr, '位置(%d, %d)已有子%s，不能放子！' % (
                x, y, self.grids[x][y])
            sys.exit(1)
        else:
            self.grids[x][y] = piece_char

        self.update_display()

    def update_display(self):
        """更新棋盘显示"""
        for i in range(self.height):
            for j in range(self.width):
                print '%s ' % (self.grids[i][j],),
            print
        print '---' * self.width


if __name__ == '__main__':
    main()
