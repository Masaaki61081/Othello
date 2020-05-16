import numpy as np
import random

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
################################
# ボード
class Board:

    def __init__(self):
        # # 手番
        self.Turns = 0
        # 手番の色
        self.CurrentColor = BLACK
        # 得点
        self.Score = {BLACK:2, WHITE:2}
        # おける場所と方向
        self.MovablePos = int()
        # self.MovableDir = np.zeros((BOARD_SIZE + 2, BOARD_SIZE + 2),  dtype=int)

        # self.BitBoard_B = 0x0000001008000000
        # self.BitBoard_W = 0x0000000810000000
        self.BitBoard = {BLACK:0x0000001008000000, WHITE:0x0000000810000000}
        self.BitBoard[BLACK] = 0x0000001008000000
        self.BitBoard[WHITE] = 0x0000000810000000

        # self.MovablePos = 0x0000000000000000

        self.initMovable()

    def initMovable(self):
        # MovablePosの初期化
        # self.MovablePos = int(0)
        # color = self.CurrentColor
        self.MovablePos = self.checkPut(self.CurrentColor)

    def getSum(self):
        B = bin(self.BitBoard[BLACK])
        W = bin(self.BitBoard[WHITE])
        B = str(B)
        W = str(W)
        dif = 66 - len(B) + 2
        maru = str(0) * dif
        B = maru + B[2:]
        B = int(B)

        dif = 66 - len(W) + 2
        maru = str(0) * dif
        W = maru + W[2:]
        W = int(W)

        SUM = str(B + W * 2)
        dif = 64 - len(SUM)
        maru = str(0) * dif
        SUM = maru + SUM
        return SUM
    def reset(self):
        # 盤の初期値
        self.BitBoard = {BLACK:0x0000001008000000, WHITE:0x0000000810000000}
        self.BitBoard[BLACK] = 0x0000001008000000
        self.BitBoard[WHITE] = 0x0000000810000000
        # 手番
        self.Turns = 0
        # 手番の色
        self.CurrentColor = BLACK
        # おける場所と方向
        self.MovablePos = int()
        self.initMovable()
    def display(self):
        SUM = self.getSum()
        print()
        # for i in range(7):
        #     print(SUM[(8*i+2):(8*i+10)])
        print(' a b c d e f g h')
        for i in range(64):
            if i % 8 == 0:
                print(int(i/8) + 1, end="")



            stone = int(SUM[i])
            if stone == EMPTY:
                print('□', end="")
            elif stone == 2:
                print('○', end="")
            elif stone == BLACK:
                print('●', end="")
            if (i + 1) % 8 == 0:
                print()
        # 改行
        print()
# 座標変換
    def coordinaterToBit(self, x, y):
        mask = 0x8000000000000000
        # x
        if x == 'a':
            pass
        elif x == 'b':
            mask = mask >> 1
        elif x == 'c':
            mask = mask >> 2
        elif x == 'd':
            mask = mask >> 3
        elif x == 'e':
            mask = mask >> 4
        elif x == 'f':
            mask = mask >> 5
        elif x == 'g':
            mask = mask >> 6
        elif x == 'h':
            mask = mask >> 7
        else:
            pass
        # y
        y = int(y)
        mask = mask >> ((y-1) * 8)

        return mask
# 着手判定
    def checkPut(self, color):
        PlayerBoard = self.BitBoard[color]
        OpponentBoard = self.BitBoard[- color]
        HorizontalWatchBoard = OpponentBoard & HORIZONTAL_BOARD
        VerticalWatchBoard = OpponentBoard & VERTICAL_BOARD
        AllSideWatchBoard = OpponentBoard & ALLSIDE_BOARD
        BlankBoard = ~(PlayerBoard | OpponentBoard)
        tmp = int()
        LegalBoard = int()

        # 左
        tmp = HorizontalWatchBoard & (PlayerBoard << 1)
        tmp = tmp | HorizontalWatchBoard & (tmp << 1)
        tmp = tmp | HorizontalWatchBoard & (tmp << 1)
        tmp = tmp | HorizontalWatchBoard & (tmp << 1)
        tmp = tmp | HorizontalWatchBoard & (tmp << 1)
        tmp = tmp | HorizontalWatchBoard & (tmp << 1)
        LegalBoard = LegalBoard | BlankBoard & (tmp << 1)

        # 右
        tmp = HorizontalWatchBoard & (PlayerBoard >> 1)
        tmp = tmp | HorizontalWatchBoard & (tmp >> 1)
        tmp = tmp | HorizontalWatchBoard & (tmp >> 1)
        tmp = tmp | HorizontalWatchBoard & (tmp >> 1)
        tmp = tmp | HorizontalWatchBoard & (tmp >> 1)
        tmp = tmp | HorizontalWatchBoard & (tmp >> 1)
        LegalBoard = LegalBoard | BlankBoard & (tmp >> 1)

        # 上
        tmp = VerticalWatchBoard & (PlayerBoard << 8)
        tmp = tmp | VerticalWatchBoard & (tmp << 8)
        tmp = tmp | VerticalWatchBoard & (tmp << 8)
        tmp = tmp | VerticalWatchBoard & (tmp << 8)
        tmp = tmp | VerticalWatchBoard & (tmp << 8)
        tmp = tmp | VerticalWatchBoard & (tmp << 8)
        LegalBoard = LegalBoard | BlankBoard & (tmp << 8)

        # 下
        tmp = VerticalWatchBoard & (PlayerBoard >> 8)
        tmp = tmp | VerticalWatchBoard & (tmp >> 8)
        tmp = tmp | VerticalWatchBoard & (tmp >> 8)
        tmp = tmp | VerticalWatchBoard & (tmp >> 8)
        tmp = tmp | VerticalWatchBoard & (tmp >> 8)
        tmp = tmp | VerticalWatchBoard & (tmp >> 8)
        LegalBoard = LegalBoard | BlankBoard & (tmp >> 8)

        # 右上
        tmp = AllSideWatchBoard & (PlayerBoard << 7)
        tmp = tmp | AllSideWatchBoard & (tmp << 7)
        tmp = tmp | AllSideWatchBoard & (tmp << 7)
        tmp = tmp | AllSideWatchBoard & (tmp << 7)
        tmp = tmp | AllSideWatchBoard & (tmp << 7)
        tmp = tmp | AllSideWatchBoard & (tmp << 7)
        LegalBoard = LegalBoard | BlankBoard & (tmp << 7)

        # 左上
        tmp = AllSideWatchBoard & (PlayerBoard << 9)
        tmp = tmp | AllSideWatchBoard & (tmp << 9)
        tmp = tmp | AllSideWatchBoard & (tmp << 9)
        tmp = tmp | AllSideWatchBoard & (tmp << 9)
        tmp = tmp | AllSideWatchBoard & (tmp << 9)
        tmp = tmp | AllSideWatchBoard & (tmp << 9)
        LegalBoard = LegalBoard | BlankBoard & (tmp << 9)

        # 右下
        tmp = AllSideWatchBoard & (PlayerBoard >> 9)
        tmp = tmp | AllSideWatchBoard & (tmp >> 9)
        tmp = tmp | AllSideWatchBoard & (tmp >> 9)
        tmp = tmp | AllSideWatchBoard & (tmp >> 9)
        tmp = tmp | AllSideWatchBoard & (tmp >> 9)
        tmp = tmp | AllSideWatchBoard & (tmp >> 9)
        LegalBoard = LegalBoard | BlankBoard & (tmp >> 9)

        # 左下
        tmp = AllSideWatchBoard & (PlayerBoard >> 7)
        tmp = tmp | AllSideWatchBoard & (tmp >> 7)
        tmp = tmp | AllSideWatchBoard & (tmp >> 7)
        tmp = tmp | AllSideWatchBoard & (tmp >> 7)
        tmp = tmp | AllSideWatchBoard & (tmp >> 7)
        tmp = tmp | AllSideWatchBoard & (tmp >> 7)
        LegalBoard = LegalBoard | BlankBoard & (tmp >> 7)

        return LegalBoard
    def put(self, IN):
        IN = str(IN)
        # print("IN", IN)
        x, y = IN[0], IN[1]
        # print("xy", x, y)
        INbit = self.coordinaterToBit(x, y)
        # print(bin(INbit))
        # 置けるかチェック
        if not x in IN_ALPHABET:
            return False
        if int(y) < 1 or 8 < int(y):
            return False
        if self.MovablePos & INbit == 0:
            return False
        # 石を裏返す
        self.reverse(INbit)
        # 手番を進める
        self.Turns += 1
        # 手番を交代する
        self.CurrentColor = - self.CurrentColor
        # MovablePosとMovableDirの更新
        self.initMovable()

        return True
    def putBit(self, INbit):
        # 石を裏返す
        self.reverse(INbit)
        # 手番を進める
        self.Turns += 1
        # 手番を交代する
        self.CurrentColor = - self.CurrentColor
        # MovablePosとMovableDirの更新
        self.initMovable()

        return True



# 反転全体
    def reverse(self, put):
        PlayerBoard = self.BitBoard[self.CurrentColor]
        OpponentBoard = self.BitBoard[- self.CurrentColor]
        # print(put)
        # print(PlayerBoard,OpponentBoard)
        # 反転盤
        rev = 0x0 # 各方向の合計
        for k in range(8):
            rev_ = 0x0 # k方向に進む時の合計
            mask = self.transfer(put, k) # 着手点からk方向に進む
            while (mask != 0) & ((mask & OpponentBoard) != 0): # 相手の石がなくなるまで
                rev_ = rev_ | mask
                mask = self.transfer(mask, k)
            if (mask & PlayerBoard) != 0: # 対岸に自分の石がある場合のみ反転
                rev = rev | rev_
        PlayerBoard = PlayerBoard ^ (put | rev) # 置いたところと反転部分
        OpponentBoard = OpponentBoard ^ rev # 反転した部分は排除
        self.BitBoard[self.CurrentColor] = PlayerBoard
        self.BitBoard[- self.CurrentColor] = OpponentBoard
        # self.Turns += 1
        # print("good")

# 着手の各方向へのシフト
    def transfer(self, put, k):
        if k == 0: # 上
            return (put << 8) & 0xffffffffffffff00
        elif k == 1: # 右上
            return (put << 7) & 0x7f7f7f7f7f7f7f00
        elif k == 2: # 右
            return (put >> 1) & 0x7f7f7f7f7f7f7f7f
        elif k == 3:
            return (put >> 9) & 0x007f7f7f7f7f7f7f
        elif k == 4: # 下
            return (put >> 8) & 0x00ffffffffffffff
        elif k == 5:
            return (put >> 7) & 0x00fefefefefefefe
        elif k == 6:
            return (put << 1) & 0xfefefefefefefefe
        elif k == 7:
            return (put << 9) & 0xfefefefefefefe00
        else:
            return 0
# 結果
    def getResult(self):
        Black_Score = bitCount(self.BitBoard[BLACK])
        White_Score = bitCount(self.BitBoard[WHITE])
        dif = Black_Score - White_Score
        if dif > 0:
            winner = BLACK
        elif dif < 0:
            winner = WHITE
        else:
            winner = 0
        return Black_Score, White_Score, winner

    def bitCount(self, bitboard):
        mask = 0x8000000000000000
        count = 0
        for i in range(BOARD_SIZE):
            if mask & bitboard != 0:
                count += 1
            mask = mask >> 1
        return count
    def checkIN(self, IN):
        if not IN:
            return False
        if len(IN) !=2:
            return False
        if IN[0] in IN_ALPHABET:
            if IN[1] in IN_NUMBER:
                return True
        return False

# ランダム入力
    def randomInput(self):
        # if self.checkSkip == True:
        #     self.CurrentColor = - self.CurrentColor
        #     self.initMovable()
        #     return False

        # おけるところ
        # print("テストrandom")
        grid = self.MovablePos
        # print("テストgrid", bin(grid))
        print(len(bin(grid)))
        grid_str = str(bin(grid))
        mask = 0x1
        bits = list()
        for i in range(len(grid_str)-2):
            if grid & mask:
                bit = self.MovablePos & mask
                bits.append(bit)
                # print("テストrandom", i, bit)
            mask = mask << 1
            # print("test_random:for")
        if len(bits) == 0:
            return False
        # 手を選択
        random_chosen_index = random.randrange(len(bits))
        # x_grid = grids[0][random_chosen_index]
        # y_grid = grids[1][random_chosen_index]
        bit = bits[random_chosen_index]

        # return IN_ALPHABET[x_grid - 1] + IN_NUMBER[y_grid - 1]
        # return x_grid, y_grid
        print(bit)
        return bit

    def isGameOver(self):
        # 60手
        if self.Turns >= MAX_TURNS:
            print("test_isGameOver_MAX_TURNS")
            return True
        # どちらかが打てる時終了しない
        if self.MovablePos != 0:
            return False
        # 相手が打てる時終了しない
        if self.checkPut(-self.CurrentColor) != 0:
            print("test_isGameOver_checkput")
            return False
        # if self.checkPut(-self.CurrentColor) != 0:
        #     return False
        # 余事象は終了
        print("test_isGameOver_True")
        print("test_isGameOver", self.MovablePos, self.checkPut(-self.CurrentColor))
        return True
def TestDisplay(bins):
    mmoo = str(bins)
    sa = 66 - len(mmoo) + 2
    maru = str(0) * sa
    mmoo = maru + mmoo[2:66]
    for i in range(7):
        print(mmoo[(8*i+2):(8*i+10)])


# board = Board()
# board.put("e3")
# board.display()
# BBB = board.BitBoard[BLACK]
# bbb = bin(BBB)
# WWW = board.BitBoard[WHITE]
# www = bin(WWW)
# atai = bin(board.checkPut(board.CurrentColor))
# moji = str(atai)
# print("B")
# TestDisplay(bbb)
# print("W")
# TestDisplay(www)
# print("can")
# TestDisplay(atai)
# print()
# IN = "e3"
# IN = board.coordinaterToBit("e", 3)
# IN = bin(IN)
# TestDisplay(IN)
# board.put("e3")
# board.display()
# put = 0x0000080000000000
# board.reverse(put)
# BBB = board.BitBoard_B
# bbb = bin(BBB)
# WWW = board.BitBoard_W
# www = bin(WWW)
# atai = bin(board.checkPut())
# moji = str(atai)
# print("B")
# TestDisplay(bbb)
# print("W")
# TestDisplay(www)
# print("can")
# TestDisplay(atai)
