class BinaryTree:
    def __init__(self,x):
        self.key = x
        self.leftChild = None
        self.rightChild = None
    def insertLeft(self,newNode):
        if self.leftChild == None:
            self.leftChild = BinaryTree(newNode)
        else:
            t = BinaryTree(newNode)
            t.leftChild = self.leftChild
            self.leftChild = t
    def insertRight(self,newNode):
        if self.rightChild == None:
            self.rightChild = BinaryTree(newNode)
        else:
            t = BinaryTree(newNode)
            t.rightChild = self.rightChild
            self.rightChild = t
    def getRightChild(self):
        return self.rightChild
    def getLeftChild(self):
        return self.leftChild
    def setkey(self,obj):
        self.key = obj
    def getkey(self):
        return self.key
    def getHeight(self,root):
        if root==None:
            return 0
        else:
            root.key = 1 + max(self.getHeight(root.leftChild), self.getHeight(root.rightChild))
            return root.key
    def tree(self,root):
        if root == None:
            return '['+']'
        else:
            s='['+root.getkey()+','+self.tree(root.leftChild)+','+self.tree(root.rightChild)+']'
            return s
r = BinaryTree('a')
r.insertLeft('b')
r.insertRight('c')
r.getLeftChild().insertRight('d')
r.getRightChild().insertLeft('e')
r.getRightChild().insertRight('f')
print(r.tree(r))
print(r.getHeight(r))