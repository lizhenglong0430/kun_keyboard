import functools
import os
import sys
# 该QtCore模块包含核心类，包括事件循环和 Qt 的信号和槽机制。
# 它还包括针对动画、状态机、线程、映射文件、共享内存、正则表达式以及用户和应用程序设置的平台独立抽象。
import threading

import playsound
from pynput.keyboard import Listener, GlobalHotKeys
from PyQt5.QtCore import Qt, QTimer, QUrl
from PyQt5.QtGui import QPixmap, QIcon, QCursor, QFont, QDesktopServices
# “小部件”是赋予用户可以与之交互的 UI 组件的名称
from PyQt5.QtWidgets import (
    QApplication,
    QLabel,  # 只是一个标签，没有互动
    QMainWindow,
    QMessageBox,
    QSystemTrayIcon,
    QAction, QMenu,
)


# 得到当前执行文件同级目录的其他文件绝对路径
def resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath('.')
    return os.path.join(base_path, relative_path)


# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        # 获取位置
        self.pos_first = self.pos()
        # 气泡
        self.lab_bubble = QLabel(self)
        self.lab_content = QLabel(self)
        # 文字居中
        self.lab_content.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # ikun
        self.lab = QLabel(self)

        # 定时器，用于长时间不输入清空输入状态和闭嘴
        self.timer = QTimer()
        self.timer.timeout.connect(self.reset_char)
        # 3秒定时清除文字
        self.timer.start(3000)

        self.ch2audio = {
            # 'j': os.path.join(os.path.dirname(os.path.abspath(__file__)), "audios", "j.mp3"),
            'j': resource_path(os.path.join("audios", "j.mp3")),
            'n': resource_path(os.path.join("audios", "n.mp3")),
            't': resource_path(os.path.join("audios", "t.mp3")),
            'm': resource_path(os.path.join("audios", "m.mp3")),
            'J': resource_path(os.path.join("audios", "j.mp3")),
            'N': resource_path(os.path.join("audios", "n.mp3")),
            'T': resource_path(os.path.join("audios", "t.mp3")),
            'M': resource_path(os.path.join("audios", "m.mp3")),
            'jntm': resource_path(os.path.join("audios", "ngm.mp3"))
        }

        self.init_monitor()
        self.init_monitor_all()
        self.windowinit()
        self.icon_quit()

    def windowinit(self):
        # 初始窗口设置大一点以免放入的图片显示不全
        self.pet_width = 200
        self.pet_height = 200
        # 获取桌面桌面大小决定宠物的初始位置为右上角
        desktop = QApplication.desktop()
        self.x = desktop.width() - self.pet_width
        self.y = 100
        self.setGeometry(self.x, self.y, self.pet_width, self.pet_height)
        self.setWindowTitle("坤音键盘-by 政函数")

        self.lab_bubble.setGeometry(0, 0, 150, 150)
        self.lab_bubble.setPixmap(QPixmap(resource_path(os.path.join("imgs", "bubble.png"))))

        self.lab.setGeometry(50, 80, 150, 150)
        self.lab.setPixmap(QPixmap(resource_path(os.path.join("imgs", "cai1.png"))))

        # 设置窗口为 无边框 | 保持顶部显示
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        # 设置窗口透明
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.show()

    def icon_quit(self):
        mini_icon = QSystemTrayIcon(self)
        mini_icon.setIcon(QIcon(resource_path(os.path.join("imgs", "kun_keyboard.ico"))))
        mini_icon.setToolTip("桌面宠物-by 政函数")
        # 为托盘增加一个菜单选项
        tpMenu = QMenu(self)
        # 为菜单指定一个选项
        # 1 toggle()、triggered()、clicked()区别
        # 这三个信号都是按钮点击后发射的信号，区别在于：
        # clicked()用于Button发射的信号
        # triggered()用于QAction发射的信号，原型：​​void triggered(bool checked = false);​​
        # toggle()用于ChekBox,非开即关，原型：​​void toggled(bool);​​
        version_menu = QAction("作者", self, triggered=self.version_content)
        tpMenu.addAction(version_menu)
        quit_menu = QAction('退出', self, triggered=self.quit)
        tpMenu.addAction(quit_menu)
        open_qq_group = QAction('bilibili作者链接', self, triggered=self.open_qq_group)
        tpMenu.addAction(open_qq_group)
        mini_icon.setContextMenu(tpMenu)
        mini_icon.show()

    def mousePressEvent(self, QMouseEvent):
        if QMouseEvent.button() == Qt.MouseButton.LeftButton:
            self.pos_first = QMouseEvent.globalPos() - self.pos()
            QMouseEvent.accept()
            # 改变鼠标样式
            self.setCursor(QCursor(Qt.CursorShape.OpenHandCursor))

    # 拖动移动
    def mouseMoveEvent(self, QMouseEvent):
        self.move(QMouseEvent.globalPos() - self.pos_first)
        QMouseEvent.accept()

    # 开线程放音乐，避免阻断主流程，实现可以同时放多个radio
    def play_radio(self, path):
        t = threading.Thread(target=playsound.playsound, args=(path,))
        t.start()
    # 判断是社么文字
    def set_char(self, ch):
        if ch is None:
            return
        if ch in self.ch2audio:
            self.play_radio(self.ch2audio[ch])
        if ch == "j" or ch == "J":
            ch = "只因"
        if ch == "ctrl_l":
            ch = "你干嘛"
        # 设置字母
        if len(ch) == 1:
            # 显示字母
            font = QFont()
            font.setFamily("微软雅黑")
            font.setPixelSize(35)
            font.setBold(True)
            self.lab_content.setFont(font)
            self.lab_content.setStyleSheet("color:black;")
            self.lab_content.move(40, 50)
        else:
            # 显示字母
            font = QFont()
            font.setFamily("微软雅黑")
            font.setPixelSize(25)
            font.setBold(True)
            self.lab_content.setFont(font)
            self.lab_content.setStyleSheet("color:black;")
            self.lab_content.move(24, 50)
        self.lab_content.setText(ch)
        self.lab_content.adjustSize()
        # 张嘴
        self.lab.setPixmap(QPixmap(resource_path(os.path.join("imgs", "cai2.png"))))

    #  特定按钮
    def init_monitor(self):
        def on_activate_ctrl_j():
            self.play_radio(self.ch2audio['jntm'])

        h = GlobalHotKeys({
            '<ctrl>+j': on_activate_ctrl_j,
        })
        h.start()
    # 监测全部键盘
    def init_monitor_all(self):
        def on_press(key):
            '按下按键时执行。'
            try:
                ch = key.char
            except AttributeError:
                ch = key.name
            # 通过属性判断按键类型。
            self.set_char(ch)

        def on_release(key):
            '松开按键时执行。'
            self.lab.setPixmap(QPixmap(resource_path(os.path.join("imgs", "cai1.png"))))

        # Collect events until released
        self.listener = Listener(
            on_press=on_press,
            on_release=on_release)
        self.listener.start()

    # 长时间没有触发则要回归到最初状态
    def reset_char(self):
        # 清除文字
        self.lab_content.setText("")
        self.lab_content.adjustSize()
        # 闭嘴
        self.lab.setPixmap(QPixmap(resource_path(os.path.join("imgs", "cai1.png"))))

    def quit(self):
        self.close()
        sys.exit()
    # 版本提示
    def version_content(self):
        QMessageBox.information(self, "坤音键盘v1.0", "B站：政函数_",
                                QMessageBox.StandardButton.Yes)
    # 弹出提示
    def open_qq_group(self):
        QDesktopServices.openUrl(QUrl('https://space.bilibili.com/1519207016?spm_id_from=333.1007.0.0'))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
