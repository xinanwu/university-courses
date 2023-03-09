#uuid_share#  b2215cc4-9ec0-4c44-b144-b65c061be00c  #
# SESSDSA20 H3 随机测试样例P1

from random import randrange, shuffle, choice
from sys import stderr, stdout
print_bak = globals().get('print_bak', print)  # 使用另行备份的print函数

from collections import Counter


class Node:  # 检测规范调用接口
    invalid_key = Counter()

    def __init__(self, initdata=None):
        self.__data = initdata
        self.__next = None
        self.__prev = None

    for k in ('data', 'next', 'prev'):
        exec(f'''@property
def {k}(self):
    self.invalid_key['get_'+'{k}']+=1
    return getattr(self,'get'+'{k.capitalize()}')()
@{k}.setter
def {k}(self,val):
    self.invalid_key['set_'+'{k}']+=1
    getattr(self,'set'+'{k.capitalize()}')(val)''', globals(), locals())

    def getData(self):
        return self.__data

    def getNext(self):
        return self.__next

    def getPrev(self):
        return self.__prev

    def setData(self, newdata):
        self.__data = newdata

    def setNext(self, newnext):
        self.__next = newnext

    def setPrev(self, newprev):
        self.__prev = newprev


# ======= 1 中缀表达式求值 =======
def gen_exp():
    pool = ['@']
    op_expand = randrange(7)
    op_group = randrange(4)
    ops = [''] * op_expand + ['()'] * op_group
    shuffle(ops)

    has_pow = False
    for op in ops:
        tmp = list(i for i, x in enumerate(pool) if x == '@')
        tmp = choice(tmp)
        if op:  # add brackets
            pool.insert(tmp + 1, ')')
            pool.insert(tmp, '(')
            tmp += 1
        # expand expr
        op = '+-*/^' [randrange(5)]
        if op == '^':
            if has_pow:
                op = '+-*/' [randrange(4)]
            else:
                has_pow = True
        pool.insert(tmp + 1, '@')
        pool.insert(tmp + 1, op)

    for i, x in enumerate(pool):
        if x == '@':
            pool[i] = str(randrange(12))

    expr = ' '.join(pool)

    try:  # 有效性检查
        res = eval(expr.replace('^', '**'))
        res1 = eval(expr.replace('/', '//').replace('^', '**'))
        ress = (res, res1)
        assert all(1e-8 < abs(x) < 1e8 and type(x).__name__ != 'complex'
                   and str(x) != 'nan' for x in ress)
        return expr, (res, res1)
    except:
        return gen_exp()


print_bak("======== 1 中缀表达式求值 ========")
try:
    cases = [
        ('114514', (114514, 114514)),
    ]
    for test in range(20):
        res1 = None
        if test < len(cases):
            expr, ress = cases[test]
        else:
            expr, ress = gen_exp()
        res1 = calculate(expr)
        if not any(
                abs((r - res1) / r) < 1e-6 if r else r == res1 for r in ress):
            raise AssertionError('参考答案: %s 或 %s' % ress)
    print_bak('>>> PASS')
except Exception as e:
    print_bak(f'''调用: calculate({repr(expr)})''', file=stderr)
    print_bak(f'输出: {repr(res1)}', file=stderr)
    print_bak(f'{type(e).__name__}: {e}', file=stderr)

# ======= 2 基数排序 =======
print_bak("======== 2 基数排序 ========")
try:
    cases = []
    for test in range(20):
        res1 = None
        if test < len(cases):
            lst = cases[test]
        else:
            lst = [randrange(1000) for i in range(randrange(10, 50))]
        res = sorted(lst)
        res1 = radix_sort(lst[:])
        assert res == res1, f'''参考答案: {res}'''
    print_bak('>>> PASS')
except Exception as e:
    print_bak(f'''调用: radix_sort({repr(lst).replace(' ','')})''', file=stderr)
    print_bak(f'输出: {repr(res1)}', file=stderr)
    print_bak(f'{type(e).__name__}: {e}', file=stderr)

# ======= 3 HTML =======


def gen_xml(make_invalid=False):
    pool = []
    n_pairs = randrange(1, 15)
    from string import ascii_letters, ascii_lowercase
    text_pool = ascii_letters + "0123546789" + ' ' * 50

    for i in range(n_pairs):
        tag = ''.join(choice(ascii_lowercase) for i in range(randrange(1, 5)))
        tmp = randrange(len(pool) + 1)
        pool.insert(tmp, f'</{tag}>')
        pool.insert(tmp, f'<{tag}>')

    if make_invalid:
        for i in range(3):
            if not pool:
                break
            pool.pop(randrange(len(pool)))
    pool.append('</html>')

    res = ['<html>']
    for node in pool:
        res.append(''.join(choice(text_pool) for i in range(randrange(10))))
        res.append(node)

    return ''.join(res)
ref_match=lambda s:(lambda l:not any(map(lambda t:t[1]!=l.pop()[1] if t[0] else l.append(t),__import__('re').findall('<(/?)(.*?)>', s))) and not l)([])

print_bak("======== 3 HTML MATCH ========")
try:
    cases = [
        ('<html></html>', True),
        ('<html>', False),
        ('</html>', False),
    ]
    for test in range(20):
        res1 = None
        if test < len(cases):
            expr, res = cases[test]
        else:
            expr = gen_xml(test % 2)
            res = ref_match(expr)
        res1 = HTMLMatch(expr)
        assert res == res1, f'''参考答案: {res}'''
    print_bak('>>> PASS')
except Exception as e:
    print_bak(f'''调用: HTMLMatch({repr(expr)})''', file=stderr)
    print_bak(f'输出: {repr(res1)}', file=stderr)
    print_bak(f'{type(e).__name__}: {e}', file=stderr)

# SESSDSA20 H3 随机测试样例P2
LINE_WIDTH = 50
N_TESTS = 10
N_OPS = 20

from collections import deque
from random import randrange, choice
from sys import stderr

if 'ref ds':

    class ref_node:
        def __init__(self, lst, ind):
            self.lst = lst
            self.ind = ind

        def getData(self):
            return self.lst[self.ind]

        def getNext(self):
            return ref_node(self.lst, self.ind + 1)

        def getPrev(self):
            return ref_node(self.lst, self.ind - 1)

        def setData(self, newdata):
            self.lst[self.ind] = newdata

        def __eq__(self, other):
            try:
                return self.getData() == other.getData()
            except:
                return False

    ref_node.__str__ = lambda self: 'Node(%r)' % self.getData()
    Node.__str__ = Node.__repr__ = ref_node.__repr__ = ref_node.__str__

    class ref_list:
        isEmpty = lambda self: not self.lst
        add = lambda self, item: self.lst.insert(0, item)
        search = lambda self, item: item in self.lst
        size = __len__ = lambda self: len(self.lst)

        def __init__(self, ref_type, it=None):
            self.ref_type = ref_type
            self.lst = []
            if it:
                for i in it:
                    self.lst.append(i)

        def getTail(self):
            assert self.size() > 0
            return ref_node(self.lst, len(self) - 1)

        def __getitem__(self, arg):
            res = self.lst[arg]
            if isinstance(arg, slice):
                res = ref_list(self.ref_type, res)
            return res

        def __eq__(self, other):
            try:
                if len(self) != len(other):
                    return False
                tmp = [(self[i], other[i]) for i in range(len(self))]
                return all(i == j for i, j in tmp)
            except:
                return False

        __str__ = __repr__ = lambda self: f'{self.ref_type.__name__}({self.lst})'

    class ref_deque(deque):
        push = deque.append
        peek = lambda self: self[-1]
        enqueue = deque.append
        dequeue = deque.popleft
        isEmpty = lambda self: not bool(self)
        size = deque.__len__


def test(i, t_lst, r_lst, op_write, op_read):
    print_bak('TEST #%d' % i, end='')
    _SIZE = 0
    passed = True
    ops = []
    params = []

    def get(param):
        if param == 'num':
            return randrange(N_OPS)
        elif param == 'numstr':
            if randrange(2):
                return randrange(N_OPS)
            return str(randrange(10))
        elif param == 'len':
            return randrange(_SIZE)
        elif param == '-len':
            return randrange(_SIZE) - _SIZE
        elif param == 'slice':
            a = randrange(_SIZE - 1)
            b = randrange(a, _SIZE + 1)
            return slice(a, b, randrange(1, 10))

    def one_check(op):
        ref_exec = True
        op = op.split()

        try:
            params.clear()
            params.extend(map(get, op[1:]))
            r_ref = getattr(r_lst, op[0])(*params)
        except:
            ref_exec = False

        if ref_exec:
            r_test = getattr(t_lst, op[0])(*params)
            if r_ref != None:
                assert r_ref == r_test, '输出: %r;\n应该输出: %r' % (r_test, r_ref)
                if isinstance(r_ref, ref_list):
                    assert type(
                        r_test) == r_ref.ref_type, '输出类型错误: %s;\n应为: %s' % (
                            type(r_test).__name__, r_ref.ref_type.__name__)

            ops.append((op[0], *params))

    def output(op):
        func = op[0]
        params = ','.join(map(repr, op[1:]))
        return '%s(%s)' % (func, params)

    try:
        for i in range(N_OPS):
            # write one
            curr_op = choice(op_write)
            one_check(curr_op)

            # update size
            _SIZE = len(r_lst)

            # read one
            curr_op = choice(op_read)
            one_check(curr_op)

        print_bak(' PASS')
    except Exception as e:
        print_bak('\n出错的操作:', output((curr_op.split()[0], *params)))
        print_bak('历史操作:', ','.join(map(output, ops)))
        print_bak('报错: (%s: %s)' % (type(e).__name__, str(e)), file=stderr)
        try:
            print_bak('LAST LISTS'.center(LINE_WIDTH, '.'))
            print_bak('参考列表:', r_lst)
            print_bak('测试列表:', t_lst)
        except Exception as e:
            print_bak(
                '打印报错 (%s: %s)' % (type(e).__name__, str(e)), file=stderr)
        print_bak('END'.center(LINE_WIDTH, '.'))


def test_code(title, code):
    print_bak(title, end=':\n')
    # print_bak('Code'.center(LINE_WIDTH, '.'))
    # print_bak(code)
    try:
        exec(code, globals())
    except Exception as e:
        print_bak('报错 (%s: %s)' % (type(e).__name__, str(e)), file=stderr)


def prev_iter(lst):
    node = lst.getTail()
    res = []
    for i in range(len(lst)):
        res.append(node.getData())
        node = node.getPrev()
    return res


def safe_iter(lst):
    lst_iter = iter(lst)
    for i in range(len(lst)):
        yield next(lst_iter)
    try:
        not_end = next(lst_iter)
        yield 'NOT END'
    except:
        pass


# push pop peek
print_bak('\n' + "1 LinkStack".center(LINE_WIDTH, '='))
for i in range(N_TESTS):
    test(i, LinkStack(), ref_deque(), (
        'push num',
        'pop',
    ), (
        'isEmpty',
        'peek',
        'size',
    ))

# enqueue dequeue
print_bak('\n' + "2 LinkQueue".center(LINE_WIDTH, '='))
for i in range(N_TESTS):
    test(i, LinkQueue(), ref_deque(), (
        'enqueue num',
        'dequeue',
    ), (
        'isEmpty',
        'size',
    ))

# getTail
print_bak('\n' + "3 DoublyLinkedList".center(LINE_WIDTH, '='))
for i in range(N_TESTS):
    l1 = DoublyLinkedList()
    l2 = ref_list(DoublyLinkedList)
    test(i, l1, l2, (
        'append numstr',
        'add numstr',
        'insert len numstr',
        'pop len',
        'pop',
        'remove numstr',
    ), (
        'isEmpty',
        'search numstr',
        'size',
        '__len__',
        'index numstr',
        '__getitem__ len',
        '__getitem__ slice',
        'getTail',
    ))
    test_code('prev link test', r'''r1=prev_iter(l1)
r2=l2[::-1]
if r1==r2:
    print_bak('PASS')
else:
    print_bak('双链表倒序结果: ',r1,file=stderr)
    print_bak('参考结果: ',r2,file=stderr)''')

comment = '''
注：prev link test用于测试双链表反向连接情况
以上为必做内容，以下为选做内容
'''
try:
    from browser import document
    target = document['py_stdout']
    target.innerHTML += f'<span style="color:blue">{comment}</span>'
except ImportError:
    print_bak(comment, file=stderr)

# Additional


def print_helper(text, cond):
    print_bak(text, end=' ')
    print_bak(cond, file=stdout if cond else stderr)


print_bak('\n' + "Ex DoublyLinkedList".center(LINE_WIDTH, '='))
test_code('__eq__+__iter__ test', '''lst=DoublyLinkedList(range(5))
print_bak('lst:',lst)
print_helper('lst==DoublyLinkedList(range(5)) -> T:',lst==DoublyLinkedList(range(5)))
print_helper('lst!=DoublyLinkedList(range(6)) -> T:',lst!=DoublyLinkedList(range(6)))
print_helper('lst!=list(range(5)) -> T:',lst!=list(range(5)))
print_helper('lst!=None -> T:',lst!=None)
print_helper('lst==DoublyLinkedList(lst) -> T:',lst==DoublyLinkedList(safe_iter(lst)))
mtest=[(x,y) for x in safe_iter(lst) for y in safe_iter(lst)]
print_helper('多iter测试 -> T:',mtest==[(x,y) for x in range(5) for y in range(5)])'''
          )
test_code('-slice test', '''lst='DoublyLinkedList(range(50))'
print_bak('list:',lst)
lst=eval(lst)
all_pass=1
for i in range(20):
    sli=slice(randrange(-100,100),randrange(-100,100),randrange(1,10)*(randrange(2)*2-1))
    l1=list(lst[sli])
    l2=list(range(50)[sli])
    if l1!=l2:
        all_pass=0
        print_bak('FAIL:',sli,l1,l2,file=stderr)
        print_bak('RESULT:',l1,file=stderr)
        print_bak('SHOULD BE:',l2,file=stderr)
if all_pass:
    print_bak('PASS')''')

if Node.invalid_key:
    print_bak('非法调用:', dict(Node.invalid_key), file=stderr)