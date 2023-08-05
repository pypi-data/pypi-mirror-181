import os

def mkdir_ifnot_exists(path):
    '''
    '''
    if not os.path.exists(path):
        os.makedirs(path)
    return path
