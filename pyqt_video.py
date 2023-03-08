import cv2
from PyQt5.QtGui import QImage, QPixmap, QIcon
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QFileDialog, QPushButton
from PyQt5.QtCore import QTimer

class VideoPlayer(QWidget):
    def __init__(self):
        super().__init__()
        #设置窗口大小
        self.initUI()

        # 创建视频播放窗口
        self.video_label = QLabel(self)
        self.video_label.setGeometry(10,10, 960, 540)#（距左，距上，宽度，高度）

        # 创建一个定时器，用于更新视频播放窗口
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)

        # 创建一个VideoCapture对象，用于读取视频文件
        self.capture = None

        # 创建一个按键，用于打开视频文件
        self.open_button = QPushButton('打开', self)
        self.open_button.clicked.connect(self.open_video)

    def initUI(self):
        # 设置主窗口的大小
        self.setFixedSize(980, 560)
        #  icon and background
        self.setWindowTitle(" AI奇异果🥝 ")  #窗口名称
        self.setWindowIcon(QIcon("img/JNTM.jpg"))  #logo

    def open_video(self):
        # 打开视频文件，获取文件名
        filename, _ = QFileDialog.getOpenFileName(self, '打开视频', '', '视频文件 (*.mp4 *.avi)')

        if filename:
            # 创建一个VideoCapture对象，用于读取视频文件
            self.capture = cv2.VideoCapture(filename)

            # 启动定时器，开始更新视频播放窗口
            self.timer.start(40)  # 25帧每秒

    def update_frame(self):
        # 读取视频的下一帧
        ret, frame = self.capture.read()

        if ret:
            # 将OpenCV的图像转换为QImage格式
            height, width, channel = frame.shape
            bytes_per_line = 3 * width
            image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(image)

            # 在视频播放窗口中显示图像
            self.video_label.setPixmap(pixmap)
            self.video_label.setScaledContents(True)
        else:
            # 视频读取结束，停止定时器
            self.timer.stop()

            # 释放VideoCapture对象
            self.capture.release()

if __name__ == '__main__':
    app = QApplication([])
    player = VideoPlayer()
    player.show()
    app.exec_()
