import os.path
from time import perf_counter
from os import listdir, remove
from pickle import dump, load
from imageio.v3 import imread
from imageio import mimsave
from matplotlib import pylab as pyl
from PyQt5.QtWidgets import QProgressDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from matplotlib import use

import numpy as np

gif_busy = False  # 必要的全局变量
pyl.rcParams['font.sans-serif'] = ['Kaitt', 'SimHei']  # 使画图正常显示中文
pyl.rcParams['axes.unicode_minus'] = False  # 使画图正常显示负号


# 创建一个以g为环境的对象
class Sample(object):
    def __init__(self, g=np.matrix(np.zeros((3, 3))), s=-1, e=-1):
        self.Graph = g
        self.S = s
        self.E = e
        self.MinPath = []  # 记录全局最短路径
        self.MinL = []
        self.LastPath = []
        self.Mink = 0  # 最短路径的迭代次数
        self.Minm = 0  # 跑出最短路径的蚂蚁序号

    def draw_en(self, name, save_path, if_num=False):  # 定义画出对象环境的方法
        mm, nn = self.Graph.shape[0], self.Graph.shape[1]
        if 0 < mm <= 10 and 0 < nn <= 10:  # 设置窗口大小
            figsize = (nn * 1.3, mm * 1.3)
            pyl.figure(name, figsize=figsize)
        elif mm <= 20 and nn <= 20:
            figsize = (nn * 0.65, mm * 0.65)
            pyl.figure(name, figsize=figsize)
        elif mm <= 30 and nn <= 30:
            figsize = (nn * 0.43, mm * 0.43)
            pyl.figure(name, figsize=figsize)
        elif mm > 81 or nn > 81:
            exit("暂时只支持栅格数目不超过81*81的地图环境哦")
        else:
            figure = pyl.get_current_fig_manager()
            figure.window.showMaximized()

        pyl.xlim(0, nn)
        pyl.ylim(0, mm)
        pyl.xticks(np.array(range(nn + 1))), pyl.yticks(np.array(range(mm + 1)))  # 此处是为了设置网格线的间隔
        pyl.grid(color="black")
        pyl.title(name)
        pyl.xlabel("x")
        [sx, sy] = n_to_s(self.S, mm, nn)  # 获得起始点的坐标
        [ex, ey] = n_to_s(self.E, mm, nn)  # 获得终点的坐标
        SX = [sx - 0.5, sx + 0.5]
        SY = [sy - 0.5, sy + 0.5]
        EX = [ex - 0.5, ex + 0.5]
        EY = [ey - 0.5, ey + 0.5]

        for i in range(mm):
            for j in range(nn):
                n = j * mm + i
                [x, y] = n_to_s(n, mm, nn)
                X = [x - 0.5, x + 0.5]
                Y = [y - 0.5, y + 0.5]
                if self.Graph[i, j] == 1:
                    pyl.fill_between(X, Y[0], Y[1], facecolor="#373737", alpha=0.85)  # alpha表示不透明度
                elif self.Graph[i, j] == 2:
                    pyl.fill_between(X, Y[0], Y[1], facecolor="#ee0000")  # 阿绫红
                if if_num:  # 是否要在格子上标出序号
                    if self.Graph[i, j] == 0 and n < 10:
                        pyl.text(x - 0.2, y - 0.2, str(n), color="#373737", fontsize="small", alpha=0.7)  # 标出指定位置的序号
                    elif self.Graph[i, j] == 0 and n < 100:
                        pyl.text(x - 0.28, y - 0.2, str(n), color="#373737", fontsize="small", alpha=0.7)  # 标出指定位置的序号
                    elif self.Graph[i, j] == 0 and n < 1000:
                        pyl.text(x - 0.32, y - 0.2, str(n), color="#373737", fontsize="x-small", alpha=0.7)  # 标出指定位置的序号
                    elif self.Graph[i, j] == 0:
                        pyl.text(x - 0.32, y - 0.2, str(n), color="#373737", fontsize="xx-small",
                                 alpha=0.7)  # 标出指定位置的序号

        if self.S != -1:  # 起点为-1表示不标出起点
            pyl.fill_between(SX, SY[0], SY[1], facecolor="#99ffff")  # 言和绿
        if self.E != -1:  # 终点为-1 表示不标出终点
            pyl.fill_between(EX, EY[0], EY[1], facecolor="#66ccff")  # 天依蓝
        pyl.savefig(save_path + '\\' + name + ".png")
        pyl.show()
        # pyl.close()

    def draw_path(self, Path, Title, save_path, is_figure=False, is_gif=False, continuous=False):  # 定义画出路径的方法
        MM, NN = np.shape(self.Graph)[0], np.shape(self.Graph)[1]
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
        [Tx, Ty] = n_to_s(self.E, MM, NN)  # 获得目标点的坐标
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
                if self.Graph[i, j] == 1:
                    pyl.fill_between(X, Y[0], Y[1], facecolor="#373737", alpha=0.85)  # alpha表示不透明度
                elif self.Graph[i, j] == 2:
                    pyl.fill_between(X, Y[0], Y[1], facecolor="red")

        # 标出起点和终点还有目标点
        pyl.fill_between(SX, SY[0], SY[1], facecolor="#99ffff")  # 言和绿
        pyl.fill_between(EX, EY[0], EY[1], facecolor="#66ccff")  # 天依蓝
        pyl.fill_between(TX, TY[0], TY[1], facecolor="#66ffcc")  # 初音绿

        for i in range(L):  # 获得线路上各点的坐标
            [Px[i], Py[i]] = n_to_s(Path[i], MM, NN)

        d, Turn = 0, 0
        pyl.ion()  # 打开交互模式

        if is_gif:  # 是否保存gif图
            if not os.path.exists(save_path + "\pics"):  # pics为每次动图帧的存放位置，若不存在就创建
                os.mkdir(save_path + "\pics")
            for i in range(L - 1):  # 开始画线路图
                vect = [Px[i + 1] - Px[i], Py[i + 1] - Py[i]]
                d = d + (vect[0] ** 2 + vect[1] ** 2) ** 0.5
                if i != 0:
                    if vect[0] != (Px[i] - Px[i - 1]) or vect[1] != (Py[i] - Py[i - 1]):  # 若此次发生了转向
                        Turn = Turn + 1
                pyl.plot([Px[i], Px[i + 1]], [Py[i], Py[i + 1]], 'b')  # 画线路图
                pyl.title(Title + ' Length of Pathing:' + str(round(d, 2)))
                pyl.xlabel('x  Number of TURN:' + str(Turn))
                pyl.pause(0.001)
                length = len(listdir(save_path + "/pics/"))
                pyl.savefig(save_path + "/pics/" + str(length + 1) + ".jpg")
            if not continuous:  # 若想要多次连续的图片,则暂时先不将pic中的帧制作成动图
                # 保存当代蚂蚁的gif图
                makegif(save_path + "/pics", save_path + "/" + Title + " th.gif", loop=1, fps=24)
        else:
            for i in range(L - 1):  # 开始画线路图
                vect = [Px[i + 1] - Px[i], Py[i + 1] - Py[i]]
                d = d + (vect[0] ** 2 + vect[1] ** 2) ** 0.5
                if i != 0:
                    if vect[0] != (Px[i] - Px[i - 1]) or vect[1] != (Py[i] - Py[i - 1]):  # 若此次发生了转向
                        Turn = Turn + 1
                pyl.plot([Px[i], Px[i + 1]], [Py[i], Py[i + 1]], 'b')  # 画线路图
                pyl.title(Title + ' Length of Pathing:' + str(round(d, 2)))
                pyl.xlabel('x  Number of TURN:' + str(Turn))
                pyl.pause(0.01)

        pyl.ioff()  # 关闭交互模式

    def save_drawline(self, save_path, is_gif=False):  # 定义画出收敛曲线的方法
        pyl.figure("Convergence curve", figsize=(10, 10))
        pyl.title("Convergence curve")
        pyl.xlabel("Number of iterations")
        pyl.ylabel("Minimum path length per generation")
        pyl.ion()  # 打开交互模式
        if is_gif:
            if not os.path.exists(save_path + "\pics"):  # pics为每次动图帧的存放位置，若不存在就创建
                os.mkdir(save_path + "\pics")
            for i in range(len(self.MinL) - 1):
                pyl.plot([i + 1, i + 2], [self.MinL[i], self.MinL[i + 1]], 'b')
                pyl.pause(0.01)
                pyl.savefig(save_path + "/pics/" + str(i + 1) + ".jpg")
            makegif(save_path + "/pics", save_path + "/Convergence curve.gif", loop=1, fps=24)
        else:
            for i in range(len(self.MinL) - 1):
                pyl.plot([i + 1, i + 2], [self.MinL[i], self.MinL[i + 1]], 'b')
                pyl.pause(0.001)
        pyl.savefig(save_path + "/Convergence curve.jpg")
        pyl.ioff()  # 关闭交互模式


# 在这里设置参数
class Parameter(object):
    def __init__(self):
        # 参数设置
        self.Alpha = 1.5  # Alpha表征信息素重要程度
        self.Beta = 2  # Beta表征启发式因子重要程度
        self.Gama = 0  # Gama表征路径转向角度的重要程度 障碍点较少时 建议调小一点
        self.Rho = 0.03  # Rho信息素蒸发系数
        self.Q = 50  # Q信息素增加强度系数
        self.Ra = 0.1  # 蚂蚁理性程度(越大表示越容易选择概率高的目标点)
        self.Rate = 0.3  # 当前节点到下一节的距离在启发式因子中所占权重
        self.Deadcell = True  # 设置是否使用无效点算法
        self.if_drawout = False  # 设置是否画出中间过程
        self.is_gif = False  # 设置是否将结果保存为gif

    def save(self):
        f = open('./parameter.pkl', 'wb')
        # 保存参数文件
        dump(self, f)
        f.close()

    def load(self):
        f = open('./parameter.pkl', 'rb')
        # 加载参数文件
        pa = load(f)
        self.Alpha = pa.Alpha
        self.Beta = pa.Beta
        self.Gama = pa.Gama
        self.Rho = pa.Rho
        self.Q = pa.Q
        self.Ra = pa.Ra
        self.Rate = pa.Rate
        self.Deadcell = pa.Deadcell
        self.if_drawout = pa.if_drawout
        self.is_gif = pa.is_gif
        f.close()


# 存放路径
class Save_path(object):
    def __init__(self):
        self.en_save_path = './graphs'
        self.result_save_path = './images'

    def save(self):
        f = open('./save_path.pkl', 'wb')
        # 保存储存路径文件
        dump(self, f)
        f.close()

    def load(self):
        f = open('./save_path.pkl', 'rb')
        # 加载储存路径文件
        path = load(f)
        self.en_save_path = path.en_save_path
        self.result_save_path = path.result_save_path
        f.close()


# 进度条对话框
class ProgressDialog(QProgressDialog):
    def __init__(self, parent=None, *args, **kwargs):  # 初始化方法
        super().__init__(parent, *args, **kwargs)  # 优先调用父方法
        self.setWindowTitle("Ant Searching -- Author : GS and XiaoYang")  # 设置窗口标题
        self.setWindowIcon(QIcon('ICON/icon.jpg'))  # 设置窗口图标
        self.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowMinimizeButtonHint)  # 设置只显示最小化按钮
        self.setWindowModality(Qt.WindowModal)  # 设为模态 这是必须的
        self.resize(600, 100)
        self.setMinimumDuration(0)  # 打开dialog的等待时间为0
        self.setAutoClose(False)  # 设置进度条结束后不要自动关闭
        self.setAutoReset(False)  # 设置进度条结束后不要自动重置
        self.show()


def n_to_s(N, m, n):  # 序列序号转变为坐标
    if N + 1 > m * n:
        exit("注意！序号超出环境设置")
    if (N + 1) % m == 0:
        y = 0.5
    else:
        y = m - (N + 1) % m + 0.5  # 栅格中心纵坐标
    x = ((N + 1) + y - 0.5 * (m + 1)) / m  # 栅格中心横坐标
    return [x, y]


def n_to_l(N, m, n):  # 序列序号转变为环境矩阵中的位置
    if N + 1 > m * n:
        exit("注意！序号超出环境设置")
    else:
        return int(N % m), N // m


def runif(sample):
    MM, NN = sample.Graph.shape[0], sample.Graph.shape[1]
    [Sx, Sy] = n_to_l(sample.S, MM, NN)  # 获得起始点在矩阵中的位置
    [Tx, Ty] = n_to_l(sample.E, MM, NN)  # 获得目标点在矩阵中的位置

    if sample.Graph[Tx, Ty] == 1:
        exit("目标点设置在障碍点上了！")
    elif sample.Graph[Sx, Sy] == 1:
        exit("起始点设置在障碍点上了！")
    return


def angle(v1, v2):  # 计算两个向量之间夹角的余弦值
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))


def wall(g):  # 给G封上围墙
    m = g.shape[0]
    n = g.shape[1]
    gg = np.vstack((np.ones(n, dtype=int), g, np.ones(n, dtype=int)))
    gg = np.hstack((np.ones((m + 2, 1), dtype=int), gg, np.ones((m + 2, 1), dtype=int)))  # 二者不可颠倒顺序
    return gg


def distant(g):  # 计算邻接矩阵
    # D(i,j)表示G中第i个元素(按列数)离G中第j(按列数)个元素的距离(0表示一步内不可到达 八向行动)
    mm, nn = g.shape[0], g.shape[1]
    D = (-1) * np.matrix(np.ones((mm * nn, mm * nn)))
    g = wall(g)  # 给G封上围墙
    for i in range(1, mm + 1):
        for j in range(1, nn + 1):
            if g[i, j] == 0:
                [row, col] = np.where(g[i - 1:i + 2, j - 1:j + 2] == 0)
                for k in range(len(row)):
                    x, y = row[k] + i - 1, col[k] + j - 1  # (x,y)表示在G(有围墙)中的坐标(目标节点)
                    xx, yy = x - 1, y - 1  # (xx,yy)表示在G(无围墙)中的坐标
                    ii, jj = i - 1, j - 1  # (ii,jj)表示在G(无围墙)中的坐标(当前节点)
                    d = ((xx - ii) ** 2 + (yy - jj) ** 2) ** 0.5  # 当前节点与目标节点的距离
                    px, py = jj * mm + ii, yy * mm + xx  # (px,py)表示对应的D中的坐标
                    p = row[k] + col[k] * 3
                    # 判断目标结点和当前节点的相对位置
                    if p == 0:
                        if g[x + 1, y] == 0 or g[x, y + 1] == 0:  # 只有当两边没有阻碍时 才表示可以前行
                            D[px, py] = d  # 左上
                    elif p == 2:
                        if g[x - 1, y] == 0 or g[x, y + 1] == 0:
                            D[px, py] = d  # 左下
                    elif p == 6:
                        if g[x, y - 1] == 0 or g[x + 1, y] == 0:
                            D[px, py] = d  # 右上
                    elif p == 8:
                        if g[x, y - 1] == 0 or g[x - 1, y] == 0:
                            D[px, py] = d  # 右下
                    else:
                        D[px, py] = d
    return D


def dead_cell(gg, D, W, mm, nn):  # 更新G和D 排除无效节点
    ss = 0
    ddots = []
    [I, J] = n_to_l(W, mm, nn)
    I, J = I + 1, J + 1  # 获得W位置在gg中的坐标
    dots = [[I - 1, J], [I + 1, J], [I, J - 1], [I, J + 1]]  # 获得W位置周围四个点在GG中的坐标 （不可改变顺序）
    for i in range(4):
        if gg[dots[i][0], dots[i][1]] > 0:  # 若该位置存在障碍物
            ss = ss + 1
            ddots.append(i)  # 记下障碍物的位置
    if ss == 3:  # 若该节点周围有三个障碍物体 则必是无效节点
        D[W, :], D[:, W] = -1, -1  # 更新D矩阵
        gg[I, J] = 2  # 将当前节点看做有障碍物并标红
    elif ss == 2:  # 若该节点周围有两个障碍物 则有可能是无效节点
        dd = [dots[ddots[1]][0] - dots[ddots[0]][0], dots[ddots[1]][1] - dots[ddots[0]][1]]
        if np.linalg.norm(dd) != 2:  # 两障碍物之间距离不等于2 则有可能是无效节点
            d_ = dd[1] / dd[0]  # 向量纵横坐标相除
            if d_ == 1:
                if gg[I + 1, J + 1] > 0 or gg[I - 1, J - 1] > 0:  # 此时有可能满足无效节点的条件
                    if dd[0] == 1 and gg[I + 1, J - 1] == 0:  # 此时该节点为无效节点
                        D[W, :], D[:, W] = -1, -1  # 更新D矩阵
                        gg[I, J] = 2  # 将当前节点看做有障碍物并标红
                    elif dd[0] == -1 and gg[I - 1, J + 1] == 0:  # 此时该节点为无效节点
                        D[W, :], D[:, W] = -1, -1  # 更新D矩阵
                        gg[I, J] = 2  # 将当前节点看做有障碍物并标红
            elif d_ == -1:
                if gg[I - 1, J + 1] > 0 or gg[I + 1, J - 1] > 0:  # 此时有可能满足无效节点的条件
                    if dd[0] == 1 and gg[I + 1, J + 1] == 0:  # 此时该节点为无效节点
                        D[W, :], D[:, W] = -1, -1  # 更新D矩阵
                        gg[I, J] = 2  # 将当前节点看做有障碍物并标红
                    elif dd[0] == -1 and gg[I - 1, J - 1] == 0:  # 此时该节点为无效节点
                        D[W, :], D[:, W] = -1, -1  # 更新D矩阵
                        gg[I, J] = 2  # 将当前节点看做有障碍物并标红
    return [gg, D]


def aca(sample, save_path, para, K=64, M=80):
    mm = sample.Graph.shape[0]
    nn = sample.Graph.shape[1]

    gg = wall(sample.Graph)  # 给G封上围墙
    D = distant(sample.Graph)  # 计算邻接矩阵
    # result = sample  # 获得关于G的对象
    # -----------计算起始点&终止点-------------------
    N = mm * nn  # 节点总个数
    [Ex, Ey] = n_to_s(sample.E, mm, nn)
    # -----------参数设置-------------------
    b = 1 - para.Rate  # 节点到终止点的距离在启发式因子中所占权重
    minkl = float("inf")  # 初始化最短路径长度为无穷大
    Tau = 8 * np.matrix(np.ones((N, N)))  # 初始信息素分布Tau(i, j)表示G中第i个节点和第j个节点之间的信息素
    ROUTES = np.empty((K, M), dtype=object)  # 用细胞结构存储每一代的每一只蚂蚁的爬行路线
    S_Route = np.empty((K, M), dtype=object)  # 记录觅食成功的路径
    PL = np.zeros((K, M))  # 用矩阵存储每一代成功觅食的每一只蚂蚁的爬行路线长度
    PN = np.zeros((K, M))  # 用矩阵存储每一代成功觅食的每一只蚂蚁的爬行转向次数
    is_figure = 0
    # 进度条对话框

    process = ProgressDialog()
    process.setRange(0, K * M)
    process.setValue(0)
    # -----------开始循环-----------
    for k in range(K):
        for m in range(M):
            # 状态初始化
            W = sample.S  # 当前节点初始化为起始点
            Path = [sample.S]  # 爬行路径初始化
            vect = []  # 初始化转向向量
            PLkm = 0  # 爬行路径长度初始化
            PNkm = 0  # 爬行路径转向次数初始化
            DD = D.copy()  # 邻接矩阵初始化
            ii = -1  # 初始化运动步数
            # 初始化第一步可前往的节点
            DW = DD[W, :]
            LJD = np.where(DW > 0)[1]  # 找到G中第W个位置的周围可行进的点的序号
            Len_LJD = len(LJD)  # 可选节点个数
            # 蚂蚁开始觅食直到陷入死胡同或者结束觅食(while)
            sample.Graph = gg[1:mm + 1, 1:nn + 1].copy()  # 开始觅食前先把前一次的gg矩阵保存下来方便画图
            while W != sample.E and Len_LJD >= 1:  # 即可选节点个数不为0或者W不等于E(觅食结束)
                Hn = np.zeros(Len_LJD)  # 各参数初始化
                Gn = np.zeros(Len_LJD)
                Eta = np.zeros(Len_LJD)
                Theta = np.zeros(Len_LJD)
                PP = np.zeros(Len_LJD)  # 概率转移矩阵
                Pcum = np.zeros(Len_LJD)
                ii = ii + 1  # 已运动步数更新
                [Wx, Wy] = n_to_s(W, mm, nn)  # 序列序号转变为空间坐标
                # 计算概率转移矩阵
                if sample.E in LJD:
                    PP[np.where(LJD == sample.E)] = 1  # 若下一个可前进节点中有终点则前往终点的概率为1
                else:  # 若下一个可前进节点中没有终点 才进行参数的计算
                    # 计算启发式因子矩阵
                    for i in range(Len_LJD):
                        [ix, iy] = n_to_s(LJD[i], mm, nn)
                        Hn[i] = ((ix - Wx) ** 2 + (iy - Wy) ** 2) ** 0.5  # 下一个节点到当前节点的距离
                        Gn[i] = ((ix - Ex) ** 2 + (iy - Ey) ** 2) ** 0.5  # 节点到终止点的距离
                        aa = [ix - Wx, iy - Wy]
                        bb = [Ex - Wx, Ey - Wy]  # cos(ab) / | a | | b |
                        Theta[i] = angle(aa, bb) + 2  # 计算目标点 当前节点 和最终节点之间的夹角
                        Eta[i] = 1 / (para.Rate * Hn[i] + b * Gn[i])  # 节点的启发因子η
                        Pi = (Tau[W, LJD[i]] ** para.Alpha) * ((Eta[i]) ** para.Beta) * (Theta[i] ** para.Gama)
                        if Pi == float("inf"):
                            PP = np.zeors(Len_LJD)
                            PP[i] = 1
                            break
                        else:
                            PP[i] = Pi
                    PP = PP / np.sum(PP)  # 建立概率转移矩阵
                # A*算法选择下一步怎么走
                if np.random.rand() <= para.Ra:
                    Max = np.where(PP == max(PP))[0]  # PP中概率最大的下标
                    to_visit = LJD[Max[0]]  # 此处加下标是为了防止若有相同最大的概率
                else:  # 转轮赌法
                    Pcum[0] = PP[0]
                    for i in range(1, Len_LJD):
                        Pcum[i] = Pcum[i - 1] + PP[i]
                    select = np.where(Pcum >= np.random.rand())[0]  # 找到比(0,1)之间随机数大的Pcum元素位置
                    to_visit = LJD[select[0]]  # 哪个概率大就有可能用哪个
                # 路径更新
                Path.append(to_visit)  # 路径增加
                PLkm = round(PLkm + DD[W, to_visit], 2)  # 路径长度增加
                [Vx, Vy] = n_to_s(to_visit, mm, nn)  # 下一个目标点的坐标
                vect.append([Vx - Wx, Vy - Wy])  # 运动向量更新
                ANG = angle([Vx - Wx, Vy - Wy], vect[ii - 1])
                if W != sample.S and (ANG == 1 or ANG == -1):
                    PNkm = PNkm + 1
                # 更新G_矩阵和DD矩阵 防止走走过的路
                DD[W, :], DD[:, W] = -1, -1
                W = to_visit  # 蚂蚁移到下一个节点
                # 求下一步可前往的节点
                DW = DD[W, :]  # 获得G中第W个位置到其他所有点的距离
                LJD = np.where(DW > 0)[1]
                Len_LJD = len(LJD)  # 可选节点的个数
                if para.Deadcell:  # 判断是否要使用死点算法
                    if Len_LJD <= 3 and W != sample.E:  # 若目标节点周围可选节点数量小于等于3个 则可能落入无效节点
                        [gg, D] = dead_cell(gg, D, W, mm, nn)  # 更新gg和D 排除无效节点
            # 第m只蚂蚁觅食结束 (while结束)
            # 画下第m只蚂蚁的寻路图
            if para.if_drawout:
                if m <= 1 and 0.5 * np.log2(k + 1) % 1 == 0:  # 只画前4^k代前m+1只蚂蚁
                    Title = 'Gen ' + str(k + 1) + 'th  The ' + str(m + 1) + 'th Ant Searching...  '
                    sample.draw_path(Path, Title, save_path=save_path + "/Gen", is_figure=is_figure, is_gif=para.is_gif,
                                     continuous=True)
                    pyl.clf()
                    is_figure = 1

            # 记下每一代每一只蚂蚁的觅食路线和路线长度
            ROUTES[k, m] = Path  # 将当前蚂蚁的路径储存在ROUTES里
            if Path[-1] == sample.E:  # 若当前蚂蚁觅食成功
                PL[k, m] = PLkm  # 路径长度
                PN[k, m] = PNkm  # 爬行路径历史转向次数
                S_Route[k, m] = Path  # 蚂蚁觅食成功的路径
                if PLkm < minkl:  # 若此次觅食路径长度小于最小长度
                    sample.Mink, sample.Minm = k, m
                    minkl = PLkm  # 则更新全局最优解最短路径长度并记录迭代次数和蚂蚁序号
                    sample.MinPath = Path
            if process.wasCanceled():  # 选择取消则跳出循环
                return sample
            process.setLabelText("第 " + str(k + 1) + " 代第 " + str(m + 1) + " 只蚂蚁觅食完成")
            process.setValue(process.value() + 1)
        # M只蚂蚁全部觅食结束(第二个for循环结束)

        # 更新信息素
        # 正常信息素更新
        Delta_Tau = np.matrix(np.zeros((N, N)))  # 更新量初始化
        S_PL = np.where(PL[k, :] > 0)[0]  # 获得当代第S_L只成功觅食的蚂蚁序号
        for m in S_PL:
            ROUTE = ROUTES[k, m]  # 获得那只蚂蚁的觅食路径
            PL_km = PL[k, m]  # 获得那只蚂蚁的觅食路径长度
            TS = len(ROUTE) - 1  # 跳数
            for s in range(TS):
                x, y = ROUTE[s], ROUTE[s + 1]
                Delta_Tau[x, y] = 1 / PL_km
        if len(sample.MinPath) != 0:
            MTS = len(sample.MinPath) - 1  # 最短路径跳数
            for s in range(MTS):
                mx, my = sample.MinPath[s], sample.MinPath[s + 1]
                Delta_Tau[mx, my] = Delta_Tau[mx, my] + para.Q / minkl
        Tau = (1 - para.Rho) * Tau + Delta_Tau
        # print("  第 " + str(k + 1) + " 代信息素更新完成 ", end="")

    # K次迭代结束
    pyl.close()
    if not os.path.exists(save_path + "/Gen/pics"):  # pics为每次动图帧的存放位置，若不存在就创建
        os.mkdir(save_path + "/Gen/pics")
    if len(listdir(save_path + "/Gen/pics")) != 0:  # 此处是为了应对drawout= False 的场景
        if para.is_gif:  # 是否保存gif图
            makegif(save_path + "/Gen/pics", save_path + "/Gen/" + "Process.gif", loop=1, fps=24)

    for i in range(PL.shape[0]):  # 获得每一代的最短路径长度
        if len(np.where(PL[i] > 0)[0]) > 0:
            sample.MinL.append(min(PL[i][np.where(PL[i] > 0)]))
        else:
            sample.MinL.append(None)
    if len(np.where(PL[-1, :] == sample.MinL[-1])[0]) != 0:  # 若至少有一次找到了通路
        last = np.where(PL[-1, :] == sample.MinL[-1])[0][-1]  # 获得最后一代的最短路径长度和蚂蚁只数
        sample.LastPath = ROUTES[-1, last]  # 获得最后一代的最短路径
    return sample


def makegif(img_path, save_path, duration=None, loop=0, fps=None):  # 传入文件路径和保存路径即可创建gif
    if fps:
        duration = 1 / fps
    imgPaths = listdir(img_path)  # 读取文件目录下所有图片
    imgPaths.sort(key=lambda x: int(x[:-4]))  # 安照每个文件的先后顺序排序
    images = []
    process = ProgressDialog()  # 展示进度条
    process.setCancelButton(None)  # 禁用取消按钮 即不能中断操作
    process.setRange(0, len(imgPaths))
    process.setLabelText("正在保存gif到" + save_path)
    for i in range(len(imgPaths)):
        images.append(imread(img_path + "/" + imgPaths[i]))
        process.setValue(i)
    # images = [imread(img_path + "/" + path) for path in imgPaths] # 储存每一帧图片
    mimsave(save_path, images, "gif", duration=duration, loop=loop)  # 生成gif动图
    for each in imgPaths:  # 删除残留文件
        remove(img_path + "/" + each)
    process.close()
    return


if __name__ == '__main__':
    # 在这里输入你想跑的环境 设置起点和终点
    # use('Agg')  # 使图像不显示
    use('Qt5Agg')  # 画图环境为Qt5Agg
    G = np.matrix([[0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0],
                   [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0],
                   [1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0],
                   [1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
                   [0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1],
                   [1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0],
                   [1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1],
                   [0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1],
                   [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                   [0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0],
                   [1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1],
                   [0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1],
                   [1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0],
                   [0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0],
                   [1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1],
                   [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0],
                   [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0],
                   [1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0],
                   [0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1],
                   [1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0],
                   [1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0],
                   [0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0],
                   [0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                   [1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
                   [0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
                   [1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1],
                   [0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0],
                   [1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
                   [1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0],
                   [0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0]])
    # G = np.matrix(np.zeros((20, 30)))
    S = 44  # 设置起点
    E = 899  # 设置终点
    sample0 = Sample(G, S, E)
    Iter_K = 32  # 迭代次数
    Ant_num = 40  # 每一代蚂蚁只数
    # 参数设置
    parameter = Parameter()  # 参数类
    save_paths = Save_path()  # 设置图片保存路径
    if not os.path.exists(save_paths.result_save_path + "\Gen"):  # Gen为过程动图的存放位置，若不存在就创建
        os.mkdir(save_paths.result_save_path + "\Gen")
    runif(sample0)  # 检查初始设置是否有误
    # 画环境建模图
    Graph_Name = "Graph11"  # 设置此次环境名称
    print('\n确认无误后关闭窗口继续')
    sample0.draw_en(name="Environment-" + Graph_Name, save_path="Environment", if_num=True)
    print('程序正在运行...')
    T0 = perf_counter()
    Result = aca(sample0, save_paths.result_save_path, parameter, Iter_K, Ant_num)  # 获得最短路径和其他信息
    print("\n迭代完成，最短路径在第 " + str(Result.Mink + 1) + "代 被第 " + str(Result.Minm + 1) + " 只蚂蚁找到")
    T1 = perf_counter()
    print("程序运行时间:%s秒" % (round(T1 - T0, 2)))
    # -----------绘图-------------------
    # 绘制收敛曲线
    Result.save_drawline(save_path=save_paths.result_save_path, is_gif=parameter.is_gif)
    pyl.show()
    # 绘制最短路径爬行图
    Result.draw_path(Result.MinPath, 'Shortest Path Map (with dead-cell)', save_path=save_paths.result_save_path,
                     is_figure=False,
                     is_gif=parameter.is_gif)
    pyl.savefig(save_paths.result_save_path + "\Shortest Path Map (with dead-cell).jpg")
    pyl.show()
    Result.Graph = G  # 将结果对象的环境初始化
    Result.draw_path(Result.MinPath, "Shortest Path Map (without dead-cell)", save_path=save_paths.result_save_path,
                     is_figure=False,
                     is_gif=parameter.is_gif)
    pyl.savefig(save_paths.result_save_path + "\Shortest Path Map (without dead-cell).jpg")
    pyl.show()
    # 绘制收敛路径
    Result.draw_path(Result.LastPath, 'Convergence Path Diagram', save_path=save_paths.result_save_path,
                     is_figure=False, is_gif=parameter.is_gif)
    pyl.savefig(save_paths.result_save_path + "\Convergence Path Diagram.jpg")
    print("\r关闭图像以结束")
    pyl.show()
