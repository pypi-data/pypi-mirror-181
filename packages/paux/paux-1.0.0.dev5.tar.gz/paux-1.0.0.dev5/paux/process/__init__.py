'''
TODO 加入log日志
解决multiprocessing中Pool的不稳定性
'''
from multiprocessing import Process, Manager
import traceback
import time
from collections.abc import Iterable
from copy import deepcopy

def _pool_worker(q_param, q_result):
    while True:
        try:
            data = q_param.get(block=False, timeout=0)
            index = data['index']
            param = data['param']
            skip_exception = data['skip_exception']
            func = param['func']
            del param['func']
        except:
            break
        if skip_exception:
            try:
                ret = func(**param)
                q_result.put(
                    {
                        'index': index,
                        'data': ret
                    }
                )
            except:
                print(traceback.format_exc())
        else:
            ret = func(**param)
            q_result.put(
                {
                    'index': index,
                    'data': ret
                }
            )


def pool_worker(params, p_num=4, func=None, skip_exception=False):
    results = [None] * len(params)
    # 标准化param，让param中存在要执行的函数func
    q_param = Manager().Queue()
    q_result = Manager().Queue()
    for index, param in enumerate(params):
        # param['func']优先级最高
        # 存在    param['func']
        if 'func' in param.keys() and param['func'] != None:
            pass
        # 不存在   param['func']
        else:
            # 有func
            if func != None:
                param['func'] = func
            # 无func
            else:
                raise Exception('没有执行的函数func')  # todo
        q_param.put(
            {
                'index': index,
                'param': param,
                'skip_exception': skip_exception
            }
        )
    # 单进程运行
    if p_num <= 1:
        _pool_worker(q_param, q_result)
    # 多进程运行
    else:
        processes = []
        for i in range(p_num):
            p = Process(target=_pool_worker, kwargs={'q_param': q_param, 'q_result': q_result})
            processes.append(p)
            p.start()

        def wait_processes(processes):
            for p in processes:
                if p.is_alive():
                    return False
            return True

        # 等待进程均运行完成
        while True:
            if wait_processes(processes):
                break
            else:
                time.sleep(1)
    # 整理结果
    for i in range(q_result.qsize()):
        result = q_result.get(block=False, timeout=0)
        index = result['index']
        data = result['data']
        # 按照索引赋值，如果某个参数执行异常并且skip_exception，这个结果为None
        results[index] = data
    return results




