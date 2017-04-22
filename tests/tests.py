#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import unittest

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from core import gomoku


class BoardTestCase(unittest.TestCase):

    def setUp(self):
        self.board = gomoku.Board(3, 3, [[' ', ' ', ' '],
                                         [' ', 'a', 'a'],
                                         [' ', 'a', ' ']])

    def test_full(self):
        self.assertTrue(self.board.full() == False)

        full_board = gomoku.Board(3, 3, [['a', 'a', 'a'],
                                         ['a', 'a', 'a'],
                                         ['a', 'a', 'a']])
        self.assertTrue(full_board.full() == True)

    def test_get(self):
        self.assertTrue(self.board.get(0, 0) == ' ')
        self.assertTrue(self.board.get(2, 2) == ' ')

        self.assertTrue(self.board.get(-1, 2) is None)
        self.assertTrue(self.board.get(1, -2) is None)
        self.assertTrue(self.board.get(1, 3) is None)
        self.assertTrue(self.board.get(3, 1) is None)

    def test_is_piece(self):
        board = gomoku.Board(3, 3, [[' ', ' ', ' '],
                                    [' ', 'a', 'a'],
                                    [' ', 'a', ' ']])

        self.assertTrue(self.board.is_piece(1, 1, 'a'))
        self.assertTrue(self.board.is_piece(1, [1, 2], 'a'))
        self.assertTrue(self.board.is_piece([1, 2], 1, 'a'))
        self.assertTrue(self.board.is_piece([2, 1], [1, 2], 'a'))

        self.assertFalse(self.board.is_piece(0, 0, 'a'))
        self.assertFalse(self.board.is_piece(1, [0, 1], 'a'))
        self.assertFalse(self.board.is_piece([0, 1], 1, 'a'))
        self.assertFalse(self.board.is_piece([2, 1], [0, 1], 'a'))

        self.assertFalse(self.board.is_piece(1, -1, 'a'))
        self.assertFalse(self.board.is_piece(1, [-1, 1, 2], 'a'))
        self.assertFalse(self.board.is_piece([-1, 1, 2], 1, 'a'))
        self.assertFalse(self.board.is_piece([-1, 2, 1], [-1, 1, 2], 'a'))


if __name__ == '__main__':
    unittest.main()
