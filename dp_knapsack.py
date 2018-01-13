# -*- coding:UTF-8 -*-

import random

NBR_ITEMS = 30
MAX_WEIGHT = 10

items = {}

random.seed(1) #乱数の種を作っておく

for i in range(NBR_ITEMS):  #ランダムにアイテムを生成 前者が重さで後者が価値(不動点小数で定義)
    items[i] = (random.randint(1, 10), random.uniform(0, 100))

def dp(i, w):
    if i==w:
        return 0
    elif w >= items[i][0]:
        return max(dp(i-1, w-items[i][0])+items[i][1], dp(i-1, w))
    else:
        return dp(i-1, w)

if __name__ == '__main__':
    print dp(NBR_ITEMS-1, MAX_WEIGHT)
