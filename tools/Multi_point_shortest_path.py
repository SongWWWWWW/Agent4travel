import numpy as np
from itertools import permutations

n = 4
distance_matrix = np.zeros((n, n))

distances = {
    (1, 2): 10,
    (1, 3): 3,
    (1, 4): 4,
    (2, 3): 5,
    (2, 4): 6,
    (3, 4): 2
}

for (i, j), dist in distances.items():
    distance_matrix[i - 1, j - 1] = dist
    distance_matrix[j - 1, i - 1] = dist


# 生成所有可能的路径（包括起点和终点）
def generate_paths(n):
    return permutations(range(1, n))


# 计算路径的总距离
def calculate_path_distance(path, distance_matrix):
    total_distance = 0
    for i in range(len(path)):
        total_distance += distance_matrix[path[i - 1], path[i]]
    # 加上从最后一个城市返回到起点的距离
    total_distance += distance_matrix[path[-1], 0]
    return total_distance


# 找到最短路径
def find_shortest_path(distance_matrix):
    n = distance_matrix.shape[0]
    shortest_distance = float('inf')
    shortest_path = None

    for path in generate_paths(n):
        path_distance = calculate_path_distance(path, distance_matrix)
        if path_distance < shortest_distance:
            shortest_distance = path_distance
            shortest_path = (0,) + path + (0,)

    return shortest_path, shortest_distance


# 执行寻找最短路径的函数
shortest_path, shortest_distance = find_shortest_path(distance_matrix)

# 输出结果
print("最短路径为：", shortest_path)
print("最短路径的总距离为：", shortest_distance)
