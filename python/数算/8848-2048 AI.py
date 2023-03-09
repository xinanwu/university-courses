import numpy as np
import math
import time
import random

# 0519 还没考虑时间问题
# 记得操作都要先复制棋盘
# 除了alpha-beta外可以视情况考虑其他额外的剪枝

# 20200520增：添加了alphabeta剪枝部分，但我也没想好怎么考虑时间问题。如何让所有的搜索在计时停止后立刻停止并且返回当前的最大值？

# 0521 发现node的child完全没用到，先删掉
# 我本来搞错belong的意思了QQ 但我改好了(希望

# 有个想法是先取较深的searchDepth 等快超时的时后 searchDepth - 1 (治标不致本)

# 0524 1200 解决前期落子在敌方的问题，考虑一些特殊情况不需要调用决策树能直接返回移动，决策树减少考虑在敌方落子 新的ee也放进来了

# 0524 1419 让后手搜索深度变成4 先手还是3

# 参数

infinity = 10 ** 9  # 定义这个为无穷 棋盘计分函数不要超过这个数www
maxTime = 5  # 最大时间(s)


class Node:  # 树的节点
    def __init__(self, key, minormax: bool, depth, mode, parent, isFirst, early,searchDepth):  # minormax = True 表示min
        self.key = key  # 棋盘作为key
        self.depth = depth  # 深度
        self.mode = mode
        self.parent = parent
        self.isFirst = isFirst
        if self.depth == searchDepth:  # 到达最大深度则返回棋盘分数
            self.value = chessboardPoint(key, isFirst, early)
        else:  # 还没到最大深度 若为min 先令此数为正无穷，max为负无穷，随者搜索过程调整
            self.value = infinity if minormax else -1 * infinity
        self.minormax = minormax  # 我方操作则max(False) 敌方操作则min(True)
        self.child = []
        self.alpha = -1 * infinity  # alpha 起始为负无穷
        self.beta = infinity  # beta 起始为正无穷

    def addChild(self, key):  # 添加子节点
        if key not in self.child:
            self.child.append(key)

    def updateValue(self, newval):
        self.value = newval

    def updateAlpha(self, newAlpha):
        self.alpha = newAlpha

    def updateBeta(self, newBeta):
        self.beta = newBeta

    def possibleMove(self, currentRound, isFirst, early) -> list:  # 输出下一步的所有可能
        output = []
        if self.mode == "position":  # 下棋
            if self.minormax:  # 敌方下棋
                if early:  # 前期只考虑在自己的领域下棋
                    copyBoard = self.key.copy()
                    if len(copyBoard.getNone(not isFirst)) == 0:
                        pass
                    else:
                        copyBoard.add(not isFirst, self.key.getNext(not isFirst, currentRound))
                        output.append(copyBoard)
                    return output

                elif self.key.getNext(not isFirst, currentRound) != ():  # 若敌方可在敌方领域下棋则添加
                    copyBoard = self.key.copy()  # 复制棋盘后添加下一步位置
                    copyBoard.add(not isFirst, self.key.getNext(not isFirst, currentRound))
                    output.append(copyBoard)
                for position in self.key.getNone(isFirst):  # 我方空位
                    copyBoard = self.key.copy()
                    copyBoard.add(isFirst, position)
                    if chessboardPoint(board=copyBoard, isFirst=not isFirst, early=early) > chessboardPoint(
                            board=self.key, isFirst=not isFirst, early=early):
                        output.append(copyBoard)  # 敌方在我方空位落子 分数要上升才考虑
            else:  # 我方下棋
                if early is True:  # 前期只考虑在自己的领域下棋
                    copyBoard = self.key.copy()  # 复制棋盘后添加下一步位置
                    copyBoard.add(isFirst, self.key.getNext(isFirst, currentRound))
                    output.append(copyBoard)
                    return output

                elif self.key.getNext(isFirst, currentRound) != ():  # 若我方可在我方领域下棋则添加
                    copyBoard = self.key.copy()  # 复制棋盘后添加下一步位置
                    copyBoard.add(isFirst, self.key.getNext(isFirst, currentRound))
                    output.append(copyBoard)
                for position in self.key.getNone(not isFirst):  # 敌方空位
                    copyBoard = self.key.copy()
                    copyBoard.add(not isFirst, position)
                    if chessboardPoint(board=copyBoard, isFirst=isFirst, early=early) > chessboardPoint(board=self.key,
                                                                                                        isFirst=isFirst,
                                                                                                        early=early):
                        output.append(copyBoard)  # 我方在敌方空位落子 分数要上升才考虑
                    output.append(copyBoard)

        else:  # 移动
            if self.minormax:  # 敌方移动
                for direction in range(4):  # 上下左右
                    copyBoard = self.key.copy()
                    if copyBoard.move(not isFirst, direction):  # 如果可移动 则添加到output
                        output.append(copyBoard)
            else:  # 我方移动
                for direction in range(4):  # 上下左右
                    copyBoard = self.key.copy()
                    if copyBoard.move(isFirst, direction):  # 如果可移动 则添加到output
                        output.append(copyBoard)
        return output


def chessboardPoint(board, isFirst, early):  # 棋盘分数(待调整)
    if early and isFirst:
        return ee(board, isFirst) - ee(board, not isFirst)
    elif early and (not isFirst):
        return midscore(board,isFirst)
    else:
        return midscore(board, isFirst)


def newmode(mode, isFirst, minormax) -> str:  # 返回下一模式
    if (mode, isFirst, minormax) in [('position', True, True), ("direction", True, False),
                                     ("direction", False, True), ('position', False, False)]:
        return "direction"
    else:
        return 'position'


# 增加了alpha-beta剪枝
def minimax(nowBoard, currentRound, minormax: bool, mode, isFirst, parent, depth,
            early, searchDepth):  # minimax tree, depth starts from 0
    newRound = currentRound + 1 if newmode(mode, isFirst,
                                           minormax) == 'position' and mode is not 'position' else currentRound
    # 计算下一轮是否要加1
    if depth == searchDepth:  # 搜到底层 直接返回棋盘分数
        node = Node(key=nowBoard, depth=depth, minormax=minormax, mode=mode, parent=parent, isFirst=isFirst,
                    early=early, searchDepth=searchDepth)
        if minormax:  # 本步敌方移动，父节点为max，更新beta
            node.updateBeta(node.value)
        else:  # 本步己方移动，父节点为min，更新alpha
            node.updateAlpha(node.value)
        return node.value

    elif depth == 0:  # 顶层节点  为了方便决策 直接返回下旗位置或移动方向
        point = -1*infinity
        output = ()
        node = Node(key=nowBoard, depth=0, minormax=minormax, mode=mode, parent=None, isFirst=isFirst,
                    early=early, searchDepth=searchDepth)  # 先制造节点
        if mode == 'position':  # 我方下棋
            if node.key.getNext(isFirst, currentRound) != ():  # 若我方可在我方领域下棋则添加
                copyBoard = nowBoard.copy()  # 复制棋盘后添加下一步位置
                copyBoard.add(isFirst, node.key.getNext(isFirst, currentRound))
                point = minimax(nowBoard=copyBoard, currentRound=newRound, minormax=not minormax, isFirst=isFirst,
                                  mode=newmode(mode, isFirst, minormax), depth=1, parent=node, early=early,
                                  searchDepth=searchDepth)
                output = node.key.getNext(isFirst, currentRound)
                # 添加进字典
            for position in nowBoard.getNone(not isFirst):  # 敌方空位
                copyBoard = nowBoard.copy()
                copyBoard.add(not isFirst, position)
                if chessboardPoint(board=copyBoard, isFirst=isFirst, early=early) > chessboardPoint(nowBoard,
                                                                                                    isFirst, early):
                    # 我方在敌方空位落子 分数要上升才考虑
                    if minimax(nowBoard=copyBoard, currentRound=newRound, minormax=not minormax, isFirst=isFirst,
                                      mode=newmode(mode, isFirst, minormax), depth=1, parent=node,
                                      early=early, searchDepth=searchDepth) > point:
                        point = minimax(nowBoard=copyBoard, currentRound=newRound, minormax=not minormax, isFirst=isFirst,
                                      mode=newmode(mode, isFirst, minormax), depth=1, parent=node,
                                      early=early, searchDepth=searchDepth)
                        output = position
            return output

        else:  # 我方移动
            if len(node.possibleMove(currentRound=currentRound, early=early, isFirst=isFirst)) == 1:  # 只有一个可能移动方向
                for direction in range(4):
                    copyBoard = nowBoard.copy()
                    if copyBoard.move(isFirst, direction):
                        return direction

            for direction in range(4):  # 上下左右
                copyBoard = nowBoard.copy()
                if copyBoard.move(isFirst, direction) and minimax(nowBoard=copyBoard, currentRound=newRound, minormax=not minormax, isFirst=isFirst,
                                mode=newmode(mode, isFirst, minormax), depth=1, parent=node,
                                early=early, searchDepth=searchDepth) > point:
                    point = minimax(nowBoard=copyBoard, currentRound=newRound, minormax=not minormax, isFirst=isFirst,
                                mode=newmode(mode, isFirst, minormax), depth=1, parent=node,
                                early=early, searchDepth=searchDepth)
                    output = direction  # 添加进字典
            return output

    else:  # 不是树的底层或顶层,当我方操作（max）时返回下界alpha，反之返回上界beta
        node = Node(key=nowBoard, depth=depth, minormax=minormax, mode=mode, parent=parent, isFirst=isFirst,
                    early=early, searchDepth=searchDepth)  # 先制造节点
        node.updateAlpha(node.parent.alpha)
        node.updateBeta(node.parent.beta)
        if len(node.possibleMove(currentRound=currentRound, isFirst=isFirst, early=early)) is not 0:  # 如果有下一步 添加到子节点
            if minormax:  # min,返回beta值
                for i in node.possibleMove(currentRound=currentRound, isFirst=isFirst, early=early):
                    node.updateBeta(min(node.beta, minimax(nowBoard=i, depth=depth + 1, minormax=not minormax,
                                                           mode=newmode(mode, isFirst, minormax), isFirst=isFirst,
                                                           currentRound=newRound, parent=node, early=early,
                                                           searchDepth=searchDepth)))
                    if node.beta <= node.alpha:  # beta小于等于alpha时剪枝
                        break
                return node.beta
            else:  # max，返回alpha值
                for i in node.possibleMove(currentRound=currentRound, isFirst=isFirst, early=early):
                    node.updateAlpha(max(node.alpha, minimax(nowBoard=i, depth=depth + 1, minormax=not minormax,
                                                             mode=newmode(mode, isFirst, minormax), isFirst=isFirst,
                                                             currentRound=newRound, parent=node, early=early,
                                                             searchDepth=searchDepth)))
                    if node.beta <= node.alpha:
                        break
                return node.alpha
        else:  # 没有下一步
            if minormax:  # min
                node.updateBeta(minimax(nowBoard=nowBoard.copy(), depth=depth + 1, currentRound=newRound,
                                        minormax=not minormax, mode=newmode(mode, isFirst, minormax), isFirst=isFirst,
                                        parent=node, early=early, searchDepth=searchDepth))
                return node.beta
            else:  # max
                node.updateAlpha(minimax(nowBoard=nowBoard.copy(), depth=depth + 1, currentRound=newRound,
                                         minormax=not minormax, mode=newmode(mode, isFirst, minormax), isFirst=isFirst,
                                         parent=node, early=early, searchDepth=searchDepth))
                return node.alpha


class Player:
    def __init__(self, isFirst: bool, array) -> None:
        self.isFirst = isFirst
        self.array = array
        self.searchDepth = 3  # 树的搜索深度 (start from 0) (可再调整)
        self.goback = False

    def output(self, currentRound: int, board, mode: str):
        if board.getTime(self.isFirst) <= 0.5*maxTime:
            self.searchDepth = 2
        alist = board.getScore(self.isFirst)
        yourLlist = board.getScore(not self.isFirst)  # 敌方序列

        if len(alist) is 0:  # 棋盘空着
            return board.getNext(self.isFirst, currentRound)

        elif mode is 'direction' and self.goback:  # 吃完之后回去
            if self.isFirst and board.move(True,2):  # 先手
                return 2
            elif not self.isFirst and board.move(False,3):  # 后手
                return 3

        elif mode is 'position' and alist[-1] <= 4 and len(alist)!=0 and len(board.getNone(self.isFirst)) is not 0:  # 前期落子
            return board.getNext(self.isFirst, currentRound)

        elif mode is 'position' and len(board.getNone(not self.isFirst)) == 0:  # 敌方已经被塞满
            return board.getNext(self.isFirst, currentRound)

        elif mode is 'position' and len(board.getNone(self.isFirst)) == 0:  # 我方被塞满 敌方还没满
            if len(yourLlist) == 0:
                return board.getNone()[0]
            pointDict = {}
            for position in board.getNone(not self.isFirst):  # 敌方空位
                copyBoard = board.copy()
                copyBoard.add(not self.isFirst, position)
                pointDict[chessboardPoint(copyBoard,self.isFirst,early=False)] = position
                return pointDict[max(pointDict.keys())]  # 返回最高的分数的下其位置

        if mode in ['position', 'direction']:
            if len(alist) is 0:  # 棋盘空着
                pass
            else:  # 棋盘非空
                if alist[-1] < 4 and len(alist)!=0:  # 前期
                    return minimax(nowBoard=board, currentRound=currentRound, minormax=False, mode=mode,
                                   isFirst=self.isFirst, parent=None, depth=0, early=True,searchDepth=self.searchDepth)
                elif len(yourLlist) is not 0 and (alist[-1] + 2 <= yourLlist[-1]):  # 大幅落后
                    return self.extremeOutput(currentRound=currentRound, board=board, mode=mode)
                elif len(yourLlist) is not 0 and alist[-1] >= 7 and yourLlist[-1] < alist[-1]:  # 大幅领先 可以考虑7或8
                    return self.extremeOutput(currentRound=currentRound, board=board, mode=mode)
                else:  # 一般情况
                    return minimax(nowBoard=board, currentRound=currentRound, minormax=False, mode=mode,
                                   isFirst=self.isFirst, parent=None, depth=0, early=False,searchDepth=self.searchDepth)
        else:  # 下一步没得动
            return None

    def extremeOutput(self, currentRound, board, mode):
        z=True
        alist = board.getScore(self.isFirst)
        yourLlist = board.getScore(not self.isFirst)  # 敌方序列
        if alist[-1] >= 7 and yourLlist[-1] < alist[-1] and self.chance2(board)!=[]:
            pass
        else:
            z=False
        if not z:
            if mode == 'position':  # 给出己方下棋的位置
                if len(yourLlist) is not 0 and (alist[-1] + 2 <= yourLlist[-1]) and self.trouble2(board)!=():  # 大幅落后
                    return self.trouble2(board)
                elif len(yourLlist) is not 0 and alist[-1] >= 8 and yourLlist[-1] < alist[-1] and self.trouble1(board)!=():  # 大幅领先 可以考虑7或8
                    return self.trouble1(board)
                else:
                    return minimax(nowBoard=board, currentRound=currentRound, minormax=False, mode=mode,
                                   isFirst=self.isFirst, parent=None, depth=0, early=False,searchDepth=self.searchDepth)
            elif mode == 'direction':  # 给出己方合并的方向
                if alist[-1] >= 7 and yourLlist[-1] < alist[-1] and int(self.chance1(board)) in [0,1,2,3]:
                    if board.move(self.isFirst,self.chance1(board)):
                        return 3
                    else:
                        return minimax(nowBoard=board, currentRound=currentRound, minormax=False, mode=mode,
                                   isFirst=self.isFirst, parent=None, depth=0, early=False,searchDepth=self.searchDepth)
                else:
                    return minimax(nowBoard=board, currentRound=currentRound, minormax=False, mode=mode,
                                   isFirst=self.isFirst, parent=None, depth=0, early=False,searchDepth=self.searchDepth)
        else:
            if mode=='position':
                return self.chance2(board)[0]
            elif mode=='direction':
                return int(self.chance2(board))[1]
            else:
                return None
    # 判断棋子是否为我方棋子，返回bool
    def isin(self, board, cow, column):
        if self.isFirst:
            return board.getBelong((cow, column))
        else:
            return not board.getBelong((cow, column))

    # 判断此处的我方棋子是否有被敌方棋子吃掉的危险，若有危险，返回威胁棋子位置组成列表[[row,column]]；否则返回[]
    def menace(self, board, score, row, column):
        l = []
        d = 0
        x=board.getDecision(not self.isFirst)
        while d < 4:
            a = row
            b = column
            s = 0
            if d == 0 and row != 0:  # 我方棋子不处于第一行，向上搜索
                # 若搜索到空位且未达到顶端且此处棋子还属于敌方，则继续搜索
                while s == 0 and a != 0 and not self.isin(board, a-1, b):
                    a -= 1
                    if x!=(a,b):】
                        s = board.getValue((a, b))
                    else:
                        s=1
                if score == s:
                    l.append([a, b])
                else:
                    pass
            elif d == 1 and row != 3:  # 我方棋子不处于第四行，向下搜索
                # 若搜索到空位且未达到底端且棋子还属于敌方，则继续搜索
                while s == 0 and a != 3 and not self.isin(board, a+1, b):
                    a += 1
                    if x!=(a,b):
                        s = board.getValue((a, b))
                    else:
                        s=1
                if score == s:
                    l.append([a, b])
                else:
                    pass
            elif d == 2 and column != 0:  # 我方棋子不属于第一列，向左搜索
                # 若搜索到空位且未达到最左端且棋子还属于敌方，则继续搜索
                while s == 0 and b != 0 and not self.isin(board, a, b-1):
                    b -= 1
                    if x!=(a,b):
                        s = board.getValue((a, b))
                    else:
                        s=1
                if score == s:
                    l.append([a, b])
                else:
                    pass
            elif d == 3 and column != 7:  # 我方棋子不属于第八列，向右搜索
                # 若搜索到空位且未达到最右端且棋子还属于敌方，则继续搜索
                while s == 0 and b != 7 and not self.isin(board, a, b+1):
                    b += 1
                    if x!=(a,b):
                        s = board.getValue((a, b))
                    else:
                        s=1
                if score == s:
                    l.append([a, b])
                else:
                    pass
            else:
                pass
            d += 1
        return l

    def ast(self,board,cow,column):
        column+=1
        if self.isFirst:
            if int(column % 4 + 4)<8 and \
                   int(column % 4 + 4)>=4 and int(cow - 1 + column / 4)>=0 and int(cow - 1 + column / 4)<4:
                return True
            else:
                return False
        else:
            if int(column % 4 )<4 and \
                   int(column % 4 )>=0 and int(cow  + column / 4)>=0 and int(cow + column / 4)<4:
                return True
            else:
                return False

    # 给定搜索级别值，从给定行列出发逐行搜索，返回搜索到第一个符合的棋子位置(row,column)
    def search(self, board, score, cow, column):
        s = ()
        while s == () and self.ast(board,cow,column):
            if self.isFirst:
                column += 1
                if board.getValue((int(cow - 1 + column / 4), int(column % 4 + 4))) == score:
                    s = (int(cow - 1 + column / 4), int(column % 4 + 4))
                else:
                    pass
            else:
                column += 1
                if board.getValue((int(cow + column / 4), int(column % 4))) == score:
                    s = (int(cow + column / 4), int(column % 4))
                else:
                    pass
        return s

    # 若对方存在两个较大级别的棋子快要合并的情况，在其中一个棋子旁边插入一个2搅乱计划，返回插入2的位置(cow,column)
    def trouble1(self, board):
        s = max(board.getScore(not self.isFirst))  # 取得敌方棋子级别的最大值
        l = []
        a = ()
        k = []
        b = ()
        c = []
        # 搜索包含级别至少为3
        while s > 2 and l == []:
            if self.isFirst and (s in board.getScore(not self.isFirst)) and self.search(board, s, 0, 4)!=():
                a = self.search(board, s, 0, 4)  # 搜索满足条件的第一个棋子
                l = self.menace(board, s, a[0], a[1])  # 查看附近是否可能存在可以合并的棋子
            elif not self.isFirst and (s in board.getScore(not self.isFirst)) and self.search(board, a, 0, 0)!=():
                a = self.search(board, a, 0, 0)  # 搜索满足条件的第一个棋子
                l = self.menace(board, s, a[0], a[1])  # 查看附近是否可能存在可以合并的棋子
            else:
                pass
            s -= 1
        if len(l)>0:
            for i in l:
                if abs(i[0] - a[0]) > 1 or abs(i[1] - a[1]) > 1:  # 查看这两个棋子之间是否有空位
                    k.append(i)
                else:
                    pass
        else:
            k=[]
        if k == []:
            b = ()
        else:
            c = k[0]
            if c[0] == a[0]:
                if c[1] > a[1]:
                    b = (a[0], a[1] + 1)
                else:
                    b = (a[0], a[1] - 1)
            else:
                if c[0] > a[0]:
                    b = (a[0] + 1, a[1])
                else:
                    b = (a[0] - 1, a[1])
        return b

    # 对于落后情况尽量牵制对方，往对方扔2，返回2的位置(cow,column)
    def trouble2(self, board):
        b = self.trouble1(board)
        s = []
        c = 0
        # 若满足trouble1条件，则调用trouble1
        if b != ():
            return b
        else:
            l = board.getNone(not self.isFirst)  # 取得对方空位列表
            a = len(l)
            if a>0:
                for i in range(0, a):
                    s.append(self.total(board, l[i][0], l[i][1]))  # 往对方周围除开空位级别数和最大的地方扔2
                c = s.index(max(s))
                b = l[c]
            else:
                b=()
            return b

    # 查看周围是否有可合并项，返回可合并项位置及方向组成的列表[[cow,column,diraction]]
    def search2(self, board, score, row, column):
        l = []
        d = 0
        while d < 4:
            a = row
            b = column
            s = 0
            if d == 0 and row != 0:
                a -= 1
                s = board.getValue((a, b))
                if score == s:
                    l.append([a, b, 0])
                else:
                    pass
            elif d == 1 and row != 3:
                a += 1
                s = board.getValue((a, b))
                if score == s:
                    l.append([a, b, 1])
                else:
                    pass
            elif d == 2 and column != 0:
                b -= 1
                s = board.getValue((a, b))
                if score == s:
                    l.append([a, b, 2])
                else:
                    pass
            elif d == 3 and column != 7:
                b += 1
                s = board.getValue((a, b))
                if score == s:
                    l.append([a, b, 3])
                else:
                    pass
            else:
                pass
            d += 1
        return l

    # 返回除开空位周围四个棋子的级别之和
    def total(self, board, row, column):
        d = 0
        a = 0
        while d < 4:
            s = 0
            if d == 0 and row > 0:
                while s == 0 and row != 0:
                    row -= 1
                    s = board.getValue((row, column))
                a += s
            elif d == 1 and row < 3:
                while s == 0 and row != 3:
                    row += 1
                    s = board.getValue((row, column))
                a += s
            elif d == 2 and column > 0:
                while s == 0 and column != 0:
                    column -= 1
                    s = board.getValue((row, column))
                a += s
            elif d == 3 and column < 7:
                while s == 0 and column != 7:
                    column += 1
                    s = board.getValue((row, column))
                a += s
            else:
                pass
            d += 1
        return a

    #对于可能存在的对面棋子位于边界线并且刚好可以被我方棋子吃掉不被反吃的情况，返回方向choice;否则返回choice=-1
    def chance1(self,board):
        d=0
        l=[]
        a=0
        choice=-1
        if self.isFirst:
            while d<4:
                column=3
                s=0
                while column>=0 and s==0:
                    a=board.getValue((d,column))
                    if a!=0 and self.isin(board,d,column):
                        s=a
                    else:
                        pass
                    column-=1
                l.append(s)
                d+=1
            #判断是否满足可以被我方吃且吃后不会被反吃的情况
            if (l[0]==board.getValue((0,4)) and self.menace(board,l[0]+1,0,4)==[] and not self.isin(board,0,4) and
                l[1]!=board.getValue((1,4)) and l[2]!=board.getValue((2,4)) and l[3]!=board.getValue((3,4))) or \
               (l[1]==board.getValue((1,4)) and self.menace(board,l[1]+1,1,4)==[] and not self.isin(board,1,4) and
                l[0]!=board.getValue((0,4)) and l[2]!=board.getValue((2,4)) and l[3]!=board.getValue((3,4))) or \
               (l[2]==board.getValue((2,4)) and self.menace(board,l[2]+1,2,4)==[] and not self.isin(board,2,4) and
                l[0]!=board.getValue((0,4)) and l[1]!=board.getValue((1,4)) and l[3]!=board.getValue((3,4))) or \
               (l[3]==board.getValue((3,4)) and self.menace(board,l[3]+1,3,4)==[] and not self.isin(board,3,4) and
                l[0]!=board.getValue((0,4)) and l[1]!=board.getValue((1,4)) and l[2]!=board.getValue((2,4))):
                choice=3
            else:
                pass
            return choice
        else:
            return choice
    #若我方为先手且我方有2落在边界线上，在对面空位走个2且合并后不会被对方吃掉的情况\
    #返回落子位置和移动方向[(row,column),diraction]
    def chance2(self,board):
        k=[]
        d=0
        l=[]
        a=0
        if self.isFirst:
            while d<4:
                column=3
                s=0
                while column>=0 and s==0:
                    a=board.getValue((d,column))
                    if a!=0:
                        s=a
                    else:
                        pass
                    column-=1
                l.append([s,column])
                d+=1
            if l[0][0]==1 and l[0][1]==3 and self.menace(board,2,0,4)==[] and board.getValue(0,4)==0 and not board.getBelong(0,4) \
               and l[1][0]!=board.getValue(1,4) and l[2][0]!=board.getValue(2,4) and l[3][0]!=board.getValue(3,4):
                k=[(0,4),3]
            elif l[1][0]==1 and l[1][1]==3 and self.menace(board,2,1,4)==[] and board.getValue(1,4)==0 and not board.getBelong(1,4) \
               and l[0][0]!=board.getValue(0,4) and l[2][0]!=board.getValue(2,4) and l[3][0]!=board.getValue(3,4):
                k=[(1,4),3]
            elif l[2][0]==1 and l[2][1]==3 and self.menace(board,2,2,4)==[] and board.getValue(2,4)==0 and not board.getBelong(2,4) \
               and l[1][0]!=board.getValue(1,4) and l[0][0]!=board.getValue(0,4) and l[3][0]!=board.getValue(3,4):
                k=[(2,4),3]
            elif l[3][0]==1 and l[3][1]==3 and self.menace(board,2,3,4)==[] and board.getValue(3,4)==0 and not board.getBelong(3,4) \
               and l[1][0]!=board.getValue(1,4) and l[2][0]!=board.getValue(2,4) and l[0][0]!=board.getValue(0,4):
                k=[(3,4),3]
            else:
                k=[]
        else:
            pass
        return k

def midscore(board,isFirst):
    def isin(board,cow,column,isFirst):
        if isFirst:
            return board.getBelong((cow,column))
        else:
            return not board.getBelong((cow,column))
    def menace(board,score,row,column,isFirst):
        l=[]
        d=0
        while d<4:
            a=row
            b=column
            s=0
            if d==0 and row!=0:
                while s==0 and a!=0 and not isin(board,a-1,b,isFirst):
                    a-=1
                    s=board.getValue((a,b))
                if score==s:
                    l.append([a,b])
                else:
                    pass
            elif d==1 and row!=3:
                while s==0 and a!=3 and not isin(board,a+1,b,isFirst):
                    a+=1
                    s=board.getValue((a,b))
                if score==s:
                    l.append([a,b])
                else:
                    pass
            elif d==2 and column!=0:
                while s==0 and b!=0 and not isin(board,a,b-1,isFirst):
                    b-=1
                    s=board.getValue((a,b))
                if score==s:
                    l.append([a,b])
                else:
                    pass
            elif d==3 and column!=7:

                while s==0 and b!=7 and not isin(board,a,b+1,isFirst):
                    b+=1
                    s=board.getValue((a,b))
                if score==s:
                    l.append([a,b])
                else:
                    pass
            else:
                pass
            d+=1
        return l

    b=board.getRaw()



    #board.getBelong((i,j))->b[i][j][1]
    # board.getValue((i,j))->b[i][j][0]


    score = 0
    if isFirst==True:
        for i in range(4):
            for j in range(4):
                if b[i][j][1]==isFirst and b[i][j][0]!=0:
                    score+=4**b[i][j][0]
                elif b[i][j][1]!=isFirst:
                    score-=4**(b[i][j][0]+0.8)
            for j in range(5,8):
                if b[i][j][1]==isFirst:
                    score+=4**(b[i][j][0]+1.1)

    else:
        for i in range(4):
            for j in range(5,8):
                if b[i][j][1] == isFirst and b[i][j][0] != 0:
                    score += 4 ** b[i][j][0]
                elif b[i][j][1]!=isFirst:
                    score-=4**(b[i][j][0]+0.8)
            for j in range(4):
                if b[i][j][1]==isFirst:
                    score+=4**(b[i][j][0]+1.1)


    for i in range(4):
        for j in range(8):
            if b[i][j][1]==isFirst and b[i][j][0]!=0:
                grade=b[i][j][0]
                dif=[]
                if i>0 and b[i][j][1]==isFirst:
                    dif1=abs(grade-b[i][j][0])
                    dif.append(dif1)
                if i<3 and b[i][j][1]==isFirst:
                    dif2=abs(grade-b[i][j][0])
                    dif.append(dif2)
                if j<7 and b[i][j][1]==isFirst:
                    dif3=abs(grade-b[i][j][0])
                    dif.append(dif3)
                if j>0 and b[i][j][1]==isFirst:
                    dif4=abs(grade-b[i][j][0])
                    dif.append(dif4)
                difz = []
                diff = []
                for i in dif:
                    if i >= 0:
                        difz.append(i)
                    else:
                        diff.append(-i)
                difz.sort()
                diff.sort()
                if len(difz) >= 1:
                    if difz[0] <= 2:
                        score += grade ** 2 * difz[0]
                        if isFirst==True:
                            score+=grade**2*difz[0]
                    else:
                        score -= grade ** 2 * difz[0]
                if len(diff) >= 1:
                    if diff[0] <= 2:
                        score += grade ** 2 * diff[0]
                        if isFirst==True:
                            score+=grade**2*diff[0]
                    else:
                        score -= grade ** 2 * diff[0]
                    if len(diff)>=2 and diff[0]==diff[1] and diff[0]<=2:
                        score-=4**(grade-diff[0])

    for i in range(4):
        for j in range(8):
            if b[i][j][1] == isFirst and b[i][j][0] != 0:
                ll = menace(board, b[i][j][0], i, j, isFirst)
                if ll != [] and b[i][j][0]!=0:
                    score-= 4**(b[ll[0][0]][ll[0][1]][0]+1.5)

    return score

def getourpower(board, isFirst, row):
    board1 = board.copy()
    if isFirst:
        for i in range(5):
            if board1.getValue((row, 4 - i)) != 0 and board1.getBelong((row, 4 - i)):
                return board1.getValue((row, 4 - i))
        else:
            return 0
    else:
        for i in range(5):
            if board1.getValue((row, 3 + i)) != 0 and not board1.getBelong((row, 3 + i) ):
                return board1.getValue((row, 3 + i))
        else:
            return 0

def getdanger(board, isFirst, row):
    board1 = board.copy()
    if not isFirst:
        for i in range(5):
            if board1.getValue((row, 4 - i)) != 0 and board1.getBelong((row, 4 - i)):
                return board1.getValue((row, 4 - i))
        else:
            return 0
    else:
        for i in range(5):
            if board1.getValue((row, 3 + i)) != 0 and not board1.getBelong((row, 3 + i)):
                return board1.getValue((row, 3 + i))
        else:
            return 0

def ee(board, isFirst):  # early evaluate
    score = 0
    lst1 = board.getScore(isFirst)
    len1 = len(lst1)
    for i in range(len1):
        score += 2 ** lst1[i] - 1
    if not board.move(isFirst, 3) and not board.move(isFirst, 2) and not board.move(isFirst, 1) and not board.move(isFirst, 0):
        return -1000
    else:
        if isFirst:
            # 先只考虑是否进攻
            for i in range(4):
                if getourpower(board, isFirst, i) != 0 and getourpower(board, isFirst, i) == board.getValue((i, 4)) and board.getValue((i,3)) == 0 and not board.getBelong((i,4)):
                    score += 2**getourpower(board, isFirst, i) - 1
                if (board.getBelong((i,4)) or board.getValue((i,4)) == 0) and getourpower(board, isFirst, i) == getdanger(board, isFirst, i) and (board.getValue((i,3)) !=0 or board.getBelong((i,4))):
                    score -= 2**getdanger(board, isFirst, i) - 1
                if board.getBelong((i, 4)) and board.getValue((i,4)) != getdanger(board, isFirst, i):
                    score += 2**board.getValue((i, 4)) - 1
                if not board.getBelong((i, 3)) and board.getValue((i,3)) != getourpower(board, isFirst, i):
                    score -= 2 * (2**board.getValue((i, 3)) - 1)
                if not board.getBelong((i, 2)):
                    score -= 2 * (2**board.getValue((i, 2)) - 1)
            if (board.getValue((0,0)) == lst1[len1 - 1] or board.getValue((3,0)) == lst1[len1 - 1]) and lst1[len1 - 1] > 1:
                score += 2**lst1[len1 - 1] / 4 * 3 - 1
        else:  # 后手，保守发育
            for i in range(4):
                if getourpower(board, isFirst, i) != 0 and getourpower(board, isFirst, i) == board.getValue((i, 3)) and board.getValue((i,4)) == 0 and not board.getBelong((i,3)):
                    score += 2**getourpower(board, isFirst, i) - 1
                if (not board.getBelong((i,3)) or board.getValue((i,3)) == 0) and getourpower(board, isFirst, i) == getdanger(board, isFirst, i) and (board.getValue((i,4)) != 0 or not board.getBelong((i,3))):
                    score -= 2**getdanger(board, isFirst, i) - 1
                if board.getBelong((i, 4)) and board.getValue((i,4)) != getourpower(board, isFirst, i):
                    score -= 2 * (2**board.getValue((i, 4)) - 1)
                if board.getBelong((i, 5)):
                    score -= 2 * (2**board.getValue((i, 5)) - 1)
                if not board.getBelong((i, 3)) and board.getValue((i,3)) != getdanger(board, isFirst, i):
                    score += 2**board.getValue((i, 3)) - 1
            if (board.getValue((0,7)) == lst1[len1 - 1] or board.getValue((3,7)) == lst1[len1 - 1]) and lst1[len1 - 1] > 1:
                score += 2**lst1[len1 - 1] / 4 * 3 - 1
        return score
