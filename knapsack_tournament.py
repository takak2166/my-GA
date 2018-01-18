# -*- coding: utf-8 -*-
import random
import numpy as np

from deap import algorithms
from deap import base
from deap import creator
from deap import tools

import matplotlib.pyplot as plt
import numpy as np

from operator import attrgetter
from operator import itemgetter

# 適合度クラスを作成
creator.create("Fitness", base.Fitness, weights=(1.0, -1.0))
creator.create("Individual", set, fitness=creator.Fitness)  # setは重複がない集合

# アイテムの重さと体積をランダムに決める
NBR_ITEMS = 30
IND_INIT_SIZE = 5  # 最初に選ぶアイテムの個数
# MAX_ITEM = 3
MAX_WEIGHT = 50

items = {}

random.seed(1)  # 乱数の種を作っておく

# 前者が価値で後者が重さ
for i in range(NBR_ITEMS):
    items[i] = (random.uniform(0, 100), random.randint(1, 10))

print items

toolbox = base.Toolbox()
# Attributeを生成する関数を定義
toolbox.register("attr_item", random.randrange, NBR_ITEMS)
# 個体を生成する関数を定義(Individualクラスでattr_itemの値をいくつか持つ)
toolbox.register("individual", tools.initRepeat,
                 creator.Individual, toolbox.attr_item, IND_INIT_SIZE)
# 集団を生成する関数を定義
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# 評価関数


def evalknapsack(individual):
    value = 0.0
    weight = 0.0
    for item in individual:
        value += items[item][0]
        weight += items[item][1]
    if weight > MAX_WEIGHT:
        return 0, 10000
    return value, weight


def cxSet(ind1, ind2):
    """1番目の子は二つのセットの交叉(AND)で
    2番目の子は違う二つのセットの交叉(XOR).
    """
    temp = set(ind1)
    ind1 &= ind2
    ind2 ^= temp
    return ind1, ind2


def mutSet(individual):
    """突然変異・挿入"""
    if random.random() < 0.5:
        if len(individual) > 0:  # 空になったら取り出せない
            individual.remove(random.choice(sorted(tuple(individual))))
    else:
        individual.add(random.randrange(NBR_ITEMS))
    return individual,


def selBest(inds, k, fit_attr="fitness.wvalues"):
    """選択"""
    return sorted(inds, key=attrgetter(fit_attr), reverse=True)[:k]


# 評価関数を登録
toolbox.register("evaluate", evalknapsack)
# 交叉関数を登録
toolbox.register("mate", cxSet)
# 変異関数を登録
toolbox.register("mutate", mutSet)
# 選択関数を登録
toolbox.register("select", tools.selTournament, tournsize=4)


def main():
    NGEN = 100  # 世代数
    MU = 200  # 集団の数
    LAMBDA = 100  # 子供の数
    CXPB = 0.3  # 交叉率
    MUTPB = 0.6  # 突然変異率

    pop = toolbox.population(n=MU)
    # print pop
    hof = tools.ParetoFront()  # 進化の中で最も優れている個体を保存

    # 初期集団の個体を評価
    fitnesses = [[]]
    fitnesses = list(map(toolbox.evaluate, pop))

    for ind, fit in zip(pop, fitnesses):  # zipは複数変数の同時ループ
        # 適合性をセットする
        ind.fitness.values = fit

    fig, ax = plt.subplots(1, 1)
    x = np.arange(0)
    y = np.array([])
    ax.set_xlim(0, NGEN)
    ax.set_ylim(0, 950)
    lines, = ax.plot(x, y)

    # 進化計算開始
    for g in range(NGEN):

        print("--- %i generations ---" % g)

        # 選択
        offspring = toolbox.select(pop, len(pop))
        offspring = list(map(toolbox.clone, offspring))
        # print offspring

        # 交叉
        #  上位1%以内は保持
        for child1, child2 in zip(offspring[MU / 100::2], offspring[MU / 100 + 1::2]):
            if random.random() < CXPB:
                toolbox.mate(child1, child2)
                # 交叉された個体の適合度を削除
                del child1.fitness.values
                del child2.fitness.values

        # 変異
        for mutant in offspring[MU / 100::]:
            if random.random() < MUTPB:
                toolbox.mutate(mutant)
                del mutant.fitness.values

        # 適合度が計算されていない個体を集めて適合度を計算
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        # 次世代群をoffspringする
        pop[:] = offspring

        # すべての個体の適合度を配列にする
        fits = [ind.fitness.values[0] for ind in pop]

        # print fits

        length = len(pop)
        mean = sum(fits) / length
        sum2 = sum(x * x for x in fits)
        std = abs(sum2 / length - mean**2)**0.5  # 標準偏差

        hof.update(pop)

        print(" number of pop %s " % length)
        print(" Min %s" % min(fits))
        print(" Max %s" % max(fits))
        print(" Avg %s" % mean)
        print(" Std %s" % std)

        x = np.append(x, g)
        y = np.append(y, max(fits))
        lines.set_data(x, y)  # グラフの更新
        ax.set_xlim = (0, x.max() + 1)
        plt.pause(.01)

    print("--- end --- \n")

    bests = [ind.fitness.values for ind in hof]
    selected_items = [(i, items[i])
                      for i in tuple(hof[bests.index(max(bests))])]

    print(" Best {}".format(max(bests)))
    print(" Selected items ")
    print(selected_items)

    """ 確認用
    w_sum = 0
    v_sum = 0.0
    for i in selected_items:
        w_sum += i[1][1]
        v_sum += i[1][0]
    print w_sum
    print v_sum
    """

    plt.show()

    return pop, hof


if __name__ == '__main__':
    main()
