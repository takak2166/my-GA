# -*- coding:UTF-8 -*-

import random

NBR_ITEMS = 30
MAX_WEIGHT = 50

items = {}
selected = [] #選ばれたアイテムを保持する

random.seed(1) #乱数の種を作っておく

for i in range(NBR_ITEMS):  #ランダムにアイテムを生成 前者が重さで後者が価値(不動点小数で定義)
    items[i] = (random.uniform(0, 100), random.randint(1, 10) )

print items

if __name__ == '__main__':

    dp = [[0 for i in range(MAX_WEIGHT+1)] for j in range(NBR_ITEMS)]

    for i in range(NBR_ITEMS): #dpの初期化
        dp[i][0] = 0
    for  k in range(MAX_WEIGHT+1):
        if k < items[0][1]:
            dp[0][k] = 0
        else:
            dp[0][k] = items[0][1]

    for i in range(NBR_ITEMS-1):
        for w in range(MAX_WEIGHT+1):
            if w >= items[i][1]:
                dp[i+1][w] =  max(dp[i][w-items[i][1]]+items[i][0], dp[i][w])
            else:
                dp[i+1][w] = dp[i][w]

    # どのアイテムを選んだか確かめる
    w = MAX_WEIGHT
    for i in range(NBR_ITEMS)[:0:-1]:
        if w == 0:
            break
        if dp[i][w] != dp[i-1][w] :
            selected.append(items[i-1])
            w -= items[i-1][1]

    print dp[NBR_ITEMS-1][MAX_WEIGHT]
    print selected
    print len(selected)
    w_sum = 0
    v_sum = 0.0
    for i in selected:
        w_sum += i[0]
        v_sum += i[1]
    print w_sum
    print v_sum
