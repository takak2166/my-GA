# -*- coding:UTF-8 -*-

import random

NBR_ITEMS = 30
MAX_WEIGHT = 50

items = {}
selected = [] #選ばれたアイテムを保持する

random.seed(1) #乱数の種を作っておく

for i in range(NBR_ITEMS):  #ランダムにアイテムを生成 前者が重さで後者が価値(不動点小数で定義)
    items[i] = (random.randint(1, 10), random.uniform(0, 100))

if __name__ == '__main__':

    dp = [[0 for i in range(MAX_WEIGHT+1)] for j in range(NBR_ITEMS)]

    for w in range(MAX_WEIGHT+1): #dpの初期化
        dp[0][w] = 0

    for i in range(NBR_ITEMS-1):
        for w in range(MAX_WEIGHT+1):
            if w >= items[i][0]:
                dp[i+1][w] =  max(dp[i][w-items[i][0]]+items[i][1], dp[i][w])
                if selected.count(items[i]) == 0:
                    selected.append(items[i])

            else:
                dp[i+1][w] = dp[i][w]

    print dp[NBR_ITEMS-1][MAX_WEIGHT]
    print selected
