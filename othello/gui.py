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

# MODE
MENU = -1
HUMAN = 0
CPU = 1

# CPULevel
EASY = 0
NORMAL = 1

# 手の表現
IN_ALPHABET = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
IN_NUMBER = ['1', '2', '3', '4', '5', '6', '7', '8']
################################

board = App.Board()
class OthelloGame:
    def __init__(self):
        self.PlayMode = MENU
        self.CPULevel = EASY
    # 初級
game = OthelloGame()
def function_B():
    # データ上のリセット
    board.reset()
    game.PlayMode = CPU
    game.CPULevel = EASY
    # 見た目のリセット
    reset()
    # playCPU()
# # 中級
# def function_I():
#     board.reset()
#     game.PlayMode = CPU
#     game.CPULevel = 2
#     reset()
#     playCPU()
# 対人
def function_H():
    board.reset()
    game.PlayMode = HUMAN
    reset()


################################################
################メイン画面の生成################
root = Tk()
root.title("オセロ")
root.resizable(0,0)     #サイズ変更不可にする

################################################
################メニュー################

# メニューオブジェクト
menu_ROOT = Menu(root)
#メインウィンドウ（root）のmenuに作成したメニューオブジェクトを設定し更新
root.configure(menu = menu_ROOT)

# ゲームメニューを作る
menu_GAME = Menu(menu_ROOT, tearoff = False)

menu_ROOT.add_cascade(label = 'ゲーム(G)', under = 4, menu = menu_GAME)
# サブメニュー
menu_COM = Menu(menu_GAME, tearoff = False)
menu_GAME.add_cascade(label = "コンピュータ対戦(C)", under = 3, menu = menu_COM)
# menu_COM.add_command(label = "初級(B)", under = 3)
menu_COM.add_command(label = "初級(B)", under = 3, command=function_B)
# menu_COM.add_command(label = "中級(I)", under = 3, command=function_I)
menu_GAME.add_command(label = "対人(H)", under = 3, command=function_H)

menu_ROOT.add_command(label = "終了(X)", under = 3, command=quit)

################################################
################フレームオブジェクト作成################
#外枠のフレーム作成
root_frame = Frame(root, relief = 'groove', borderwidth = 5, bg = 'LightGray')
#上部ステータス画面のフレーム作成
status_frame = Frame(root_frame, height = 50, relief = 'sunken', borderwidth=3, bg= 'LightGray')
#下部ゲーム画面のフレーム作成
game_frame = Frame(root_frame, height = 300, relief = 'sunken', borderwidth=3, bg= 'LightGray')
#それぞれのフレームを配置する。ステータス画面とゲーム画面は上下左右それぞれ余白を少し設ける
root_frame.pack()
status_frame.pack(pady = 5, padx = 5, fill = 'x')
game_frame.pack(pady = 5, padx = 5)


################################################
def renew():
    SUM = str(board.getSum())
    for s in range(1, 9):
        for t in range(1, 9):
            # color = board.RawBoard[t, s]
            ####### s,t順番不明
            stone = SUM[(s + 8*(t-1))-1]
            if int(stone) == 2:
                frame_list[s-1][t-1].configure(relief = 'ridge', bd = '1', bg = 'White')
            if int(stone) == BLACK:
                frame_list[s-1][t-1].configure(relief = 'ridge', bd = '1', bg = 'Black')

def reset():
    SUM = str(board.getSum())
    for s in range(1, 9):
        for t in range(1, 9):
            # color = board.RawBoard[t, s]
            stone = SUM[(s + 8*(t-1))-1]
            if int(stone) == 2:
                frame_list[s-1][t-1].configure(relief = 'ridge', bd = '1', bg = 'White')
            if int(stone) == BLACK:
                frame_list[s-1][t-1].configure(relief = 'ridge', bd = '1', bg = 'Black')
            if int(stone) == 0:
                frame_list[s-1][t-1].configure(relief = 'raised', bd = '3', bg = 'Green')

# # マス目
def left_click(event):
    if game.PlayMode == MENU:
        pass
    else:
        y = event.widget.num[0]
        x = event.widget.num[1]
        x = IN_ALPHABET[x-1]
        IN = str(x+str(y))
        print(IN)
        if not board.put(IN):
            board.display()
            renew()
            # print(board.CurrentColor)
            pass
        else:
            board.put(IN)
            board.display()
            # print(board.CurrentColor)
            renew()
            if board.isGameOver():
                print("end")
                B, W = counter()
                dif = B - W
                if dif > 0:
                    print('黒の勝ち')
                elif dif < 0:
                    print('白の勝ち')
                else:
                    print('引き分け')
            elif game.PlayMode == HUMAN:
                if board.MovablePos == 0:
                    board.CurrentColor = - board.CurrentColor
                    board.initMovable()
                    print('パスしました')
                else:
                    pass
            else:
                computer()
                # print("test_computer")

def computer():
    #白が打てるか
    board.initMovable()
    if board.MovablePos == 0:
        board.CurrentColor = - board.CurrentColor
        board.initMovable()
        print('パスしました')
    else:
        # s, t = board.randomInput()
        bit = board.randomInput()
        # board.move(s, t)
        board.putBit(bit)
        board.display()
        print()
        renew()

        # 黒が打てるか
        if board.MovablePos != 0:
            pass
        else:
            while board.MovablePos == 0:
                if board.isGameOver():
                    print("end")
                    B, W = counter()
                    dif = B - W
                    if dif > 0:
                        print('黒の勝ち')
                    elif dif < 0:
                        print('白の勝ち')
                    else:
                        print('引き分け')
                    break
                else:
                    board.CurrentColor = - board.CurrentColor
                    board.initMovable()
                    bit = board.randomInput()
                    board.putBit(bit)
                    board.display()
                    print()
                    renew()



def quit():
    root.destroy()
def counter():
    count_black = board.bitCount(board.BitBoard[BLACK])
    count_white = board.bitCount(board.BitBoard[WHITE])
    return count_black, count_white



#各マス目に番号を振っておくといろいろ便利なのでそれ用の変数iを定義する
i = 0
#繰り返し作成したフレーム格納用リスト
frame_list = []
#for文の入れ子構造にして、9×9回繰り返す
for y in range(1, 9):
    x_frame = []
    for x in range(1, 9):
        frame = Frame(game_frame, width = 50, height = 50, bd = 3, relief = 'raised', bg = 'green')
        frame.bind("<1>", left_click)
        frame.num = list([x, y])
        #作成したフレームをフレームのリストに格納する。これでインデックス番号でアクセスすることで
        #各フレームを操作できる
        x_frame.append(frame)
        #gridを使ってフレームを配置する。packと違いgridを使うと、タテヨコ均等に9列x9列に配置できる
        #rowでヨコ、columnでタテを指定している
        frame.grid(row=x, column=y)
        SUM = str(board.getSum())

        stone = SUM[(x + 8*(y-1))-1]
        # print(stone)
    frame_list.append(x_frame)

################


################
root.mainloop()
