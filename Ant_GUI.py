from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget, QDialog, QMessageBox, QPushButton, QLabel, QSlider, QGraphicsOpacityEffect, \
    QWhatsThis, QFrame, QCheckBox, QSpinBox, QComboBox, QLineEdit, QFileDialog
from PyQt5.QtGui import QFont, QBrush, QPixmap, QPalette, QResizeEvent
from PyQt5.QtCore import QTimer, QDateTime, QEvent, pyqtSignal
from Ant_with_gui import *
from time import localtime

pyl.rcParams['font.sans-serif'] = ['Kaitt', 'SimHei']  # 使画图正常显示中文
pyl.rcParams['axes.unicode_minus'] = False  # 使画图正常显示负号


# 此文件为GUI窗口界面的初始设置

# 主窗口
class MainWindow(QWidget):  # 界面主窗口
    def __init__(self, parent=None, *args, **kwargs):  # 初始化方法
        super().__init__(parent, *args, **kwargs)  # 优先调用父方法
        self.setWindowTitle("Ant Search -- Author : GS and XiaoYang")  # 设置窗口标题
        self.setWindowIcon(QIcon('ICON/icon.jpg'))  # 设置窗口图标
        self.resize(1920, 1080)
        self.setWindowFlag(Qt.WindowMinimizeButtonHint)  # 设置不能最大化
        self.setWindowFlag(Qt.MSWindowsFixedSizeDialogHint)  # 设置窗口无法改变大小
        self.time_lab1, self.time_lab2 = QLabel(self), QLabel(self)  # 时间标签
        self.mouse_x, self.mouse_y = None, None  # 鼠标在用户区按下的位置
        self.pressed = None  # 鼠标是否在用户区按下的标志
        self.Timer = QTimer()  # 自定义计时器
        self.Timer.start(1000)  # 一秒钟更新一次
        self.Timer.timeout.connect(self.update_time)  # 将信号连接至槽函数
        self.setup_ui()

    def setup_ui(self):  # 设置初始ui
        self.set_background()
        self.set_start()
        self.set_setting()
        self.set_exit()
        self.set_title()
        self.set_time_label()

    def set_background(self):
        # 设置背景图片
        if 5 < localtime().tm_hour < 16:  # 白天
            pix = QPixmap("background/day01.png")
        elif 15 < localtime().tm_hour < 19:  # 傍晚
            pix = QPixmap("background/sunset01.png")
        else:  # 晚上
            pix = QPixmap("background/night01.png")
        pix = pix.scaled(self.width(), self.height())
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(pix))
        self.setPalette(palette)

    def set_start(self):  # 设置start按钮
        start_btn = MainBtn(parent=self)
        start_btn.setText("Start")
        start_btn.move(int((self.width() - start_btn.width()) / 2), self.height() - 250)
        start_btn.setIcon(QIcon("ICON/route1.png"))
        start_btn.setDefault(True)  # 设为默认按键
        start_btn.setShortcut("Enter")
        # start_btn.setStyleSheet("background-image :url(btn1.png);")
        start_btn.clicked.connect(lambda: start_window.show())  # 自定义环境之后的信息存在.Sample里

    def set_setting(self):  # 设置option按钮
        option_btn = MainBtn(parent=self)
        option_btn.setText("Setting")
        option_btn.setIcon(QIcon("ICON/mail.png"))
        option_btn.move(int((self.width() - option_btn.width()) / 2), self.height() - 190)
        # option_btn.setStyleSheet("background-image :url(btn2.png);")
        option_btn.clicked.connect(lambda: option_window.show())

    def set_exit(self):  # 设置退出按钮
        exit_btn = MainBtn(parent=self)
        exit_btn.setText("Exit")
        exit_btn.setIcon(QIcon("ICON/exit.png"))
        exit_btn.move(int((self.width() - exit_btn.width()) / 2), self.height() - 130)
        exit_btn.setShortcut("Esc")  # 将按钮和Esc键绑定
        exit_btn.pressed.connect(self.close)
        # exit_btn.setStyleSheet("background-image :url(btn3.png);")

    def set_title(self):  # 设置标题样式
        title = QLabel(self)
        title_image = QPixmap(r'title/title.png')
        title.setPixmap(QPixmap(title_image))
        title.move(int((self.width() - title_image.width()) / 2), 300)

    def set_time_label(self):
        self.time_lab1.resize(237, 117)
        self.time_lab2.resize(237, 117)
        self.time_lab1.move(1797, 950)
        self.time_lab2.move(1710, 985)
        font1, font2 = QFont(), QFont()
        font1.setFamily("Monospaced")
        font2.setFamily("KaiTi")
        font1.setPointSize(33)
        font2.setPointSize(16)
        font1.setBold(True)  # 加粗
        font2.setBold(True)
        font2.setItalic(True)  # 斜体
        self.time_lab1.setFont(font1)
        self.time_lab2.setFont(font2)
        self.time_lab1.setStyleSheet("color: White;")
        self.time_lab2.setStyleSheet("color: White;")

    def update_time(self):
        time = QDateTime.currentDateTime()
        self.time_lab1.setText(time.toString('hh:mm'))
        self.time_lab2.setText(time.toString('yyyy-MM-dd dddd'))

    def closeEvent(self, event) -> None:  # 关闭确认的同时对关闭进行检测
        reply = QMessageBox.question(self, u'Wait!', u'Exit to Desktop?', QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
            sys.exit(0)  # 关闭所有窗口
        else:
            event.ignore()

    # 实现拖拽用户区移动窗口
    def mousePressEvent(self, event) -> None:
        if event.buttons() == Qt.LeftButton:
            self.pressed = True
            self.mouse_x, self.mouse_y = event.x(), event.y()

    def mouseMoveEvent(self, event) -> None:
        if self.pressed:
            self.move(self.x() + event.x() - self.mouse_x, self.y() + event.y() - self.mouse_y)

    def mouseReleaseEvent(self, event) -> None:
        self.pressed = False


# 主窗口的子部件
class MainBtn(QPushButton):
    def __init__(self, parent=None, *args):
        super().__init__(parent, *args)  # 优先调用父方法
        self.resize(400, 50)
        # 设置字体格式
        font = QFont()
        font.setFamily("Monospaced")
        font.setPointSize(18)
        font.setBold(True)
        font.setItalic(True)
        self.setFont(font)
        # 设置按钮透明度
        op = QGraphicsOpacityEffect()
        op.setOpacity(0.8)
        self.setGraphicsEffect(op)
        self.setAutoFillBackground(True)


# 开始界面
class StartWindow(QWidget):
    font = QFont()
    font.setFamily("Monospaced")
    font.setPointSize(18)
    font.setBold(True)  # 加粗
    font.setItalic(True)  # 斜体

    def __init__(self, parent=None, *args, **kwargs):  # 初始化方法
        super().__init__(parent, *args, **kwargs)  # 优先调用父方法
        self.setWindowTitle("Ant Search -- Author : GS and XiaoYang")  # 设置窗口标题
        self.setWindowIcon(QIcon('ICON/icon.jpg'))  # 设置窗口图标
        self.resize(1920, 1080)
        self.setWindowFlag(Qt.WindowMinimizeButtonHint)  # 设置不能最大化
        self.setWindowFlag(Qt.MSWindowsFixedSizeDialogHint)  # 设置窗口无法改变大小
        self.mouse_x, self.mouse_y = None, None  # 鼠标在用户区按下的位置
        self.pressed = None  # 鼠标是否在用户区按下的标志
        self.preview = QLabel(self)  # 地形预览标签
        self.show_num = True  # 设置创造环境时是否要显示序号
        self.row, self.col = QSpinBox(self), QSpinBox(self)  # 输入自定义环境的行和列
        self.Iter_K, self.Ant_num = QSpinBox(self), QSpinBox(self)  # 输入此次的迭代次数和蚂蚁只数
        self.dead_cell_check = QCheckBox("Use Deadcell Algorithm", self)
        self.gif_check = QCheckBox("Save Result As GIF", self)
        self.drawout_check = QCheckBox("Draw While Processing", self)
        self.num_show_check = QCheckBox("Show number on cell", self)
        self.Environment_window = EnWindow()  # 初始化环境类
        self.en_choose = QComboBox(self)  # 环境选择项
        self.current_filename = None  # 当前下拉列表选择的环境名
        self.temp_exist = False  # 环境中是否存在临时环境
        self.set_ui()

    def set_ui(self):
        self.choose_en_btn()
        self.del_en_btn()
        self.initialize_en()
        self.run_btn()
        self.parameter_btn()
        self.return_btn()
        self.show_graph_label()
        self.show_graph()
        self.show_btn()
        self.reset_s_and_e_btn()
        self.set_checks()
        self.set_row_and_col()
        self.create_en_btn()
        self.set_k_and_m()
        self.random_btn()

    def choose_en_btn(self):
        self.en_choose.resize(250, 30)
        self.en_choose.move(1500, 200)
        self.font.setPointSize(13)
        self.en_choose.setFont(self.font)
        # self.en_choose.setDuplicatesEnabled(True)  # 设置选项中不可重复

        en_choose_label = QLabel("Choose your Environment here", self)
        self.font.setPointSize(16)
        en_choose_label.setFont(self.font)
        en_choose_label.move(1500, 160)
        # 监测选择哪个环境 就将哪个环境激活
        self.en_choose.activated[str].connect(lambda val: self.en_activate(val))

    def en_activate(self, val):  # 激活当前所选环境
        self.current_filename = val
        self.load_graph()
        self.show_graph()

    def del_en_btn(self):
        del_btn = QPushButton("Delete", self)
        del_btn.setFont(self.font)
        del_btn.resize(110, 32)
        del_btn.move(1770, 199)
        del_btn.setIcon(QIcon("./ICON/delete.png"))
        del_btn.clicked.connect(self.del_en)

    def del_en(self):
        if self.en_choose.count():
            reply = QMessageBox.question(self, u'Wait!', u'Delete current Environment?', QMessageBox.Yes,
                                         QMessageBox.No)
            if reply == QMessageBox.Yes:
                os.remove(save_path.en_save_path + "/pkl/" + self.en_choose.currentText())  # 删除环境变量
                os.remove(save_path.en_save_path + '/' + self.en_choose.currentText()[:-4] + '.png')  # 删除环境图
                del_index = self.en_choose.currentIndex()
                self.en_choose.removeItem(del_index)
                if self.en_choose.count():  # 若还有剩余环境
                    self.en_activate(self.en_choose.currentText())  # 重新激活新环境

    def initialize_en(self):
        graphs = listdir(save_path.en_save_path + '/pkl')
        self.en_choose.addItems(graphs)
        self.current_filename = self.en_choose.currentText()
        if len(graphs):
            self.en_activate(self.current_filename)
        if "Temp.pkl" in graphs:
            self.temp_exist = True

    def load_graph(self):  # 从pkl中加载环境变量
        if self.current_filename is not None:
            f = open(save_path.en_save_path + '/pkl/' + self.current_filename, 'rb')
            temp_sample = load(f)
            row, col = np.shape(temp_sample.Graph)[0], np.shape(temp_sample.Graph)[1]
            self.Environment_window = EnWindow(en_sample=temp_sample, m=row, n=col, filename=self.current_filename)
            if temp_sample.S != -1:
                self.Environment_window.S.append(str(temp_sample.S))
            if temp_sample.E != -1:
                self.Environment_window.E.append(str(temp_sample.E))
            f.close()

    def run_btn(self):
        run_btn = QPushButton("RUN!!!", self)
        run_btn.setFont(self.font)
        run_btn.resize(210, 50)
        run_btn.move(1690, 1000)
        run_btn.setIcon(QIcon("ICON/route1.png"))
        run_btn.setDefault(True)  # 设为默认按键
        run_btn.setShortcut("Enter")  # 将按钮和Enter键绑定
        run_btn.clicked.connect(self.run)

    def run(self):
        sample = self.Environment_window.Sample
        if sample.S == -1:  # 先检查是否正确设置了起点终点
            QMessageBox.warning(self, u'Wait!', u'You have not set the start!')
        elif sample.E == -1:
            QMessageBox.warning(self, u'Wait!', u'You have not set the end!')
        else:
            if self.en_choose.count():
                reply = QMessageBox.question(self, u'Wait!', u'Have you finished deploying your environment?',
                                             QMessageBox.Yes,
                                             QMessageBox.No)
                if reply == QMessageBox.Yes:
                    iter_K, ant_num = self.Iter_K.value(), self.Ant_num.value()
                    if not os.path.exists(save_path.result_save_path + "/Gen"):  # Gen为过程动图的存放位置，若不存在就创建
                        os.mkdir(save_path.result_save_path + "/Gen")
                    t0 = perf_counter()
                    Result_sample = aca(sample, save_path.result_save_path, parameter, iter_K, ant_num)  # 获得最短路径和其他信息
                    if len(Result_sample.LastPath):  # 判断是否找到了通路或者用户是否中途取消
                        t1 = round(perf_counter() - t0, 2)
                        Result_sample.save_drawline(save_path=save_path.result_save_path, is_gif=parameter.is_gif)
                        Result_sample.draw_path(Result_sample.MinPath, 'Shortest Path Map (with dead-cell)',
                                                save_path=save_path.result_save_path,
                                                is_figure=False,
                                                is_gif=parameter.is_gif)
                        pyl.savefig(save_path.result_save_path + "\Shortest Path Map (with dead-cell).jpg")
                        reply = QMessageBox.question(self, u'Success!',
                                                     u'Run time is '+str(t1)+' s\nDo you want to use this result as the initial environment for the next iteration?',
                                                     QMessageBox.Yes,
                                                     QMessageBox.No)
                        if reply == QMessageBox.No:  # 如果选择不,则直接保存此次的结果图
                            pyl.close("all")
                            f = open(save_path.en_save_path + '/pkl/' + self.current_filename, 'rb')
                            temp_sample = load(f)
                            graph = temp_sample.Graph  # 获得运行之前环境的复制
                            f.close()
                            Result_sample.Graph = graph  # 将结果对象的环境初始化
                            Result_sample.draw_path(Result_sample.MinPath, "Shortest Path Map (without dead-cell)",
                                                    save_path=save_path.result_save_path, is_figure=False,
                                                    is_gif=parameter.is_gif)
                            pyl.savefig(save_path.result_save_path + "\Shortest Path Map (without dead-cell).jpg")
                            # 绘制收敛路径
                            Result_sample.draw_path(Result_sample.LastPath, 'Convergence Path Diagram',
                                                    save_path=save_path.result_save_path, is_figure=False,
                                                    is_gif=parameter.is_gif)
                            pyl.savefig(save_path.result_save_path + "\Convergence Path Diagram.jpg")
                    else:
                        QMessageBox.warning(self, u'Failed!', u'No Path find')

    def parameter_btn(self):
        para_btn = QPushButton("Set Parameters", self)
        para_btn.setFont(self.font)
        para_btn.resize(210, 50)
        para_btn.move(1450, 1000)
        para_btn.setIcon(QIcon("ICON/settings.png"))
        para_btn.clicked.connect(lambda: parameter_window.exec())

    def return_btn(self):
        return_btn = QPushButton("Return", self)
        return_btn.setFont(self.font)
        return_btn.resize(210, 50)
        return_btn.move(120, 1000)
        return_btn.setIcon(QIcon("ICON/exit.png"))
        return_btn.setShortcut("Esc")  # 将按钮和Esc键绑定
        return_btn.clicked.connect(self.close)

    def show_graph_label(self):  # 设置预览地形图的标签
        self.preview.resize(800, 800)
        self.preview.move(560, 50)
        self.preview.setStyleSheet("border: 1px solid #000000;")
        self.preview.setScaledContents(True)  # 设置像素图自动填充

    def show_graph(self):  # 预览地形图
        pix = QPixmap(save_path.en_save_path + '/' + self.current_filename[:-4] + '.png')
        self.preview.setPixmap(pix)

    def show_btn(self):
        graph_btn = QPushButton(self)
        graph_btn.setText("Graph Preview")
        graph_btn.setFont(self.font)
        graph_btn.resize(200, 50)
        graph_btn.move(860, 860)
        graph_btn.setIcon(QIcon("ICON/preview.png"))
        graph_btn.clicked.connect(lambda: (self.show_en(self.current_filename[:-4]), self.show_graph()))

    def show_en(self, en_name):
        if self.Environment_window.Sample is not None:
            self.Environment_window.Sample.draw_en(en_name, save_path.en_save_path, if_num=self.show_num)

    def reset_s_and_e_btn(self):  # 设置起点和终点
        start_set = QPushButton("Reset Start and End", self)
        start_set.setFont(self.font)
        start_set.resize(300, 50)
        start_set.move(1120, 1000)
        start_set.setIcon(QIcon("ICON/route.png"))
        start_set.clicked.connect(self.reset_s_and_e)

    def reset_s_and_e(self):
        if self.en_choose.count():
            self.Environment_window.set_en(self.show_num)
            if self.Environment_window.filename == "Temp":  # 表示用户选择了不保存
                self.add_en("Temp")
                self.preview.setPixmap(QPixmap(save_path.en_save_path + '/Temp.png'))
            else:  # 表示用户此次选择了保存
                self.add_en(self.Environment_window.filename)

    def set_checks(self):  # 设置是否要保存gif 画出中间过程 使用死点算法
        self.dead_cell_check.setChecked(True)
        self.dead_cell_check.setFont(self.font)
        self.dead_cell_check.move(120, 135)
        self.dead_cell_check.toggled.connect(self.update_checks)

        self.gif_check.setFont(self.font)
        self.gif_check.move(120, 345)
        self.gif_check.toggled.connect(self.update_checks)

        self.drawout_check.setFont(self.font)
        self.drawout_check.move(120, 555)
        self.drawout_check.toggled.connect(self.update_checks)

    def update_checks(self):  # 更新参数
        parameter.Deadcell = self.dead_cell_check.isChecked()
        parameter.is_gif = self.gif_check.isChecked()
        parameter.if_drawout = self.drawout_check.isChecked()
        self.show_num = self.num_show_check.isChecked()

    def set_row_and_col(self):
        self.font.setItalic(False)
        self.font.setPointSize(12)
        # 设置自定义行数和列数
        self.row.resize(100, 30)
        self.col.resize(100, 30)
        self.row.move(120, 765)
        self.col.move(330, 765)
        self.row.setMaximum(81), self.row.setMinimum(3)
        self.col.setMaximum(81), self.col.setMinimum(3)
        self.row.setFont(self.font)
        self.col.setFont(self.font)
        # 设置提示标签
        self.font.setPointSize(15)
        diy_label = QLabel("Create Your Environment!!", self)
        row_label, col_label = QLabel("ROW:", self), QLabel("COL:", self)
        diy_label.move(120, 700)
        row_label.move(120, 730)
        col_label.move(330, 730)
        row_label.setFont(self.font)
        col_label.setFont(self.font)
        diy_label.setFont(self.font)
        # 设置是否在Cell上标出序号标签
        self.num_show_check.resize(225, 30)
        self.num_show_check.setFont(self.font)
        self.num_show_check.move(120, 810)
        self.num_show_check.setChecked(True)
        self.num_show_check.toggled.connect(self.update_checks)

    def create_en_btn(self):
        crate_btn = QPushButton("CREATE NOW!!", self)
        crate_btn.resize(210, 50)
        crate_btn.move(170, 860)
        crate_btn.setFont(self.font)
        crate_btn.setIcon(QIcon("ICON/Create.png"))
        crate_btn.clicked.connect(self.create_en)

    def create_en(self):
        Row = self.row.value()
        Col = self.col.value()
        self.Environment_window = EnWindow(m=Row, n=Col)
        self.Environment_window.set_en(self.show_num)
        if self.Environment_window.filename != "Temp":  # 若此次选择保存
            self.add_en(self.Environment_window.filename)
        else:  # 若此次选择不保存
            self.add_en("Temp")
            self.preview.setPixmap(QPixmap(save_path.en_save_path + '/Temp.png'))

    def add_en(self, en_name):
        if not (en_name + '.pkl' in [self.en_choose.itemText(i) for i in range(self.en_choose.count())]):  # 若列表中已有
            self.en_choose.addItem(en_name + '.pkl')  # 将新创建的环境添加到下拉列表中
        if self.en_choose.count():  # 若当前列表项里已选择有环境 则改为选择新环境
            self.en_choose.setCurrentText(en_name + '.pkl')
        self.current_filename = self.en_choose.currentText()
        self.show_en(en_name)  # 展示新创建的环境的同时将环境图片保存
        self.en_activate(en_name + '.pkl')  # 激活环境

    def set_k_and_m(self):
        self.font.setItalic(False)
        self.font.setPointSize(12)
        # 设置自定义迭代次数和蚂蚁只数
        self.Iter_K.setMaximum(999), self.Ant_num.setMaximum(999)
        self.Iter_K.setValue(20), self.Ant_num.setValue(100)
        self.Iter_K.resize(100, 30)
        self.Ant_num.resize(100, 30)
        self.Iter_K.move(1500, 765)
        self.Ant_num.move(1710, 765)
        self.Iter_K.setFont(self.font)
        self.Ant_num.setFont(self.font)
        # 设置提示标签
        self.font.setPointSize(15)
        k_m_label = QLabel("Set iteration and ants number!!", self)
        iter_k_label, ant_num_label = QLabel("Iteration:", self), QLabel("Ants number:", self)
        k_m_label.move(1500, 700)
        iter_k_label.move(1500, 730)
        ant_num_label.move(1710, 730)
        iter_k_label.setFont(self.font)
        ant_num_label.setFont(self.font)
        k_m_label.setFont(self.font)

    def random_btn(self):
        randomize_btn = QPushButton("Randomize!!", self)
        randomize_btn.resize(210, 50)
        randomize_btn.move(1550, 860)
        randomize_btn.setFont(self.font)
        randomize_btn.setIcon(QIcon("ICON/random.png"))
        randomize_btn.clicked.connect(self.randomize_en)

    def randomize_en(self):
        Row = self.row.value()
        Col = self.col.value()
        random_sample = Sample(g=np.matrix(np.random.randint(0, 2, (Row, Col))))
        self.Environment_window = EnWindow(m=Row, n=Col, en_sample=random_sample)
        self.Environment_window.set_en(self.show_num)
        if self.Environment_window.filename != "Temp":  # 若此次选择保存
            self.add_en(self.Environment_window.filename)
        else:  # 若此次选择不保存
            self.add_en("Temp")
            self.preview.setPixmap(QPixmap(save_path.en_save_path + '/Temp.png'))

    # 实现拖拽用户区移动窗口
    def mousePressEvent(self, event) -> None:
        if event.buttons() == Qt.LeftButton:
            self.pressed = True
            self.mouse_x, self.mouse_y = event.x(), event.y()

    def mouseMoveEvent(self, event) -> None:
        if self.pressed:
            self.move(self.x() + event.x() - self.mouse_x, self.y() + event.y() - self.mouse_y)

    def mouseReleaseEvent(self, event) -> None:
        self.pressed = False


# 输入弹框
class Input_filenameDialog(QDialog):
    font = QFont()
    font.setFamily("Monospaced")
    font.setPointSize(14)

    def __init__(self, parent=None, *args, **kwargs):  # 初始化方法
        super().__init__(parent, *args, **kwargs)  # 优先调用父方法
        self.setWindowFlag(Qt.MSWindowsFixedSizeDialogHint)  # 设置窗口无法改变大小
        self.setWindowTitle("Save your own Graph")
        self.resize(600, 200)
        self.filename = None
        self.edit_filename = QLineEdit(self)
        self.set_btn()
        self.set_lineedit()
        self.line_label()
        self.exec()

    def set_btn(self):
        save_btn = QPushButton("Save", self)
        save_btn.resize(80, 30)
        save_btn.move(330, 160)
        save_btn.clicked.connect(self.save)
        save_btn.setDefault(True)  # 设为默认按键
        not_save_btn = QPushButton("Don't save", self)
        not_save_btn.resize(80, 30)
        not_save_btn.move(420, 160)
        not_save_btn.clicked.connect(self.reject)
        cancel_btn = QPushButton("Cancel", self)
        cancel_btn.resize(80, 30)
        cancel_btn.move(510, 160)
        cancel_btn.clicked.connect(lambda: self.done(2))

    def set_lineedit(self):
        self.edit_filename.resize(300, 30)
        self.edit_filename.move(160, 80)

    def line_label(self):
        label_l = QLabel("Graph name:", self)
        label_top = QLabel("Edit file name", self)
        label_l.setFont(self.font)
        self.font.setPointSize(12)
        label_top.setFont(self.font)
        label_l.move(35, 84)
        label_top.move(160, 55)

    def save(self):
        self.filename = self.edit_filename.text()
        if self.filename == "":
            self.edit_filename.setPlaceholderText("filename cannot be empty!")
        else:
            self.accept()


#  参数设置窗口
class ParameterSetWindow(QDialog):
    def __init__(self, parent=None, *args, **kwargs):  # 初始化方法
        super().__init__(parent, *args, **kwargs)  # 优先调用父方法
        self.pressed = None
        self.mouse_x, self.mouse_y = None, None
        self.setWindowTitle("Parameter Set -- Author : GS and XiaoYang")  # 设置窗口标题
        self.setWindowIcon(QIcon('ICON/icon.jpg'))  # 设置窗口图标
        self.setWindowOpacity(0.85)  # 设置窗口不透明度
        self.setWindowFlag(Qt.WindowCloseButtonHint)  # 设置只显示关闭按钮
        self.setWindowFlag(Qt.MSWindowsFixedSizeDialogHint)  # 设置窗口无法改变大小
        self.resize(800, 450)
        self.alpha = ParaSlider(self)
        self.beta = ParaSlider(self)
        self.gama = ParaSlider(self)
        self.rho = ParaSlider(self)
        self.q = ParaSlider(self)
        self.ra = ParaSlider(self)
        self.rate = ParaSlider(self)
        self.set_sliders()
        self.help_label = QLabel(self)
        self.set_help()

    def set_sliders(self):
        self.alpha_slider()
        self.beta_slider()
        self.gama_slider()
        self.rho_slider()
        self.q_slider()
        self.ra_slider()
        self.rate_slider()

    def alpha_slider(self):
        # 设置滑块
        self.alpha.setRange(0, 200)
        self.alpha.setValue(int(parameter.Alpha * 100))  # 设置初始值
        self.alpha.move(30, 30)
        # 设置参数标签
        alpha_label = ParaLabel(self)
        alpha_label.move(570, 28)
        alpha_label.setText('Alpha:' + str(self.alpha.value() / 100))
        self.alpha.valueChanged.connect(lambda: alpha_label.setText('Alpha:' + str(self.alpha.value() / 100)))

    def beta_slider(self):
        # 设置滑块
        self.beta.setRange(0, 200)
        self.beta.setValue(int(parameter.Beta * 100))  # 设置初始值
        self.beta.move(30, 90)
        # 设置参数标签
        beta_label = ParaLabel(self)
        beta_label.move(570, 88)
        beta_label.setText('Beta:' + str(self.beta.value() / 100))
        self.beta.valueChanged.connect(lambda: beta_label.setText('Beta:' + str(self.beta.value() / 100)))

    def gama_slider(self):
        # 设置滑块
        self.gama.setRange(0, 200)
        self.gama.setValue(int(parameter.Gama * 100))  # 设置初始值
        self.gama.move(30, 150)
        # 设置参数标签
        gama_label = ParaLabel(self)
        gama_label.move(570, 148)
        gama_label.setText('Gama:' + str(self.gama.value() / 100))
        self.gama.valueChanged.connect(lambda: gama_label.setText('Gama:' + str(self.gama.value() / 100)))

    def rho_slider(self):
        # 设置滑块
        self.rho.setRange(0, 10)
        self.rho.setValue(int(parameter.Rho * 100))  # 设置初始值
        self.rho.move(30, 210)
        # 设置参数标签
        rho_label = ParaLabel(self)
        rho_label.move(570, 208)
        rho_label.setText('Rho:' + str(self.rho.value() / 100))
        self.rho.valueChanged.connect(lambda: rho_label.setText('Rho:' + str(self.rho.value() / 100)))

    def q_slider(self):
        # 设置滑块
        self.q.setRange(0, 100)
        self.q.setValue(int(parameter.Q))  # 设置初始值
        self.q.move(30, 270)
        # 设置参数标签
        q_label = ParaLabel(self)
        q_label.move(570, 268)
        q_label.setText('Q:' + str(self.q.value()))
        self.q.valueChanged.connect(lambda: q_label.setText('Q:' + str(self.q.value())))

    def ra_slider(self):
        # 设置滑块
        self.ra.setRange(0, 100)
        self.ra.setValue(int(parameter.Ra * 100))  # 设置初始值
        self.ra.move(30, 330)
        # 设置参数标签
        ra_label = ParaLabel(self)
        ra_label.move(570, 328)
        ra_label.setText('Ra:' + str(self.ra.value() / 100))
        self.ra.valueChanged.connect(lambda: ra_label.setText('Ra:' + str(self.ra.value() / 100)))

    def rate_slider(self):
        # 设置滑块
        self.rate.setRange(0, 100)
        self.rate.setValue(int(parameter.Rate * 100))  # 设置初始值
        self.rate.move(30, 390)
        # 设置参数标签
        rate_label = ParaLabel(self)
        rate_label.move(570, 388)
        rate_label.setText('Rate:' + str(self.rate.value() / 100))
        self.rate.valueChanged.connect(lambda: rate_label.setText('Rate:' + str(self.rate.value() / 100)))

    def closeEvent(self, event):  # 将设置的参数保存到全局变量parameter
        parameter.Alpha = self.alpha.value() / 100
        parameter.Beta = self.beta.value() / 100
        parameter.Gama = self.gama.value() / 100
        parameter.Rho = self.rho.value() / 100
        parameter.Q = self.q.value()
        parameter.Ra = self.ra.value() / 100
        parameter.Rate = self.rate.value() / 100
        parameter.save()

    def set_help(self):  # 设置帮助提示框
        font1 = QFont()
        font1.setFamily("Monospaced")
        font1.setPointSize(12)
        font1.setBold(True)  # 加粗
        self.help_label.setText("Alpha: Pheromone importance\n"
                                "Beta: heuristic factor importance\n"
                                "Gama: path steering angle importance\n"
                                "Rho: Pheromone evaporation coefficient\n"
                                "Q: Pheromone Increase Intensity Coefficient\n"
                                "Ra: The rationality of the ant\n"
                                "Rate: The weight of the distance between nodes in the heuristic factor"
                                )
        self.setFont(font1)
        self.help_label.resize(638, 128)
        self.help_label.move(117, 0)
        # 设置label边框样式
        self.help_label.setFrameShape(QFrame.Box)
        self.help_label.setFrameShadow(QFrame.Raised)  # 设置阴影
        self.help_label.setStyleSheet('border: 1px solid #000000;background-color: #7A7A7A;color: White')
        # self.help_label.setAlignment(Qt.AlignVCenter)  # 调整文字和边框对齐
        self.help_label.setVisible(False)

    def event(self, event) -> bool:  # 设置问号按钮的点击事件
        if event.type() == QEvent.EnterWhatsThisMode:
            QWhatsThis.leaveWhatsThisMode()  # 让鼠标不要点击问号后就变成不可用
            if self.help_label.isVisible():
                self.help_label.setVisible(False)
            else:
                self.help_label.setVisible(True)
        return QDialog.event(self, event)

    # 实现拖拽用户区移动窗口
    def mousePressEvent(self, event) -> None:
        if event.buttons() == Qt.LeftButton:
            self.pressed = True
            self.mouse_x, self.mouse_y = event.x(), event.y()

    def mouseMoveEvent(self, event) -> None:
        if self.pressed:
            self.move(self.x() + event.x() - self.mouse_x, self.y() + event.y() - self.mouse_y)

    def mouseReleaseEvent(self, event) -> None:
        self.pressed = False


# 参数设置窗口的子部件
class ParaSlider(QSlider):
    def __init__(self, parent=None, *args):  # 初始化方法
        super().__init__(Qt.Horizontal, parent, *args)  # 优先调用父方法
        self.resize(500, 30)
        self.setSingleStep(1)


# 参数设置窗口的子部件
class ParaLabel(QLabel):
    font1 = QFont()
    font1.setFamily("Monospaced")
    font1.setPointSize(16)
    font1.setBold(True)  # 加粗
    font1.setItalic(True)  # 斜体

    def __init__(self, parent=None, *args):  # 初始化方法
        super().__init__(parent, *args)  # 优先调用父方法
        self.resize(124, 30)
        self.setFont(self.font1)


# 设置存放路径
class SettingWindow(QWidget):
    font = QFont()
    font.setFamily("Monospaced")
    font.setPointSize(20)
    font.setBold(True)  # 加粗
    font.setItalic(True)  # 斜体

    def __init__(self, parent=None, *args, **kwargs):  # 初始化方法
        super().__init__(parent, *args, **kwargs)  # 优先调用父方法
        self.setWindowTitle("Ant Search -- Option -- Author : GS and XiaoYang")  # 设置窗口标题
        self.setWindowIcon(QIcon('ICON/icon.jpg'))  # 设置窗口图标
        self.resize(800, 450)
        self.setWindowFlag(Qt.WindowMinimizeButtonHint)  # 设置不能最大化
        self.setWindowFlag(Qt.MSWindowsFixedSizeDialogHint)  # 设置窗口无法改变大小
        self.e_path_edit = QLineEdit(self)
        self.r_path_edit = QLineEdit(self)
        self.set_ui()

    def set_ui(self):
        self.en_save_label()
        self.result_label()
        self.en_save_btn()
        self.result_btn()
        self.en_path_edit()
        self.result_path_edit()

    def en_save_label(self):
        en_save_label = QLabel("Set the environment variable save path:", self)
        en_save_label.setFont(self.font)
        en_save_label.move(60, 60)

    def result_label(self):
        result_label = QLabel("Set the result save path:", self)
        result_label.setFont(self.font)
        result_label.move(60, 250)

    def en_save_btn(self):
        self.font.setPointSize(10)
        self.font.setBold(False)  # 加粗
        self.font.setItalic(False)
        en_save_btn = QPushButton(self)
        en_save_btn.resize(40, 30)
        en_save_btn.setFont(self.font)
        en_save_btn.move(560, 150)
        en_save_btn.setIcon(QIcon("ICON/mail.png"))
        en_save_btn.clicked.connect(self.set_en_path)

    def result_btn(self):
        result_btn = QPushButton(self)
        result_btn.resize(40, 30)
        result_btn.setFont(self.font)
        result_btn.move(560, 330)
        result_btn.setIcon(QIcon("ICON/mail.png"))
        result_btn.clicked.connect(self.set_re_path)

    def en_path_edit(self):
        self.e_path_edit.resize(490, 30)
        self.e_path_edit.move(60, 150)
        self.e_path_edit.setFont(self.font)
        self.e_path_edit.setText(save_path.en_save_path)
        self.e_path_edit.setReadOnly(True)

    def result_path_edit(self):
        self.r_path_edit.resize(490, 30)
        self.r_path_edit.move(60, 330)
        self.r_path_edit.setFont(self.font)
        self.r_path_edit.setText(save_path.result_save_path)
        self.r_path_edit.setReadOnly(True)

    def set_en_path(self):
        result = QFileDialog.getExistingDirectory(self, "Set environment save path", "./")  # 获得此次设置的路径
        save_path.en_save_path = result
        self.e_path_edit.setText(result)

    def set_re_path(self):
        result = QFileDialog.getExistingDirectory(self, "Set environment save path", "./")  # 获得此次设置的路径
        save_path.result_save_path = result
        self.r_path_edit.setText(result)

    def closeEvent(self, event):  # 将设置的储存路径保存
        QMessageBox.warning(self, u'Warning!', u'You must reboot to take the changes ')
        if not os.path.exists(save_path.en_save_path + '/pkl'):  # 需要在新路径下新建pkl文件夹以储存环境变量文件
            os.mkdir(save_path.en_save_path + '/pkl')
        save_path.save()


# 自定义环境窗口
class EnWindow(QDialog):
    def __init__(self, parent=None, m=0, n=0, en_sample=None, filename=None, *args, **kwargs):  # 初始化方法
        super().__init__(parent, *args, **kwargs)  # 优先调用父方法
        self.filename = filename  # 此次创建的环境文件名
        self.Sample = en_sample  # 初始化环境矩阵
        self.M, self.N = m, n
        self.S, self.E = [], []  # 初始化环境中的起点和终点 注意类型为['str']
        self.click_count = 1  # 初始化环境中设置起点和终点的次数
        self.setSizeGripEnabled(True)  # 在右下角添加缩放
        self.set_font()

    def set_font(self):  # 环境初始化
        self.setWindowFlag(Qt.WindowMinMaxButtonsHint)
        self.setWindowTitle("Ant Search -- Design Your Environment -- Author : GS and XiaoYang")  # 设置窗口标题
        self.setWindowIcon(QIcon('ICON/icon.jpg'))  # 设置窗口图标
        self.setWindowOpacity(0.95)  # 设置窗口不透明度
        if self.M <= 10 and self.N <= 10:  # 设置初始窗口大小
            self.resize(100 * self.N, 100 * self.M)
        elif self.M <= 20 and self.N <= 20:
            self.resize(60 * self.N, 60 * self.M)
        elif self.M <= 30 and self.N <= 30:
            self.resize(40 * self.N, 40 * self.M)
        elif self.M > 81 or self.N > 81:
            exit("You can not set M or N over 81 !")
        else:
            self.setWindowState(Qt.WindowMaximized)  # 设置窗口最大化(M,N最大到81)

    def set_en(self, if_num=True):  # 生成自定义环境
        for i in range(self.M * self.N):
            cell = Cell(self, self.M, self.N, if_num)
            cell.setObjectName(str(i))  # 记录该栅格的编号
            if if_num:
                cell.setText(str(i))
            if self.Sample is not None:
                cell.state = self.Sample.Graph[n_to_l(i, self.M, self.N)]
                if cell.state == 1:
                    cell.setStyleSheet("background-color: #373737;")  # 变成黑色
                    cell.setText("")  # 变成黑色的同时销毁上面的标号
                if len(self.S):
                    if i == int(self.S[0]):
                        cell.state = -1
                        cell.setStyleSheet("background-color: #99ffff;")  # 设置起点为言和绿
                        cell.setText("Start")  # 变成言和绿的同时销毁上面的标号
                if len(self.E):
                    if i == int(self.E[0]):
                        cell.state = 2
                        cell.setStyleSheet("background-color: #66ccff;")  # 设置终点为天依蓝
                        cell.setText("End")  # 变成天依蓝的同时销毁上面的标号
            cell.move(n_to_l(i, self.M, self.N)[1] * cell.width(), n_to_l(i, self.M, self.N)[0] * cell.height())
        self.exec()

    def save_en(self, filename):
        f = open(save_path.en_save_path + '/pkl/' + filename + '.pkl', 'wb')
        # 保存环境地形
        dump(self.Sample, f)
        f.close()

    def get_sample(self) -> None:
        self.Sample = Sample(g=np.matrix(np.zeros((self.M, self.N))))
        for each_cell in self.findChildren(Cell):
            [x, y] = n_to_l(int(each_cell.objectName()), self.M, self.N)
            if each_cell.state == 1 or each_cell.state == 0:
                self.Sample.Graph[x, y] = int(each_cell.state)

    def resizeEvent(self, a0: QResizeEvent) -> None:  # 监听窗口大小是否改变
        children = self.findChildren(Cell)
        for i in range(len(children)):  # 使按钮大小随着窗口大小改变而改变
            children[i].resize(int(self.width() / self.N), int(self.height() / self.M))
            children[i].move(n_to_l(i, self.M, self.N)[1] * children[i].width(),
                             n_to_l(i, self.M, self.N)[0] * children[i].height())

    def closeEvent(self, event) -> None:  # 关闭确认的同时对关闭进行检测
        dialog = Input_filenameDialog(self)
        reply = dialog.result()
        if reply == 0:  # 用户选择了不保存环境（用于重新设置起点终点）
            self.filename = "Temp"
            self.get_sample()  # 将自定义环境信息储存
            if len(self.S):
                self.Sample.S = int(self.S[0])
            if len(self.E):
                self.Sample.E = int(self.E[0])
            self.Sample.draw_en("Temp", save_path.en_save_path)  # 不保存则创造一个临时预览图
            self.save_en("Temp")
            event.accept()
        elif reply == 1:  # 用户选择了保存环境
            self.filename = dialog.filename
            self.get_sample()  # 将自定义环境信息储存
            if len(self.S):
                self.Sample.S = int(self.S[0])
            if len(self.E):
                self.Sample.E = int(self.E[0])
            self.save_en(dialog.filename)
            event.accept()
        elif reply == 2:  # 用户选择了取消 表示取消当前操作
            event.ignore()


class Cell(QPushButton):  # 设置展示的栅格
    rightClicked = pyqtSignal()  # 自定义右击信号

    def __init__(self, parent=None, m=0, n=0, if_num=True, *args):
        super().__init__(parent, *args)  # 优先调用父方法
        self.setObjectName("0")  # 记录该栅格的编号
        self.parent = parent
        self.if_num = if_num
        self.state = 0  # 记录该栅格的状态{-1:起点,0:白色可通行,1:障碍物不可通行,2:终点}
        self.setStyleSheet("background-color: White;")
        self.resize(int(parent.width() / n), int(parent.height() / m))  # 初始化按钮大小
        self.pressed.connect(self.set_blockade)  # 将按下操作与设置障碍物槽函数连接
        self.rightClicked.connect(self.control_start_end)  # 将右击操作与设置起点终点槽函数连接

    def set_blockade(self):
        if self.state == 1:  # 如果该栅格为障碍物 则标记为无障碍
            self.setStyleSheet("background-color: White;")  # 变成白色
            self.state = 0  # 将该格状态设为可通行
            if self.if_num:
                self.setText(self.objectName())  # 变成白色的同时恢复上面的标号
        elif self.state == -1:  # 若该栅格为起点
            self.del_s(self.parent)  # 删除之前设立的起点
            self.setStyleSheet("background-color: #373737;")  # 变成黑色
            self.state = 1  # 将该格状态设为障碍物不可通行
            self.setText("")  # 变成黑色的同时销毁上面的标号
        elif self.state == 2:  # 若该栅格为终点
            self.del_e(self.parent)  # 删除之前设立的终点
            self.setStyleSheet("background-color: #373737;")  # 变成黑色
            self.state = 1  # 将该格状态设为障碍物不可通行
            self.setText("")  # 变成黑色的同时销毁上面的标号
        else:
            self.setStyleSheet("background-color: #373737;")  # 变成黑色
            self.state = 1  # 将该格状态设为障碍物不可通行
            self.setText("")  # 变成黑色的同时销毁上面的标号

    def control_start_end(self):  # 实现一个右键事件同时可以设置起点和终点
        if len(self.parent.S) == 0:
            if self.state == 2:  # 若此次尝试在终点处设置起点
                self.del_e(self.parent)
            self.set_s(self.parent)  # 设立新的起点
        elif len(self.parent.S) == 1 and len(self.parent.E) == 0:
            if self.state == -1:  # 若此次尝试在起点处设置终点
                self.del_s(self.parent)
            self.set_e(self.parent)  # 设立新的终点
        elif len(self.parent.S) == 1 and len(self.parent.E) == 1:
            if self.state == -1 or self.state == 2:  # 如果设置在起点或终点上
                self.swap(self.parent)
            elif self.parent.click_count == 1:
                self.del_s(self.parent)  # 删除之前设立的起点
                self.set_s(self.parent)  # 设立新的起点
                self.parent.click_count = 2
            elif self.parent.click_count == 2:
                self.del_e(self.parent)  # 删除之前设立的终点
                self.set_e(self.parent)  # 设立新的终点
                self.parent.click_count = 1

    def set_s(self, parent):
        parent.S.append(self.objectName())
        self.setStyleSheet("background-color: #99ffff;")  # 设置起点为言和绿
        self.setText("Start")  # 变成言和绿的同时销毁上面的标号
        self.state = -1

    def set_e(self, parent):
        parent.E.append(self.objectName())
        self.setStyleSheet("background-color: #66ccff;")  # 设置终点为天依蓝
        self.setText("End")  # 变成天依蓝的同时销毁上面的标号
        self.state = 2

    def del_s(self, parent):  # 删除之前设立的起点
        cell_s = parent.findChild(Cell, parent.S[0])
        cell_s.state = 0
        cell_s.setStyleSheet("background-color: White;")
        if self.if_num:
            cell_s.setText(cell_s.objectName())
        else:
            cell_s.setText("")
        del parent.S[0]

    def del_e(self, parent):  # 删除之前设立的终点
        cell_e = parent.findChild(Cell, parent.E[0])
        cell_e.state = 0
        cell_e.setStyleSheet("background-color: White;")
        if self.if_num:
            cell_e.setText(cell_e.objectName())
        else:
            cell_e.setText("")
        del parent.E[0]

    @staticmethod
    def swap(parent):  # 交换起点和终点位置
        cell_s = parent.findChild(Cell, parent.S[0])
        cell_e = parent.findChild(Cell, parent.E[0])
        # 设置起点为终点
        cell_s.setStyleSheet("background-color: #66ccff;")  # 设置终点为天依蓝
        cell_s.state = 2
        cell_s.setText("End")  # 变成言和绿的同时销毁上面的标号
        parent.E[0] = cell_s.objectName()
        # 设置终点为起点
        cell_e.setStyleSheet("background-color: #99ffff;")  # 设置起点为言和绿
        cell_e.state = -1
        cell_e.setText("Start")  # 变成言和绿的同时销毁上面的标号
        parent.S[0] = cell_e.objectName()

    def mousePressEvent(self, event) -> None:

        super().mousePressEvent(event)  # 保留原本的鼠标单击信号
        if event.buttons() == Qt.RightButton:
            if self.state != 1:  # 只允许在非障碍物处设置起点终点
                self.rightClicked.emit()


if __name__ == '__main__':
    import sys

    # 全局变量
    save_path = Save_path()  # 文件保存路径类
    save_path.load()  # 加载文件储存路径
    parameter = Parameter()  # 参数类
    parameter.load()  # 加载参数设置
    # 创建一个应用程序对象
    app = QApplication(sys.argv)
    # 创建控件
    Main_window = MainWindow()
    start_window = StartWindow()
    parameter_window = ParameterSetWindow()
    option_window = SettingWindow()

    # 设置控件
    a = QDialog
    # 展示控件
    Main_window.show()
    # 应用程序的执行，进入到消息循环
    sys.exit(app.exec_())