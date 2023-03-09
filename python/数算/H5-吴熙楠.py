# 创建树的节点类
class TreeNode:
    
    # 初始化树的节点
    def __init__(self,key,val,left=None,right=None,parent=None,balance=0):
        self.key=hash(key)                    #节点值，节点位置，索引
        self.ikey=key                          #hash值
        self.val=val                              #有效载荷，节点显示的值
        self.left=left                           #左子节点
        self.right=right                         #右子节点
        self.parent=parent                            #父节点
        self.balance=balance                  #节点的平衡因子
        
    # 获取左子树 (不存在时返回None)   
    def getLeft(self):  
        return self.left
    
    # 获取右子树 (不存在时返回None)
    def getRight(self):  
        return self.right

    # 替换节点数据
    def replaceData(self,key,val,left,right):
        self.key=hash(key)                      #更新节点值
        self.ikey=key
        self.val=val                            #更新有效载荷
        self.left=left                             #更新左子节点
        self.right=right                            #更新右子节点
        if self.getLeft():                         #若有左子节点
            self.left.parent=self                #将该节点的左子节点的父节点指向self
        if self.getRight():                        #若有右子节点
            self.right.parent=self               #将该节点的右子节点的父节点指向self
            
    #替换hash值
    def replaceValue(self,key):
        self.key=hash(key)
        self.ikey=key
        
    # 判断是否是左子节点(父节点存在，并且self与self父节点的左子节点相同)   
    def isLeft(self):
        return self.parent and self.parent.left==self

    # 判断是否是右子节点
    def isRight(self):
        return self.parent and self.parent.right==self

    # 判断是否是根节点
    def isRoot(self):
        return not self.parent                          #没有父节点

    # 判断是否是叶节点
    def isLeaf(self):
        return not (self.right or self.left)  #没有左右子节点

    # 判断是否有子节点
    def Child(self):
        return self.right or self.left        #有左或右子节点

    # 判断是否有2个子节点
    def Children(self):
        return self.right and self.left       #有左右2个子节点
        
    # 中序遍历
    def __iter__(self):
        if self:                                        #若当前节点存在，则
            if self.getLeft():                     #若当前节点有左子节点，则
                for ikey in self.left:             #循环输出当前节点的左子树的节点值
                    yield ikey                          #在for循环中，每次执行到yield时，就返回一个迭代值，且不会终止循环；下个循环时，代码从yield返回值的下一行继续返回
            yield self.ikey                              #返回当前节点值
            if self.getRight():                    #若当前节点有右子节点，则
                for ikey in self.right:            #循环输出当前节点的右子树的节点值
                    yield ikey
    
    #层次嵌套列表输出TreeNode及其子节点
    def __str__(self):
        l=f"[{str(self.left)}]" if self.left else "[]"
        r=f"[{str(self.right)}]" if self.right else "[]"
        return f"[{repr(self.ikey)}({self.balance}),{l},{r}]"
    
    __repr__=__str__
                       
    # 将被删除节点的继任者拼接到被删除的节点位置
    def cut(self):
        if self.isLeaf():                               #若被删除节点是叶节点，则无需再拼接
            if self.isLeft():                      #若被删除节点是父节点的左子节点，则
                self.parent.left=None            #被删除节点为None，无需再拼接
            else:                                       #若被删除节点是父节点的右子节点，则
                self.parent.right=None           #被删除节点为None，无需再拼接
        elif self.Child():                     #若被删除节点有子节点，则
            if self.getLeft():                     #若被删除节点有左子节点，则
                if self.isLeft():                  #若被删除节点是左子节点，则
                    # 将被删除节点的父节点的左子节点指向被删除节点的左子节点
                    self.parent.left=self.left  
                else:                                   #若被删除节点是右子节点，则
                    # 将被删除节点的父节点的右子节点指向被删除节点的左子节点
                    self.parent.right=self.left
                # 将被删除节点的左子节点的父节点指向被删除节点的父节点
                self.left.parent=self.parent         
            else:                                       #若被删除节点没有左子节点，则被删除节点有右子节点
                if self.isLeft():                  #若被删除节点是左子节点，则
                    # 将被删除节点的父节点的左子节点指向被删除节点的右子节点
                    self.parent.left=self.right 
                else:                                   #若被删除节点是右子节点，则
                    # 将被删除节点的父节点的右子节点指向被删除节点的右子节点
                    self.parent.right=self.right
                # 将被删除节点的右子节点的父节点指向被删除节点的父节点
                self.right.parent=self.parent        

    # 查找被删除节点的继任者，继任者节点最多只能有一个子节点
    def findSucc(self):
        succ=None                                     #初始化被删除节点的继任者为None
        if self.getRight():                        #若被删除节点有右子节点，则
            succ=self.right.findMin()            #获取被删除节点的右子树中的最小节点作为继任者
        else:                                           #若被删除节点没有右子节点，则
            if self.parent:                             #若被删除节点有父节点，则
                if self.isLeft():                  #若被删除节点是父节点的左子节点，则
                    succ=self.parent                  #被删除节点的父节点是继任者
                else:                                   #若被删除节点是父节点的右子节点，则被删除节点的继任者是其父节点的继任者，不会是被删除节点
                    self.parent.right=None       #暂时将None赋值给被删除节点，则继任者不会是被删除节点，方便下一行递归查找
                    succ=self.parent.findSucc()  #将被删除节点的父节点的继任者作为继任者
                    self.parent.right=self       #获得继任者后，重新将被删除节点赋值给自己，以免被删除节点为None扰乱树结构
        return succ

    # 查找当前树的最小子节点
    def findMin(self):
        current=self                                  #将自身设置为当前节点
        while current.getLeft():                   #若当前节点有左子节点，则循环
            current=current.left                 #将当前节点的左子节点作为下一个当前节点
        return current                                  #返回最终左子节点，即此树中的最小节点         

# 二叉查找树类
class AVLTree:
    
    # 初始化空二叉树
    def __init__(self):
        self.root=None
        self.size=0

    # 通过__len__方法使用len()
    def __len__(self):
        return self.size

    # 实现了__iter__方法的对象就是可迭代对象
    def __iter__(self):
        if self.root:
            return iter(self.root)        #返回二叉查找树根节点的迭代，即遍历二叉查找树
        return iter([])

    # 创建二叉搜索树
    def Put(self,key,val):
        if self.root:                       #若树已经有根节点，则
            self.put(key,val,self.root)  #从树的根开始，搜索二叉树
        else:                               #若树没有根节点，则
            self.root=TreeNode(key,val)  #创建一个新的TreeNode并把它作为树的根节点
        self.size+=1           #增加树的大小

    # 搜索树，Put()的辅助函数
    def put(self,key,val,node):
        ikey=key
        key=hash(ikey)
        if key<node.key:           #若新的键值小于当前节点键值，则搜索左子树
            if node.getLeft():  #若当前节点有左子树要搜索，则
                self.put(ikey,val,node.left)  #递归搜索左子树
            else:                           #若当前节点无左子树要搜索，则
                node.left=TreeNode(ikey,val,parent=node)    #创建一个新的TreeNode并把它作为当前节点的左子节点
                self.update(node.left)   #更新当前节点的左子节点的平衡因子
        elif key==node.key:        #若新的键值=当前节点键值，则
            node.replaceValue(ikey)         #替换hash值
            node.val=val           #更新当前节点的有效载荷
            self.size-=1           #由于只修改，未增加，又因Put()中+1，所以此处-1
        else:                          #若新的键值>当前节点键值，则搜索右子树
            if node.getRight(): #若当前节点有右子树要搜索，则
                self.put(ikey,val,node.right) #递归搜索右子树
            else:                           #若当前节点无右子树要搜索，则
                node.right=TreeNode(ikey,val,parent=node)   #创建一个新的TreeNode并把它作为当前节点的右子节点
                self.update(node.right)  #更新当前节点的右子节点的平衡因子

    # 更新平衡因子
    def update(self,node):
        if node.balance>1 or node.balance<-1:   #若节点的平衡因子不是-1、0、1，则
            self.rebalance(node)                        #该节点再平衡
            return
        if node.parent!=None:                         #若该节点有父节点，即该节点不是根节点，则
            if node.isLeft():                      #若该节点是左子节点，则
                node.parent.balance+=1          #该节点的父节点的平衡因子+1
            elif node.isRight():                   #若该节点是右子节点，则
                node.parent.balance-=1          #该节点的父节点的平衡因子-1
            if node.parent.balance!=0:          #若该节点的父节点的平衡因子不为0，则
                self.update(node.parent)         #更新该节点的父节点的平衡因子
                
    #del时更新平衡因子
    def update2(self,node):
        if node.balance>1 or node.balance<-1:
            self.rebalance(node)             #重新平衡后如果root平衡因子为0需要再传播
            node=node.parent
        if node.balance==0 and node.parent:
            if node.isLeft():
                node.parent.balance-=1     #左节点少1
            elif node.isRight():
                node.parent.balance+=1   #右节点少1
            self.update2(node.parent)    #向上传播

    # 左旋转（右重的树要左旋转才平衡）
    def rotateLeft(self,rot):
        new=rot.right                   #待旋转节点的右子节点设为新的根节点
        rot.right=new.left        #新根的原左子节点作为原根的新右子节点
        if new.left!=None:                   #若新根原来有左子节点，则
            new.left.parent=rot          #将新根的原左子节点的父节点指向原根
        new.parent=rot.parent                 #新根的父节点指向原根的父节点
        if rot.isRoot():                            #若原根是树的根节点，则
            self.root=new                         #将新根设为树的根节点
        else:                                           #若原根不是树的根节点，则
            if rot.isLeft():                   #若原根是左子树，则
                rot.parent.left=new      #将原根的父节点的左子节点指向新根
            else:                                       #若原根是右子树，则
                rot.parent.right=new     #将原根的父节点的右子节点指向新根
        new.left=rot                     #将新根的左子节点指向原根
        rot.parent=new                        #将原根的父节点指向新根
        rot.balance=rot.balance+1-min(new.balance,0)   #更新原根节点的平衡因子，被移动的子树内的节点的平衡因子不受旋转影响，计算方法见上方注释
        new.balance=new.balance+1+max(rot.balance,0)   #更新新根节点的平衡因子，被移动的子树内的节点的平衡因子不受旋转影响，计算方法见上方注释

    # 右旋转（左重的树要右旋转才平衡）
    def rotateRight(self,rot):
        new=rot.left                    #待旋转节点的左子节点设为新的根节点
        rot.left=new.right         #新根的原右子节点作为原根的新左子节点
        if new.right!=None:                  #若新根原来有右子节点，则
            new.right.parent=rot         #将新根的原右子节点的父节点指向原根
        new.parent=rot.parent                 #新根的父节点指向原根的父节点
        if rot.isRoot():                            #若原根是树的根节点，则
            self.root=new                         #将新根设为树的根节点
        else:                                           #若原根不是树的根节点，则
            if rot.isLeft():                   #若原根是左子树，则
                rot.parent.left=new      #将原根的父节点的左子节点指向新根
            else:                                       #若原根是右子树，则
                rot.parent.right=new     #将原根的父节点的右子节点指向新根
        new.right=rot                    #将新根的右子节点指向原根
        rot.parent=new                       #将原根的父节点指向新根
        rot.balance=rot.balance-1-max(new.balance,0)   #更新原根节点的平衡因子，被移动的子树内的节点的平衡因子不受旋转影响，计算方法见上方注释
        new.balance=new.balance-1+min(0,rot.balance)   #更新新根节点的平衡因子，被移动的子树内的节点的平衡因子不受旋转影响，计算方法见上方注释

    # 再平衡
    def rebalance(self,node):
        if node.balance<0:                      #若该节点的平衡因子<0，则
            if node.right.balance>0:       #若该节点的右子节点的平衡因子>0，则
                self.rotateRight(node.right)       #右旋转该节点的右子节点
            self.rotateLeft(node)                       #左旋转该节点
        elif node.balance>0:                    #若该节点的平衡因子>0，则
            if node.left.balance<0:        #若该节点的左子节点的平衡因子<0，则
                self.rotateLeft(node.left)         #左旋转该节点的左子节点
            self.rotateRight(node)                      #右旋转该节点

    # 通过__setitem__方法使用Put()方法
    def __setitem__(self,k,v):
        self.Put(k,v)

    # 根据索引key获取其对应的节点值
    def Get(self,key):
        if self.root:                       #若树已经有根节点，则
            x=self.get(key,self.root) #从树的根开始，搜索二叉树
            if x:                         #若搜索到了，则
                return x.val          #返回存储在节点的有效载荷中的值，即节点显示的值
            else:                           #若没搜索到，则没有该索引对应的节点
                raise KeyError
        else:                               #若树没有根节点，则说明是空二叉树
            raise KeyError
    
    # 搜索树，Get()的辅助函数
    def get(self,key,node):
        ikey=key
        key=hash(ikey)
        if not node:
            return None
        elif node.key==key:        #若当前节点的位置和待查找的位置相同，则
            return node              #返回当前节点的值
        elif key<node.key:         #若当前节点的位置>待查找的位置，则
            return self.get(ikey,node.left)    #递归查找当前节点的左子树
        else:                               #若当前节点的位置<待查找的位置，则
            return self.get(ikey,node.right)   #递归查找当前节点的右子树

    # __getitem__方法
    def __getitem__(self,key):
        return self.Get(key)

    # 通过__contains__方法使用in方法
    def __contains__(self,key):
        if self.get(key,self.root):
            return True
        else:
            return False

    # 根据索引key删除其对应的节点
    def delete(self,key):
        ikey=key
        key=hash(ikey)
        if self.size>1:                                   #若树的大小>1，则
            a=self.get(ikey,self.root)        #获取要删除的节点
            if a!=None:                                #若该节点存在，则
                self.remove(a)                   #删除该节点
                self.size-=1                   #树的大小减1
            else:                                           #若该节点不存在，则
                raise KeyError                 #报错
        elif self.size==1 and self.root.key==key:       #若树的大小为1，且要删除的是根，则
            self.root=None                                #根节点为None
            self.size-=1                       #树的大小减1
        else:                                               #若树的大小为0，则为空树
            raise KeyError                     #报错

    # 通过__delitem__方法使用del方法
    def __delitem__(self,key):
        self.delete(key)

    # 删除节点
    def remove(self,node):
        if node.isLeaf():                        #若被删除节点是叶节点，则没有子节点
            if node==node.parent.left: #若被删除节点是其父节点的左子节点，则
                node.parent.left=None     #被删除节点为None
                node.parent.balance-=1    #左节点少1
            else:                                       #若被删除节点是其父节点的右子节点，则
                node.parent.right=None    #被删除节点为None
                node.parent.balance+=1    #右节点少1
            self.update2(node.parent)
        elif node.Children():             #若被删除节点有2个子节点，则
            succ=node.findSucc()         #获取被删除节点的继任者
            if succ.isLeft():
                succ.parent.balance-=1    #左节点少1
            else:
                succ.parent.balance+=1    #右节点少1
            succ.cut()                            #将被删除节点的继任者拼接到被删除节点位置
            node.replaceValue(succ.ikey)                  #将被删除节点位置的值设置为继任者的值
            node.val=succ.val          #将被删除节点的有效载荷设置为继任者的有效载荷
            self.update2(succ.parent)
        else:                                           #若被删除节点只有1个子节点，则
            if node.getLeft():              #若被删除节点只有左子节点，则
                if node.isLeft():           #若被删除节点是左子节点，则
                    # 将被删除节点的左子节点的父节点指向被删除节点的父节点
                    node.left.parent=node.parent   
                    # 将被删除节点的父节点的左子节点指向被删除节点的左子节点
                    node.parent.left=node.left
                    node.parent.balance-=1    #左节点少1
                elif node.isRight():        #若被删除节点是右子节点，则
                    # 将被删除节点的左子节点的父节点指向被删除节点的父节点
                    node.left.parent=node.parent
                    # 将被删除节点的父节点的右子节点指向被删除节点的左子节点
                    node.parent.right=node.left
                    node.parent.balance+=1     #右节点少1
                else:                               #若被删除节点无父节点，则被删除节点为根节点
                    # 替换被删除节点的左子节点的键、有效载荷、左子节点和右子节点数据
                    node.replaceData(node.left.ikey,node.left.val,node.left.left,node.left.right)
            else:                                       #若被删除节点只有右子节点，则
                if node.isLeft():           #若被删除节点是左子节点，则
                    # 将被删除节点的右子节点的父节点指向被删除节点的父节点
                    node.right.parent=node.parent
                    # 将被删除节点的父节点的左子节点指向被删除节点的右子节点
                    node.parent.left=node.right
                    node.parent.balance-=1    #左节点少1
                elif node.isRight():        #若被删除节点是右子节点，则
                    # 将被删除节点的右子节点的父节点指向被删除节点的父节点
                    node.right.parent=node.parent
                    # 将被删除节点的父节点的右子节点指向被删除节点的右子节点
                    node.parent.right=node.right
                    node.parent.balance+=1    #右节点少1
                else:                               #若被删除节点无父节点，则被删除节点为根节点
                    # 替换被删除节点的右子节点的键、有效载荷、左子节点和右子节点数据
                    node.replaceData(node.right.ikey,node.right.val,node.right.left,node.right.right)
            if node.parent:     #非根节点需要重新平衡
                self.update2(node.parent)
                    
    #str转换方法
    def __str__(self):
        s=", ".join([f"{repr(key)}: {repr(self[key])}" for key in self])
        return f"{{{s}}}"
    
    __repr__=__str__

#创建字典类
class mydict:

    def getRoot(self):  # 返回内部的AVL树根
        return self.avltree.root

    def __init__(self):  # 创建一个空字典
        self.avltree=AVLTree()

    def __setitem__(self,key,value):  # 将key:value保存到字典
        # md[key]=value
        self.avltree[key]=value

    def __getitem__(self,key):  # 从字典中根据key获取value
        # v = md[key]
        # key在字典中不存在的话，请raise KeyError
        return self.avltree[key]

    def __delitem__(self,key):  # 删除字典中的key
        # del md[key]
        # key在字典中不存在的话，请raise KeyError
        del self.avltree[key]

    def __len__(self):  # 获取字典的长度
        # l = len(md)
        return len(self.avltree)

    def __contains__(self,key):  # 判断字典中是否存在key
        # k in md
        return key in self.avltree

    def clear(self):  # 清除字典
        self.avltree=AVLTree()

    def __str__(self):  # 输出字符串形式，参照内置dict类型，输出按照AVL树中序遍历次序
        # 格式类似：{'name': 'sessdsa', 'hello': 'world'}
        return str(self.avltree)

    __repr__ = __str__

    def keys(self):  # 返回所有的key，类型是列表，按照AVL树中序遍历次序
        l=[]
        for i in self.avltree:
            l.append(i)
        return l

    def values(self):  # 返回所有的value，类型是列表，按照AVL树中序遍历次序
        l=[]
        for i in self.avltree:
            l.append(self.avltree[i])
        return l
# 代码结束

#mydict=dict
# 检验
print("========= AVL树实现字典 =========")
md = mydict()
md['hello'] = 'world'
md['name'] = 'sessdsa'
print(md)  # {'name': 'sessdsa', 'hello': 'world'}

for f in range(1000):
    md[f**0.5] = f

for i in range(1000, 2000):
    md[i] = i**2

print(len(md))  # 2002
print(md[2.0])  # 4
print(md[1000])  # 1000000
print(md['hello'])  # world
print(20.0 in md)  # True
print(99 in md)  # False

del md['hello']
print('hello' in md)  # False
for i in range(1000, 2000):
    del md[i]
print(len(md))  # 1001
for f in range(1000):
    del md[f**0.5]
print(len(md))  # 1
print(md.keys())  # ['name']
print(md.values())  # ['sessdsa']
for a in md.keys():
    print(md[a])  # sessdsa
md.clear()
print(md)  # {}