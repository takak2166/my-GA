# -*- coding: utf-8 -*-
import random
import numpy

from deap import algorithms
from deap import base
from deap import creator
from deap import tools

import matplotlib.pyplot as plt
import numpy as np

#適合度クラスを作成
creator.create("Fitness", base.Fitness, weights=(-1.0, 1.0))
creator.create("Individual", set, fitness=creator.Fitness)

#アイテムの重さと体積をランダムに決める
NBR_ITEMS = 30
IND_INIT_SIZE = 10
MAX_ITEM = 50
MAX_WEIGHT = 100

items = {}

for i in range(NBR_ITEMS):
    items[i] = (random.randint(1, 10), random.uniform(0, 100))

toolbox = base.Toolbox()
#Attributeを生成する関数を定義
toolbox.register("attr_item", random.randrange, NBR_ITEMS)
#個体を生成する関数を定義(Individualクラスでattr_itemの要素をいくつか持つ)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_item, IND_INIT_SIZE)
#集団を生成する関数を定義
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

#評価関数
def evalknapsack(individual):
    weight = 0.0
    value = 0.0
    for item in individual:
        weight += items[item][0]
        value += items[item][1]
    if len(individual) > MAX_ITEM or weight > MAX_WEIGHT:
        return 10000, 0
    return weight, value

def cxSet(ind1, ind2):
    """交叉を適用する. 1番目の子は二つのセットの交叉で
    2番目の子は違う二つのセットの交叉.
    """
    temp = set(ind1)
    ind1 &= ind2
    ind2 ^= temp
    return ind1, ind2

def mutSet(individual):
    """突然変異・挿入"""
    if random.random() < 0.5:
        if len(individual) > 0: #いっぱいになったら取り出せない
            individual.remove(random.choice(sorted(tuple(individual))))
    else:
        individual.add(random.randrange(NBR_ITEMS))
    return individual,

#評価関数を登録
toolbox.register("evaluate", evalknapsack)
#交叉関数を登録
toolbox.register("mate", cxSet)
#変異関数を登録
toolbox.register("mutate", mutSet)
#選択関数を登録
toolbox.register("select", tools.selNSGA2)

def main():
    NGEN = 50
    MU = 50
    LAMBDA = 10000
    CXPB = 0.7
    MUTPB = 0.2

    pop = toolbox.population(n=MU)
    hof = tools.ParetoFront()
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean, axis=0)
    stats.register("std", numpy.std, axis=0)
    stats.register("min", numpy.min, axis=0)
    stats.register("max", numpy.max, axis=0)

    algorithms.eaMuPlusLambda(pop, toolbox, MU, LAMBDA, CXPB, MUTPB, NGEN, stats,
                                halloffame=hof)

    return pop, stats, hof

if __name__ == '__main__':
    main()
