from itertools import combinations, permutations

import numpy as np


def permut(choice_list: list, pick_num: int):
    """
    排列数
    :param choice_list:
    :param pick_num:
    :return:
    """
    return permutations(choice_list, pick_num)


def combin(choice_list: list, pick_num: int):
    """
    组合数
    :param choice_list:
    :param pick_num:
    :return:
    """
    return combinations(choice_list, pick_num)



if __name__ == '__main__':
    l=[3,6,7]
    x=combin(l,2)
    for i in x:
        print(i)