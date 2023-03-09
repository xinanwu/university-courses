class Player:
    def __init__(self, isFirst, array):
        # 初始化
        self.isFirst = isFirst
        self.array = array

    def output(self, currentRound, board, mode):
        if mode == 'position':  # 给出己方下棋的位置
            another = board.getNext(self.isFirst, currentRound)  # 己方的允许落子点
            if another != (): return another

            available = board.getNone(not self.isFirst)  # 对方的允许落子点
            if not available:   # 整个棋盘已满
                return None
            else:
                from random import choice
                return choice(available)
        elif mode == 'direction':  # 给出己方合并的方向
            from random import shuffle
            directionList = [0, 1, 2, 3]
            shuffle(directionList)
            for direction in directionList:
                if board.move(self.isFirst, direction): return direction
        else:
            return
        
    #判断棋子是否为我方棋子，返回bool
    def isin(self,board,cow,column):
        if self.isFirst:
            return board.getBelong((cow,column))
        else:
            return not board.getBelong((cow,column))
        
    #判断是否存在于对方领地的我方棋子，返回棋子位置组成的列表[[row,column]]
    def hasout(self,board):
        row=0
        column=0
        l=[]
        #对于先后手分区不同分别判断
        if self.isFirst:
            while row<4:
                if board.getBelong((row,column%4+4)):
                    l.append([row,column%4+4])
                    column+=1
                    row+=column/4
                else:
                    column+=1
                    row+=column/4
            return l
        else:
            while row<4:
                if board.getBelong((row,column%4)):
                    column+=1
                    row+=column/4
                else:
                    l.append([row,column%4])
                    column+=1
                    row+=column/4
            return l
        
    #判断此处的我方棋子是否有被敌方棋子吃掉的危险，若有危险，返回威胁棋子位置组成列表[[row,column]]；否则返回[]    
    def menace(self,board,score,row,column):
        l=[]
        d=0
        while d<4:
            a=row
            b=column
            s=0
            if d==0 and row!=0:#我方棋子不处于第一行，向上搜索
                #若搜索到空位且未达到顶端且此处棋子还属于敌方，则继续搜索
                while s==0 and a!=0 and not self.isin(board,a,b):
                    a-=1
                    s=board.getValue((a,b))
                if score==s:
                    l.append([a,b])
                else:
                    pass
            elif d==1 and row!=3:#我方棋子不处于第四行，向下搜索
                #若搜索到空位且未达到底端且棋子还属于敌方，则继续搜索
                while s==0 and a!=3 and not self.isin(board,a,b):
                    a+=1
                    s=board.getValue((a,b))
                if score==s:
                    l.append([a,b])
                else:
                    pass
            elif d==2 and column!=0:#我方棋子不属于第一列，向左搜索
                #若搜索到空位且未达到最左端且棋子还属于敌方，则继续搜索
                while s==0 and b!=0 and not self.isin(board,a,b):
                    b-=1
                    s=board.getValue((a,b))
                if score==s:
                    l.append([a,b])
                else:
                    pass
            elif d==3 and column!=7:#我方棋子不属于第八列，向右搜索
                #若搜索到空位且未达到最右端且棋子还属于敌方，则继续搜索
                while s==0 and b!=7 and not self.isin(board,a,b):
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
    
    #给定搜索级别值，从给定行列出发逐行搜索，返回搜索到第一个符合的棋子位置(row,column)
    def search(self,board,score,cow,column):
        s=()
        while s==():
            if self.isFirst:
                column+=1
                if board.getValue((cow-1+column/4,column%4+4))==score:
                    s=(cow-1+column/4,column%4+4)
                else:
                    pass
            else:
                column+=1
                if board.getValue((cow+column/4,column%4))==score:
                    s=(cow+column/4,column%4)
                else:
                    pass
        return s
    
    #若对方存在两个较大级别的棋子快要合并的情况，在其中一个棋子旁边插入一个2搅乱计划，返回插入2的位置(cow,column)        
    def trouble1(self,board):
        s=max(board.getScore(not self.isFirst))#取得敌方棋子级别的最大值
        l=[]
        a=()
        k=[]
        b=()
        c=[]
        #搜索包含级别至少为3
        while s>2 and l==[]:
            if self.isFirst:
                a=self.search(board,s,0,4)#搜索满足条件的第一个棋子
                l=self.menace(board,s,a[0],a[1])#查看附近是否可能存在可以合并的棋子
            else:
                a=self.search(board,a,0,0)#搜索满足条件的第一个棋子
                l=self.menace(board,s,a[0],a[1])#查看附近是否可能存在可以合并的棋子
            s-=1
        for i in l:
            if abs(i[0]-a[0])>1 or abs(i[1]-a[1])>1:#查看这两个棋子之间是否有空位
                k.append(i)
            else:
                pass
        if k==[]:
            b=()
        else:
            c=k[0]
            if c[0]==a[0]:
                if c[1]>a[1]:
                    b=(a[0],a[1]+1)
                else:
                    b=(a[0],a[1]-1)
            else:
                if c[0]>a[0]:
                    b=(a[0]+1,a[1])
                else:
                    b=(a[0]-1,a[1])
        return b
    
    #对于落后情况尽量牵制对方，往对方扔2，返回2的位置(cow,column)
    def trouble2(self,board):
        b=self.trouble1(board)
        s=[]
        c=0
        #若满足trouble1条件，则调用trouble1
        if b!=():
            return b
        else:
            l=board.getNone(not self.isFirst)#取得对方空位列表
            a=len(l)
            for i in range(0,a):
                s.append(self.total(board,l[i][0],l[i][1]))#往对方周围除开空位级别数和最大的地方扔2
            c=s.index(max(s))
            b=l[c]
            return b
        
    #查看周围是否有可合并项，返回可合并项位置及方向组成的列表[[cow,column,diraction]]            
    def search2(self,board,score,row,column):
        l=[]
        d=0
        while d<4:
            a=row
            b=column
            s=0
            if d==0 and row!=0:
                a-=1
                s=board.getValue((a,b))
                if score==s:
                    l.append([a,b,0])
                else:
                    pass
            elif d==1 and row!=3:
                a+=1
                s=board.getValue((a,b))
                if score==s:
                    l.append([a,b,1])
                else:
                    pass
            elif d==2 and column!=0:
                b-=1
                s=board.getValue((a,b))
                if score==s:
                    l.append([a,b,2])
                else:
                    pass
            elif d==3 and column!=7:
                b+=1
                s=board.getValue((a,b))
                if score==s:
                    l.append([a,b,3])
                else:
                    pass
            else:
                pass
            d+=1
        return l
    
    #返回除开空位周围四个棋子的级别之和
    def total(self,board,row,column):
        d=0
        a=0
        while d<4:
            s=0
            if d==0 and row>0:
                while s==0 and row!=0:
                    row-=1
                    s=board.getValue((row,column))
                a+=s
            elif d==1 and row<3:
                while s==0 and row!=3:
                    row+=1
                    s=board.getValue((row,column))
                a+=s
            elif d==2 and column>0:
                while s==0 and column!=0:
                    column-=1
                    s=board.getValue((row,column))
                a+=s
            elif d==3 and column<7:
                while s==0 and column!=7:
                    column+=1
                    s=board.getValue((row,column))
                a+=s
            else:
                pass
            d+=1
        return a
    
    #对于我方棋子在敌方领地的情况，对于周围有可以偷吃敌方棋子的机会，返回方向choice,若没有机会，choice=-1
    def chance1(self,board):
        s=[]
        a=0
        b=0
        c=0
        d=0
        choice=-1
        l=self.hasout(board)
        if l!=[]:
            for i in l:
                s=self.search2(board,board.getValue((i[0],i[1])),i[0],i[1])
                #得到各个方向的可以吃到的分数
                for j in s:
                    #向上可以吃到的分数
                    if j[2]==0 and self.menace(board,board.getValue((j[0],j[1])),j[0],j[1])==[]:
                        a+=board.getValue((j[0],j[1]))
                    #向下可以吃到的分数    
                    elif j[2]==1 and self.menace(board,board.getValue((j[0],j[1])),j[0],j[1])==[]:
                        b+=board.getValue((j[0],j[1]))
                    #向左可以吃到的分数    
                    elif j[2]==2 and self.menace(board,board.getValue((j[0],j[1])),j[0],j[1])==[]:
                        c+=board.getValue((j[0],j[1]))
                    #向右可以吃到的分数    
                    elif j[2]==3 and self.menace(board,board.getValue((j[0],j[1])),j[0],j[1])==[]:
                        d+=board.getValue((j[0],j[1]))
                    else:
                        pass
    #判断哪个方向可以吃到的分数最多        
            if a==max([a,b,c,d]):
                choice=0
            elif b==max([a,b,c,d]):
                choice=1
            elif c==max([a,b,c,d]):
                choice=2
            else:
                choice=3
        else:
            pass
        return choice
    
    #对于可能存在的对面棋子位于边界线并且刚好可以被我方棋子吃掉不被反吃的情况，返回方向choice;否则返回choice=-1
    def chance2(self,board):
        d=0
        l=[]
        a=0
        choice=-1
        l1=[]
        c=board.getDecision(not self.isFirst)#取得对方上次决策的方向
        if c==():
            b=-1
        else:
            b=c[0]
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
                l.append(s)
                d+=1
            #判断是否满足可以被我方吃且吃后不会被反吃的情况
            if (l[0]==board.getValue((0,4)) and self.menace(board,l[0]+1,0,4)==[] and\
                l[1]!=board.getValue((1,4)) and l[2]!=board.getValue((2,4)) and l[3]!=board.getValue((3,4))) or \
               (l[1]==board.getValue((1,4)) and self.menace(board,l[1]+1,1,4)==[] and\
                l[0]!=board.getValue((0,4)) and l[2]!=board.getValue((2,4)) and l[3]!=board.getValue((3,4))) or \
               (l[2]==board.getValue((2,4)) and self.menace(board,l[2]+1,2,4)==[] and\
                l[0]!=board.getValue((0,4)) and l[1]!=board.getValue((1,4)) and l[3]!=board.getValue((3,4))) or \
               (l[3]==board.getValue((3,4)) and self.menace(board,l[3]+1,3,4)==[] and\
                l[0]!=board.getValue((0,4)) and l[1]!=board.getValue((1,4)) and l[2]!=board.getValue((2,4))):
                choice=3
            else:
                pass
            return choice
        else:
        #对于对方不同的移动方向分别判断
            if b==0:
                for i in range(0,4):
                    l.append(board.getValue((i,3)))
                if l[0]==l[1] and l[0]!=0:
                    if l[2]==l[3] and l[2]!=0:
                        l1=[l[0]+1,l[2]+1,0,0]
                    else:
                        l1=[l[0]+1,l[2],l[3],0]
                elif l[1]==l[2] and l[1]!=0:
                    l1=[l[0],l[1]+1,l[3],0]
                elif l[2]==l[3] and l[2]!=0:
                    l1=[l[0],l[1],l[2]+1,0]
                else:
                    l1=l
            elif b==1:
                for i in range(0,4):
                    l.append(board.getValue((i,3)))
                if l[3]==l[2] and l[2]!=0:
                    if l[0]==l[1] and l[0]!=0:
                        l1=[0,0,l[0]+1,l[2]+1]
                    else:
                        l1=[0,l[0],l[1],l[2]+1]
                elif l[1]==l[2] and l[1]!=0:
                    l1=[0,l[0],l[1]+1,l[3]]
                elif l[0]==l[1] and l[1]!=0:
                    l1=[0,l[1]+1,l[2],l[3]]
                else:
                    l1=l
            elif b==2:
                l1=[0,0,0,0]
            elif b==-1:
                for i in range(0,4):
                    l1.append(board.getValue(i,3))
            else:
                while d<4:
                    column=3
                    s=0
                    l=[]
                    while column>=0:
                        a=board.getValue((d,column))
                        if a!=0:
                            s=a
                            l.append(s)
                        else:
                            pass
                        column-=1
                        if len(l)>1:
                            if l[0]==l[1]:
                                l1.append(l[1]+1)
                            else:
                                l1.append(l[0])
                        elif len(l)==1:
                            l1.append(l[0])
                        else:
                            l1.append(0)                           
                    d+=1
        #得到我方最左边棋子从上到下的级别
        while d<4:
            column=4
            s=0
            l=[]
            while column<8 and s==0:
                a=board.getValue((d,column))
                if a!=0:
                    s=a
                else:
                    pass
                column+=1
            l.append(s)
            d+=1
        #判断是否满足可以吃掉对方且不会被反吃的情况
        if (l[0]==l1[0] and self.menace(board,l1[0]+1,0,3)==[] and\
            l[1]!=l1[1] and l[2]!=l1[2] and l[3]!=l1[3]) or \
           (l[1]==l1[1] and self.menace(board,l1[1]+1,1,3)==[] and\
            l[0]!=l1[0] and l[2]!=l1[2] and l[3]!=l1[3]) or \
           (l[2]==l1[2] and self.menace(board,l1[2]+1,2,3)==[] and\
            l[1]!=l1[1] and l[0]!=l1[0] and l[3]!=l1[3]) or \
           (l[3]==l1[3] and self.menace(board,l1[3]+1,3,3)==[] and\
            l[1]!=l1[1] and l[2]!=l1[2] and l[0]!=l1[0]):
            choice=2
        else:
            pass
        return choice
    
    #若我方为先手且我方有2落在边界线上，在对面空位走个2且合并后不会被对方吃掉的情况\
    #返回落子位置和移动方向[(row,column),diraction]
    def chance3(self,board):
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
                k.append((0,4),3)
            elif l[1][0]==1 and l[1][1]==3 and self.menace(board,2,1,4)==[] and board.getValue(1,4)==0 and not board.getBelong(1,4) \
               and l[0][0]!=board.getValue(0,4) and l[2][0]!=board.getValue(2,4) and l[3][0]!=board.getValue(3,4):
                k.append((1,4),3)
            elif l[2][0]==1 and l[2][1]==3 and self.menace(board,2,2,4)==[] and board.getValue(2,4)==0 and not board.getBelong(2,4) \
               and l[1][0]!=board.getValue(1,4) and l[0][0]!=board.getValue(0,4) and l[3][0]!=board.getValue(3,4):
                k.append((2,4),3)
            elif l[3][0]==1 and l[3][1]==3 and self.menace(board,2,3,4)==[] and board.getValue(3,4)==0 and not board.getBelong(3,4) \
               and l[1][0]!=board.getValue(1,4) and l[2][0]!=board.getValue(2,4) and l[0][0]!=board.getValue(0,4):
                k.append((3,4),3)
            else:
                k=[(),-1]
        else:
            pass
        return k


            
            
            
    
    
                
                
                
                
                
                
                
                    
                        
                    
            
            

            
        
                
                        
                
            
        
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
        