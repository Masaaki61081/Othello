import numpy as np
import random
import time
from tkinter import *
from tkinter import ttk

import bitboard as App

# 定数
EMPTY = 0
WHITE = -1
BLACK = 1
BOARD_SIZE = 64

HORIZONTAL_BOARD = 0x7e7e7e7e7e7e7e7e
VERTICAL_BOARD = 0x00FFFFFFFFFFFF00
ALLSIDE_BOARD = 0x007e7e7e7e7e7e00

MAX_TURNS = 60

# 手の表現
IN_ALPHABET = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
IN_NUMBER = ['1', '2', '3', '4', '5', '6', '7', '8']

# ボートインスタンスの作成
board = App.Board()

# テスト用初期盤面
# board.RawBoard = np.array([
#     [2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
#     [2, 1, 1, 1, 1, 1, 1, 1, 1, 2],
#     [2, 1, 1,-1,-1, 1, 1, 1, 1, 2],
#     [2, 1, 1,-1,-1,-1, 1,-1, 1, 2],
#     [2, 1, 1, 1,-1, 1, 1, 1, 1, 2],
#     [2, 1, 1,-1, 1,-1,-1, 0, 1, 2],
#     [2, 1,-1, 1, 1, 1, 1, 1, 1, 2],
#     [2, 1, 0,-1,-1,-1,-1, 1, 1, 2],
#     [2, 1, 0, 0, 0, 0,-1, 1, 1, 2],
#     [2, 2, 2, 2, 2, 2, 2, 2, 2, 2]])
# board.initMovable()

# 手番ループ
while True:
    # 盤面の表示
    board.display()

    # 手番の表示
    if board.CurrentColor == BLACK:
        print('●の番です:', end = "")
    else:
        print('○の番です:', end = "")
    print()

    # CPUかPlayerが入力
    if board.CurrentColor == BLACK:
        print('手を入力してください(例:f5):', end='')
        IN = input()
    else:
        print('手を入力してください(例:f5):', end='')
        # IN = board.randomInput()
        IN = str(input())
        print(IN)
    print()
    # 入力手をチェック
    if board.checkIN(IN):
        pass
        # x = IN_ALPHABET.index(IN[0]) + 1
        # y = IN_NUMBER.index(IN[1]) + 1
    else:
        print('正しい形式(例:f5)で入力してください')
        continue

    # 手を打つ
    if not board.put(IN):
        print('そこには置けません')
        continue
    # else:
    #     board.put(IN)
    #     print("手を打つ", IN)

    # 終局判定
    if board.isGameOver():
        board.display()
        print('おわり')
        break

    # パス
    if board.MovablePos == 0:
        board.CurrentColor = - board.CurrentColor
        board.initMovable()
        print('パスしました')
        print()
        continue

# ゲーム終了後
print()

# 各色の数
# count_black = np.count_nonzero(board.RawBoard[:, :] == BLACK)
# count_white = np.count_nonzero(board.RawBoard[:, :] == WHITE)
Black_Score, White_Score, winner = board.getResult()

print('●', Black_Score)
print('○', White_Score)

# dif = count_black - count_white
if winner == BLACK:
    print('●の勝ち')
elif winner == WHITE:
    print('○の勝ち')
else:
    print('引き分け')
