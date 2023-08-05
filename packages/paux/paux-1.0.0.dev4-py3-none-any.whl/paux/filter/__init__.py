import time


class Filter():
    def __init__(self):
        self.filter_map = {}

    def set(self, name, filter_minute=5):
        ts = int(time.time())
        self.filter_map[name] = {
            'ts': ts,
            'expire': ts + filter_minute * 60
        }

    def check(self, name):
        '''
        :param name:
        :return:  True 不过滤 False 过滤
        '''
        # 没有在过滤内容中
        if not name in self.filter_map.keys():
            return True
        # 未超过过期时间
        if time.time() < self.filter_map[name]['expire']:
            return False
        # 超过了过期时间
        del self.filter_map[name]
        return True

    def clear(self):
        del_keys = []
        for key, v in self.filter_map.items():
            if time.time() >= v['expire']:
                del_keys.append(key)

        for key in del_keys:
            del self.filter_map[key]
