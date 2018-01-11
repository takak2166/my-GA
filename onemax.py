# -*- coding: utf-8 -*-
import random

from deap import base
from deap import creator
from deap import tools

import matplotlib.pyplot as plt
import numpy as np

#適合度クラスを作成
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
#Attributeを生成する関数を定義(0,1をランダムに選ぶ)
toolbox.register("attr_bool", random.randint, 0, 1)
#個体を生成する関数を定義(Individualクラスでattr_boolの値を100個持つ)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, 100)
#集団を生成する関数を定義(個体を持つlist)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

#評価関数
def evalOneMax(individual):
    return sum(individual),

#評価関数を登録
toolbox.register("evaluate", evalOneMax)
#交叉巻数を定義(2点交叉)
toolbox.register("mate", tools.cxTwoPoint)
#変異関数を定義(ビット反転, 変異確率が5%？)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
#選択関数を定義(トーナメント選択, tournsizeはトーナメントの数？)
toolbox.register("select", tools.selTournament, tournsize=3)

if __name__ == '__main__': # 直接実行されたらモジュール名が__main__になる
    #初期集団を生成
    pop = toolbox.population(n=300)
    CXPB, MUTPB, NGEN = 0.5, 0.2, 40 # 交叉確率, 突然変異確率, 進化計算のループ回数

    print("進化開始")


    # 初期集団の個体を評価する
    fitnesses = list(map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses): # zipは複数変数の同時ループ
        # 適合性をセットする
        ind.fitness.values = fit

    print(" %i の個体を評価" %len(pop))

    #ここで1回plotする

    fig, ax = plt.subplots(1, 1)
    x = np.arange(0)
    y = np.array([])
    ax.set_ylim(0, 100)
    ax.set_xlim(0, 40)
    lines, = ax.plot(x, y)

    # 進化計算開始
    for g in range(NGEN): # NGEN回ループ
        print("-- %i世代 --" %g)

        ##########
        # 選択
        ##########

        # 次世代の個体群を選択
        offspring = toolbox.select(pop, len(pop))
        # 個体群のクローンを生成
        offspring = list(map(toolbox.clone, offspring))

        #選択した個体群に交叉と突然変異を適応する

        #########
        # 交叉
        #########
        #偶数番目と奇数番目の個体を取り出して交叉
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < CXPB :
                toolbox.mate(child1, child2)
                # 交叉された固体の適合度を削除
                del child1.fitness.values
                del child2.fitness.values

        ########
        # 変異
        ########
        for mutant in offspring:
            if random.random() < MUTPB:
                toolbox.mutate(mutant)
                del mutant.fitness.values

        # 適合度が計算されていない個体を集めて適合度を計算
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        print(" %iの個体を評価" %len(invalid_ind))

        # 次世代群をoffspringする
        pop[:] = offspring

        # すべての個体の適合度を配列にする
        fits = [ind.fitness.values[0] for ind in pop]

        length = len(pop)
        mean = sum(fits) / length
        sum2 = sum(x*x for x in fits)
        std = abs(sum2 / length - mean**2)**0.5 # 標準偏差

        print(" Min %s" %min(fits))
        print(" Max %s" %max(fits))
        print(" Avg %s" %mean)
        print(" Std %s" %std)

        x = np.append(x, g)
        y = np.append(y, max(fits))
        lines.set_data(x, y) #グラフの更新
        plt.pause(0.1)

    print("-- 進化終了 --")

    best_ind = tools.selBest(pop, 1)[0]
    print("最も優れていた固体: %s, %s" %(best_ind, best_ind.fitness.values))
