import random
from pickle import load
from os import listdir, remove
from Ant_with_gui import Sample
from imageio.v3 import imread
from imageio import mimsave
from matplotlib import pylab as pyl
import numpy as np
import os


def n_to_l(N, m, n):  # 序列序号转变为环境矩阵中的位置
    if N + 1 > m * n:
        exit("注意！序号超出环境设置")
    else:
        return int(N % m), N // m


def n_to_s(N, m, n):  # 序列序号转变为坐标
    if N + 1 > m * n:
        exit("注意！序号超出环境设置")
    if (N + 1) % m == 0:
        y = 0.5
    else:
        y = m - (N + 1) % m + 0.5  # 栅格中心纵坐标
    x = ((N + 1) + y - 0.5 * (m + 1)) / m  # 栅格中心横坐标
    return [x, y]


def wall(g):  # 给G封上围墙
    m = g.shape[0]
    n = g.shape[1]
    gg = np.vstack((np.ones(n, dtype=int), g, np.ones(n, dtype=int)))
    gg = np.hstack((np.ones((m + 2, 1), dtype=int), gg, np.ones((m + 2, 1), dtype=int)))  # 二者不可颠倒顺序
    return gg


def makegif(img_path, save_path, duration=None, loop=0, fps=None):  # 传入文件路径和保存路径即可创建gif
    if fps:
        duration = 1 / fps
    imgPaths = listdir(img_path)  # 读取文件目录下所有图片
    imgPaths.sort(key=lambda x: int(x[:-4]))  # 安照每个文件的先后顺序排序
    images = []
    for i in range(len(imgPaths)):
        images.append(imread(img_path + "/" + imgPaths[i]))
    # images = [imread(img_path + "/" + path) for path in imgPaths] # 储存每一帧图片
    mimsave(save_path, images, "gif", duration=duration, loop=loop)  # 生成gif动图
    # for each in imgPaths:  # 删除残留文件
    #     remove(img_path + "/" + each)
    return


def initial_robot(robot) -> Sample:
    Robot = Sample()
    Robot.Graph = robot.Graph
    Robot.S = robot.S
    Robot.E = robot.E
    Robot.MinPath = robot.MinPath  # 记录全局最短路径
    Robot.MinL = robot.MinL
    Robot.LastPath = robot.LastPath
    Robot.Mink = robot.Mink  # 最短路径的迭代次数
    Robot.Minm = robot.Minm  # 跑出最短路径的蚂蚁序号

    return Robot


def Backoff_algorithm(robot1: Sample, robot2: Sample, flag: int) -> int:  # 该算法实现了r1优先
    length = min(len(robot1.MinPath), len(robot2.MinPath))
    r2_path = robot2.MinPath.copy()  # 复制一份r2路径方便算法的实现
    if flag != 1:
        flag = 0  # 标志位 记录此次是否修改了路径
    for i in range(length - 1):
        if robot1.MinPath[i + 1] == robot2.MinPath[i] and robot1.MinPath[i] == robot2.MinPath[i + 1]:  # 相碰撞
            if i + 1 == len(robot1.MinPath):  # 当robot1下一步就是终点时
                idle_node = detect(robot1.Graph, robot1.MinPath[i], -1, robot2.MinPath[i])  # 避免r1越界
            else:
                idle_node = detect(robot1.Graph, robot1.MinPath[i], robot1.MinPath[i + 2], robot2.MinPath[i])
            if idle_node == -1:  # 当前robot2四周没有可以回避的栅格
                last = r2_path.index(robot2.MinPath[i]) - 1  # 获得当前节点的前驱节点的位置
                robot2.MinPath.insert(i + 1, r2_path[last])  # r2退回到上一步
                robot2.MinPath.insert(i + 2, robot2.MinPath[i])  # 因为r2退回后还要回到这里
            else:
                robot2.MinPath.insert(i + 1, idle_node)  # r2回避到空闲地带
                robot2.MinPath.insert(i + 2, robot2.MinPath[i])  # 因为r2回避后还要回到这里
            flag = 1  # 表示修改过路径

        if robot1.MinPath[i + 1] == robot2.MinPath[i + 1]:  # 若r1和r2的下一步是同一栅格
            robot2.MinPath.insert(i + 1, robot2.MinPath[i])  # r2原地等待
            flag = 1  # 表示修改过路径
    return flag


def detect(graph, node1: int, node11: int, node2: int) -> int:  # 若格栅旁边有空余节点 则返回节点位置 否则返回-1
    graph_ = wall(graph)
    row, col = n_to_l(node2, graph.shape[0], graph.shape[1])
    nodes = []  # node2 周围的空闲节点
    forbidden = [node1, node11, node2]  # 禁止节点
    for i in range(row, row + 3):
        for j in range(col, col + 3):
            number = graph.shape[0] * (j - 1) + i - 1  # 当前节点所对应的序号
            if graph_[i, j] == 0 and number not in forbidden:
                nodes.append(number)

    if len(nodes) == 0:
        return -1
    else:
        return random.choice(nodes)


def Multi_Algor(robots: list, flag: int) -> int:  # 传入Robots 对每个的路径重新规划
    for i in range(len(robots) - 1):
        for j in range(i + 1, len(robots)):
            flag = Backoff_algorithm(robots[i], robots[j], flag=flag)
    return flag


def draw_Multi_line(robot: Sample, index: int, Path: list, Title: str, is_figure=False):
    MM, NN = np.shape(robot.Graph)[0], np.shape(robot.Graph)[1]
    L = len(Path)
    Px = np.zeros(L)
    Py = np.zeros(L)
    if not is_figure:  # 判断是否要新建画布
        if 0 < MM <= 10 and 0 < NN <= 10:  # 设置窗口大小
            figsize = (NN * 1.3, MM * 1.3)
            pyl.figure(Title, figsize=figsize)
        elif MM <= 20 and NN <= 20:
            figsize = (NN * 0.65, MM * 0.65)
            pyl.figure(Title, figsize=figsize)
        elif MM <= 30 and NN <= 30:
            figsize = (NN * 0.43, MM * 0.43)
            pyl.figure(Title, figsize=figsize)
        elif MM > 81 or NN > 81:
            exit("暂时只支持栅格数目不超过81*81的地图环境哦")
        else:
            figure = pyl.get_current_fig_manager()
            figure.window.showMaximized()

    pyl.xlim(0, NN)
    pyl.ylim(0, MM)
    pyl.xticks(np.array(range(NN + 1))), pyl.yticks(np.array(range(MM + 1)))  # 此处是为了设置网格线的间隔
    pyl.grid(color="black")
    pyl.title(Title)
    pyl.xlabel("x")
    [Sx, Sy] = n_to_s(Path[0], MM, NN)  # 获得起始点的坐标
    [Ex, Ey] = n_to_s(Path[-1], MM, NN)  # 获得终点的坐标
    [Tx, Ty] = n_to_s(robot.E, MM, NN)  # 获得目标点的坐标
    SX = [Sx - 0.5, Sx + 0.5]
    SY = [Sy - 0.5, Sy + 0.5]
    EX = [Ex - 0.5, Ex + 0.5]
    EY = [Ey - 0.5, Ey + 0.5]
    TX = [Tx - 0.5, Tx + 0.5]
    TY = [Ty - 0.5, Ty + 0.5]
    for i in range(MM):
        for j in range(NN):
            n = j * MM + i
            [x, y] = n_to_s(n, MM, NN)
            X = [x - 0.5, x + 0.5]
            Y = [y - 0.5, y + 0.5]
            if robot.Graph[i, j] == 1:
                pyl.fill_between(X, Y[0], Y[1], facecolor="#373737", alpha=0.85)  # alpha表示不透明度
            elif robot.Graph[i, j] == 2:
                pyl.fill_between(X, Y[0], Y[1], facecolor="red")

    colors = ['red', 'lime', 'blue', 'black', 'orange', 'violet', 'g', 'tomato', 'blueviolet', 'darkviolet']
    # 标出起点和终点还有目标点
    pyl.fill_between(SX, SY[0], SY[1], facecolor=colors[index % 9])
    pyl.fill_between(EX, EY[0], EY[1], facecolor=colors[index % 9])
    pyl.fill_between(TX, TY[0], TY[1], facecolor=colors[index % 9])

    for i in range(L):  # 获得线路上各点的坐标
        [Px[i], Py[i]] = n_to_s(Path[i], MM, NN)
    for i in range(L - 1):  # 开始画线路图
        pyl.plot([Px[i], Px[i + 1]], [Py[i], Py[i + 1]], colors[index % 9])  # 画线路图


def final_draw(robots: list, save_path):
    Steps = []  # 每一个单位时间,各个机器人所处的位置
    length = max([len(robot.MinPath) for robot in robots])  # 获得所有机器人中路径长度的最大值
    for i in range(length):
        Step = []
        for robot in robots:
            if i < len(robot.MinPath):  # 防止数组越界
                Step.append(robot.MinPath[i])
            else:
                Step.append(robot.MinPath[-1])
        Steps.append(Step)

    MM = robots[0].Graph.shape[0]
    NN = robots[0].Graph.shape[1]
    colors = ['red', 'lime', 'blue', 'black', 'orange', 'violet', 'g', 'tomato', 'blueviolet', 'darkviolet']
    if not os.path.exists(save_path + "\pics"):  # pics为每次动图帧的存放位置，若不存在就创建
        os.mkdir(save_path + "\pics")
    if len(os.listdir(save_path + "\pics")) != 0:  # 若pics不为空，则删除上次的残留图片
        for file in os.listdir(save_path + "\pics"):
            os.remove(save_path + "/pics/" + file)
    for each_step in Steps:
        for i in range(len(each_step)):
            [Px, Py] = n_to_s(each_step[i], MM, NN)
            pyl.scatter(Px, Py, c=colors[i % 9])  # 画线路图
        pyl.pause(0.01)
        L = len(listdir(save_path + "/pics/"))
        pyl.savefig(save_path + "/pics/" + str(L + 1) + ".jpg")
        for each in each_step:
            [Px, Py] = n_to_s(each, MM, NN)
            pyl.scatter(Px, Py, c='white')  # 清除上一次的痕迹
    makegif(img_path=save_path + "/pics", save_path=save_path + "/Robots.gif", loop=1, fps=3)
    pyl.show()


if __name__ == '__main__':
    Robots_list = listdir('./images/Solutions')
    Robots = []  # 存放机器人变量

    for i in range(len(Robots_list)):  # 读入机器人信息
        f = open('./images/Solutions/' + Robots_list[i], 'rb')
        Robots.append(initial_robot(load(f)))
        f.close()

    #  以上 所有机器人都已存入Robots数组里
    Flag = 1  # 是否已经对所有机器人完成规划
    while Flag > 0:
        # print('帅')
        Flag = Multi_Algor(Robots, flag=0)

    for i in range(len(Robots)):
        draw_Multi_line(Robots[i], index=i, Path=Robots[i].MinPath, Title='MultiRobots')
    final_draw(Robots, save_path='./Robots')
