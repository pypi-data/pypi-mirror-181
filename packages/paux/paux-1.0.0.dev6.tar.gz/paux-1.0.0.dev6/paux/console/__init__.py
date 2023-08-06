from pprint import pprint as _pprint


# 逐行打印内容
def pprint(*args):
    for arg in args:
        if type(arg) in [int, float, str]:
            print(arg)
        else:
            _pprint(arg)
    print('')
