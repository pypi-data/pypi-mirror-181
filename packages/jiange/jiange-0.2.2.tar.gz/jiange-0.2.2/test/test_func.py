
import os
import sys
PATH_PRJ = '/'.join(os.path.abspath(__file__).split('/')[:-2])
sys.path.append(PATH_PRJ)
from jiange.file import load_xlsx, save_xlsx


def test_load_xlsx():
    path_src = '/Users/zhanglinjian1/Documents/project/Fuxinlp-Demo/data/graphdata/节点-keyword.xlsx'
    data = load_xlsx(path_src, return_all=True)
    for k, v in data.items():
        print(f'{k} {len(v)}')


def test_save_xlsx():
    path_tgt = '/Users/zhanglinjian1/Desktop/test.xlsx'
    data = [
        [[1, 2, 3]],
        [[3, 4, 5]]
    ]
    titles = [['a', 'b', 'c'], ['c', 'd', 'e']]
    save_xlsx(data, path_tgt, titles=titles)


if __name__ == '__main__':
    test_load_xlsx()
    test_save_xlsx()
