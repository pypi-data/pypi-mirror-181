# -*- coding: utf-8 -*-
from collections import Counter

__all__ = [
    'find_duplicate',
]


def find_duplicate(file_list):
    b = dict(Counter(file_list))
    print([key for key, value in b.items() if value > 1])  # 只展示重複元素
    print({key: value for key, value in b.items() if value > 1})  # 展現重複元素和重複次數
    return b
