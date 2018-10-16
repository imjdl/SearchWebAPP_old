#!/usr/bin/env python3
# coding=UTF-8
__author__ = "Elliot King"

__doc__ = """
TSP 旅行商算法
回朔法
"""
n = 5  # 节点数

# 5 个节点
# a = "a"
# b = "b"
# c = "c"
# d = "d"
# e = "e"

a, b, c, d, e = range(5)

# 定义各城市之间的路程
graph = [
    {b: 7, c: 6, d: 1, e: 3},
    {a: 7, c: 3, d: 7, e: 8},
    {a: 6, b: 3, d: 12, e: 11},
    {a: 1, b: 7, c: 12, e: 2},
    {a: 3, b: 68, c: 11, d: 2}
]

solution = [0] * (n + 1)  # 一个解 n+1 应为最后要回到原点

solution_list = []  # 一组解

best_sol = [0] * (n + 1)  # 一个最优解

min_cost = 0  # 最小代价


def tsp(k):
    global n, graph, solution, solution_list, best_sol, min_cost
    if k > n:
        cost = sum([graph[node1][node2] for node1, node2 in zip(solution[:-1], solution[1:])])
        if min_cost == 0 or cost < min_cost:
            best_sol = solution[:]
            min_cost = cost
    else:
        print("k=", k, "\t\t", graph[solution[k - 1]])
        for node in graph[solution[k - 1]]:
            solution[k] = node
            if not conflick(k):
                tsp(k + 1)


def conflick(k):
    """
    解决以下问题:
    1、该节点是否被访问过
    2、访问节点数。。。
    3、前面部分解的旅费之和超出已经找到的最小总旅费
    """
    global n, graph, solution, best_sol, min_cost
    if k < n and solution[k] in solution[:k]:
        # 节点以访问过
        return True

    if k == n and solution[k] != solution[0]:
        return True
    cost = sum([graph[node1][node2] for node1, node2 in zip(solution[:k], solution[1:k + 1])])
    if 0 < min_cost < cost:
        return True
    return False


solution[0] = a
tsp(0)
print(best_sol)
print(min_cost)

# if __name__ == '__main__':
#     main()
