# H5测评机
from random import randrange, choice, choices, uniform
from sys import stderr
import string

print_bak = globals().get('print_bak', print)  # 使用另行备份的print函数
d1, d2 = mydict(), dict()


def ranstr(num):
    salt = ''.join(choices(string.ascii_letters + string.digits, k=num))
    return salt


print_bak("========= 插入与取值测试 =========")
key = choice((randrange(-1000, -1), randrange(1000)))
val = choice([randrange(-1000, 1000), ranstr(randrange(1, 20)), uniform(-100, 100)])
try:
    for _ in range(100):
        key = choice((randrange(-1000, -1), randrange(1000)))
        val = choice([randrange(-1000, 1000), ranstr(randrange(1, 40)), uniform(-100, 100)])
        d1[key] = val
        d2[key] = val
        assert d1[key] == d2[key], f'''key:{key},value 应为{d2[key]},输出{d1[key]}'''
    print_bak('pass')
    for _ in range(100):
        key = ranstr(randrange(1, 40))
        val = choice([randrange(-1000, 1000), ranstr(randrange(1, 40)), uniform(-100, 100)])
        d1[key] = val
        d2[key] = val
        assert d1[key] == d2[key], f'''key:{key},value 应为{d2[key]},输出{d1[key]}'''
    print_bak('pass')
    for _ in range(100):
        key = uniform(-100, 100)
        val = choice([randrange(-1000, 1000), ranstr(randrange(1, 40)), uniform(-100, 100)])
        d1[key] = val
        d2[key] = val
        assert d1[key] == d2[key], f'''key:{key},value 应为{d2[key]},输出{d1[key]}'''
    print_bak('pass')
except Exception as e:
    print_bak(f'出错操作:插入key:{key}', file=stderr)
    # print_bak(f'测试字典:{d2}', file=stderr)
    # print_bak(f'输出字典:{d1}', file=stderr)
    print_bak(f'打印报错:{type(e).__name__}:{str(e)}', file=stderr)
print_bak("========= 删除与打印测试 =========")
key = None
try:
    while d2:
        key = choice(list(d2.keys()))
        del d1[key]
        del d2[key]
        assert eval(str(d1)) == d2, f'''删除key:{key}后发生错误'''
    print_bak('pass')
except Exception as e:
    if type(e).__name__ == SyntaxError:
        print_bak('请检查你的__str__操作是否正确', file=stderr)
    print_bak(f'出错操作:删除key:{key}', file=stderr)
    # print_bak(f'参考输出:{d2}', file=stderr)
    # print_bak(f'实际输出:{d1}', file=stderr)
    print_bak(f'打印报错:{type(e).__name__}:{str(e)}', file=stderr)
print_bak("========= 包含与keys,values测试 =========")
key, val = choices([choice((randrange(-1000, -1), randrange(1000))), ranstr(randrange(1, 20)), uniform(-100, 100)], k=2)
for _ in range(1000):
    key, val = choices([choice((randrange(-1000, -1), randrange(1000))), ranstr(randrange(1, 20)), uniform(-100, 100)],
                       k=2)
    d1[key] = val
    d2[key] = val
try:
    for x in d2:
        assert x in d1, f'''keyError:{x} is not in mydict,请检查__contain__函数'''
        assert x in d1.keys(), f'''keyError:{x} is not in mydict.keys,请检查keys函数'''
    print_bak('pass')
    assert set(d1.keys()) == set(d2.keys()), '''keys返回值错误,请检查keys函数'''
    assert set(d2.values()) == set(d2.values()), '''values返回值错误,请检查values函数'''
    print('pass')
except Exception as e:
    print_bak(f'打印报错:{type(e).__name__}:{str(e)}', file=stderr)
print_bak("========= 长度与清空测试 =========")
try:
    assert len(d1) == len(d2), '''__len__错误'''
    while len(d2) > 1:
        key = choice(list(d2.keys()))
        del d1[key]
        del d2[key]
        assert len(d1) == len(d2), '''__len__错误'''
    print_bak('pass')
    d1.clear()
    d2.clear()
    print_bak(d1)
    assert d1.getRoot() == None, '''clear错误'''
    assert len(d1) == 0, '''clear错误'''
    print_bak('pass')
except Exception as e:
    print_bak(f'打印报错:{type(e).__name__}:{str(e)}', file=stderr)
print_bak("========= 平衡性测试 =========")


def height(root):
    return (1 + max(height(root.getLeft()), height(root.getRight()))) if root else -1


def check(b):
    def _check(root):
        if root:
            if abs(height(root.getLeft()) - height(root.getRight())) <= 1:
                return _check(root.getLeft()) and _check(root.getRight())
            else:
                return False
        else:
            return True

    return _check(b.getRoot())


try:
    key, val = choices([choice((randrange(-1000, -1), randrange(1000))), ranstr(randrange(1, 20)), uniform(-100, 100)],
                       k=2)
    for _ in range(1000):
        key, val = choices(
            [choice((randrange(-1000, -1), randrange(1000))), ranstr(randrange(1, 20)), uniform(-100, 100)],
            k=2)
        d1[key] = val
        d2[key] = val
        assert check(d1), f'''插入key:{key}之后左右子树不平衡'''
    print_bak('pass')
    while d2:
        key = choice(list(d2.keys()))
        del d1[key]
        del d2[key]
        assert check(d1), f'''删除key:{key}之后左右子树不平衡'''
    print_bak('pass')
except Exception as e:
    print_bak(f'打印报错:{type(e).__name__}:{str(e)}', file=stderr)