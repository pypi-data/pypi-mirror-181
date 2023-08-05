'''
与平台相关的函数
'''

import platform
import os


def get_platform():
    sys_platform = platform.platform().upper()
    sys_names = (
        'WINDOWS', 'MACOS', 'LINUX'

    )
    for sys_name in sys_names:
        if sys_name in sys_platform:
            return sys_name
    return 'OTHER'


def get_maxOs_documents_path():
    root_path = '/Users'
    filepaths = []
    for filename in os.listdir(root_path):
        if filename.startswith('.'):
            continue
        if filename == 'Shared':
            continue
        filepath = os.path.join(root_path, filename)
        if os.path.isdir(filepath) and 'Documents' in os.listdir(filepath):
            filepaths.append(filepath)

    if not filepaths:
        raise Exception('没有找到MacOs用户名')
    documents_path = os.path.join(
        filepaths[0], 'Documents'
    )
    return documents_path


if __name__ == "__main__":
    print(get_platform())
    print(get_maxOs_documents_path())
