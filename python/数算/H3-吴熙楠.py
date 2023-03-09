class Stack:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[len(self.items) - 1]

    def size(self):
        return len(self.items)
    
class Queue:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0, item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)
    
class Node():
    def __init__(self, initdata=None):
        self.data = initdata
        self.next = None
        self.prev = None

    def getData(self):
        return self.data

    def getNext(self):
        return self.next

    def getPrev(self):
        return self.prev
    
    def setData(self, newdata):
        self.data = newdata

    def setNext(self, newnext):
        self.next = newnext

    def setPrev(self, newprev):
        self.prev = newprev
        
def calculate(s) -> float:
    token_list = s.split()
    pre_dict = {"^":4,"*":3,"/":3,"+":2,"-":2,"(":1}
    operator_stack = []
    operand_stack = []
    for token in token_list:
        if token.isdecimal() or token[1:].isdecimal():
            operand_stack.append(float(token))
        elif token == '(':
            operator_stack.append(token)
        elif token == ')':
            top = operator_stack.pop()
            while top != '(':
                op2 = operand_stack.pop()
                op1 = operand_stack.pop()
                operand_stack.append(get_value(top,op1,op2))
                top = operator_stack.pop()
        elif token in '+-*/^':
            while operator_stack and pre_dict[operator_stack[-1]] >= pre_dict[token]:
                top = operator_stack.pop()
                op2 = operand_stack.pop()
                op1 = operand_stack.pop()
                operand_stack.append(get_value(top,op1,op2))
            operator_stack.append(token)
    while operator_stack:
        top = operator_stack.pop()
        op2 = operand_stack.pop()
        op1 = operand_stack.pop()
        operand_stack.append(get_value(top,op1,op2))
    return operand_stack.pop()
 
def get_value(operator : str, op1 :float, op2 : float):
    if operator == '+':
        return op1 + op2
    elif operator == '-':
        return op1 - op2
    elif operator == '*':
        return op1 * op2
    elif operator == '/':
        return op1 / op2
    elif operator == '^':
        if op1!=0:
            return op1**op2
        elif op2>0:
            return 0
        else:
            return error

def radix_sort(s) -> list:
    l1=[]
    q=[Queue() for i in range(10)]
    qm=Queue()
    qf=Queue()
    k=len(str(max(s)))
    for i in s:
        qm.enqueue(i)
        qf.enqueue(i)
    for j in range(k):
        while not qm.isEmpty():
            m=qm.dequeue()
            s=qf.dequeue()
            n=s%10
            q[n].enqueue(m)
        for i in range(10):
            while not q[i].isEmpty():
                x=q[i].dequeue()
                qm.enqueue(x)
                qf.enqueue(int(x/10**(j+1)))
    while not qm.isEmpty():
        l1.append(qm.dequeue())
    return l1

def HTMLMatch(s) -> bool:
    stack = Stack()
    z=0
    for i in s:
        if i=="<":
            flag = 0
            temp = ""
            temp += i
            z+=1
        elif i ==">":
            temp += i
            if flag:
                if stack.isEmpty() == False:
                    temp = temp.replace("/","")
                    if temp == stack.peek():
                        stack.pop()                     
            else:
                stack.push(temp)
            temp = ""
        else:
            if i=="/":
                flag=1
            temp += i
    if stack.isEmpty() and z%2==0:
        return True
    else:
        return False

class LinkStack():
    def __init__(self):
        self.data = None
        self.next = None

    def isEmpty(self):
        if self.next == None:
            return True
        return False

    def size(self):
        size=0
        p = self.next
        while p != None:
            p = p.next
            size += 1
        return size

    def push(self, element):
        p = Node(element)
        p.data = element
        p.next = self.next
        self.next = p

    def pop(self):
        tmp = self.next
        if tmp != None:
            self.next = tmp.next
        else:
            print("栈已经为空")
        return tmp.data
    
    def peek(self):
        tmp = self.next
        if tmp == None:
            print("栈已经为空")
        else:
            return tmp.data
        
class LinkQueue():
    def __init__(self):
        self.pHead = None
        self.pEnd = None

    def isEmpty(self):
        if self.pHead == None:
            return True
        return False

    def size(self):
        size=0
        p = self.pHead
        while p != None:
            p = p.next
            size += 1
        return size

    def enqueue(self, element):
        p = Node(element)
        p.data = element
        p.next = None
        if self.pHead == None:
            self.pHead = self.pEnd=p
        else:
            self.pEnd.next = p
            self.pEnd = p

    def dequeue(self):
        tmp=self.pHead
        if self.pHead == None:
            print("出队列失败，队列已经为空")
        else:
            self.pHead = self.pHead.getNext()
            return tmp.getData()

class DoublyLinkedList():
    def __init__(self,*items):
        self.head = None
        self.tail = None
        for i in items:
            self.append(i)

    def getTail(self):
        self.tail=self.head
        while self.tail.getNext()!=None:
            self.tail=self.tail.getNext()
        return self.tail

    def isEmpty(self):
        return self.head == None
    
    def add(self,item):
        temp = Node(item)
        if self.isEmpty():
            self.head=temp
        else:
            temp.setNext(self.head)
            self.head.setPrev(temp)
            temp.setPrev(None)
            self.head = temp
 
    def size(self):
        current = self.head
        count = 0
        while current != None:
            count = count + 1
            current = current.getNext()
        return count
 
    def search(self,item):
        current = self.head
        found = False
        while current != None and not found:
            if current.getData() == item:
                found = True
            else:
                current = current.getNext() 
        return found
    
    def remove(self,item):
        current = self.head
        previous = None
        found = False
        while not found:
            if current.getData() == item:
                found = True
            else:
                previous = current
                current = current.getNext()
        if previous == None:
            self.head = current.getNext()
        else:
            previous.setNext(current.getNext())
            if current.getNext()!=None:
                current=current.getNext()
                current.setPrev(previous)
             
    def append(self,item):
        temp=Node(item)
        if self.isEmpty():
            self.head=temp
        else:
            current=self.head
            while current.getNext()!=None:
                current=current.getNext()
            current.setNext(temp)
            temp.setPrev(current)
            
    def insert(self,pos,item):
        if pos==0:
            self.add(item)
        elif pos==self.size()-1:
            self.append(item)
        elif 0<pos<len(self)-1:
            temp=Node(item)
            count=0
            previous=None
            current=self.head
            while count<pos:
                count+=1
                previous=current
                current=current.getNext()
            previous.setNext(temp)
            temp.setPrev(previous)
            temp.setNext(current)
            current.setPrev(temp)
            
    def index(self,item):
        current=self.head
        count=-1
        found=False
        while current!=None and not found:
            count+=1
            if current.getData()==item:
                found=True
            else:
                current=current.getNext()
        if found:
            return count
        else:
            print('not found')
            
    def __len__(self):
        return self.size()
    
    def __str__(self):
        st="["
        current=self.head
        while current!=None:
            st+=repr(current.getData())
            if current.getNext()!=None:
                st+=","
            current=current.getNext()
        st+="]"
        return st
    
    def __getitem__(self, key=-1):
        if  isinstance(key, slice):
            l1=self.__class__()
            a=key.start;b=key.stop;c=key.step;d=len(self)
            if -d<a<0:
                a+=d
            elif a<=-d:
                a=0
            else:
                a+=0
            if b<0:
                b+=d
            elif b>d:
                b=d
            else:
                b+=0
            for i in range(a,b,c):
                l1.append(self[i])
            return l1
        elif 0<=key<len(self):
            p = self.head
            num = -1
            while p:
                num += 1
                if key == num:
                    return p.getData()
                else:
                    p = p.getNext()
        
    def pop(self,key=-1):
        previous = None
        current = self.head
        if key==0:
            self.head=self.head.getNext()
        elif key==-1:
            while current.getNext() !=None:
                previous = current
                current=current.getNext()
        elif  0<key<len(self):
            for i in range(key):
                previous=current
                current=current.getNext()
        m=current.getData()
        previous.setNext(current.getNext())
        if current.getNext()!=None:
            current=current.getNext()
            current.setPrev(previous)        
        return m
    
    def __iter__(self):
        if not self.head:
            return
        cur = self.head
        yield cur.getData()
        while cur.getNext():
            cur = cur.getNext()
            yield cur.getData()
            
    def __eq__(self,other):
        if self is other:
            return True
        if type(self)!=type(other) or len(self)!=len(other):
            return False
        for item in self:
            if not item in other:
                return False
        return True