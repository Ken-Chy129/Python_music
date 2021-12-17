# coding:utf-8
import os
import re
import webbrowser
from os.path import exists

import jieba
import matplotlib.pyplot as plt
import numpy as np
import pymysql
import requests
import xlsxwriter
from PIL import Image
from PyQt5 import QtCore, QtWidgets
import sys
import qtawesome
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtGui import QIcon, QPalette, QBrush, QPixmap, QFont
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QDialog, QFrame, QVBoxLayout, QLineEdit, QGraphicsOpacityEffect, \
    QPushButton
from bs4 import BeautifulSoup
from wordcloud import WordCloud

class MainUi(QtWidgets.QMainWindow, QDialog):

    def __init__(self, username):
        super().__init__()
        self.username = username
        self.hot = []
        self.player = QMediaPlayer(self)
        self.playing = False
        self.play_index_now = -1
        self.timer = QtCore.QTimer()
        self.timer.setInterval(1000)
        self.timer.start()
        self.timer.timeout.connect(self.check_music_status)
        self.init_ui()

    def init_ui(self):
        self.setFixedSize(960, 700)
        self.setWindowTitle('Ken-Chy')
        self.setWindowIcon(QIcon('favicon.ico'))  # 设置窗体图标
        self.setWindowOpacity(0.9)  # 设置窗口透明度
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置窗口背景透明
        # self.setWindowFlags(QtCore.Qt.FramelessWindowHint) # 隐藏边框

        self.main_widget = QtWidgets.QWidget()  # 创建窗口主部件
        self.main_layout = QtWidgets.QGridLayout()  # 创建主部件的网格布局
        self.main_widget.setLayout(self.main_layout)  # 设置窗口主部件布局为网格布局
        self.left_widget = QtWidgets.QWidget()  # 创建左侧部件
        self.left_widget.setObjectName('left_widget')
        self.left_layout = QtWidgets.QGridLayout()  # 创建左侧部件的网格布局层
        self.left_widget.setLayout(self.left_layout)  # 设置左侧部件布局为网格
        self.right_widget = QtWidgets.QWidget()  # 创建右侧部件
        self.right_widget.setObjectName('right_widget')
        self.right_layout = QtWidgets.QGridLayout()
        self.right_widget.setLayout(self.right_layout)  # 设置右侧部件布局为网格
        self.setCentralWidget(self.main_widget)  # 设置窗口主部件
        self.main_layout.addWidget(self.left_widget, 0, 0, 12, 2)  # 左侧部件在第0行第0列
        self.main_layout.addWidget(self.right_widget, 0, 2, 12, 10)  # 右侧部件在第0行第3列

        self.left_close = QtWidgets.QPushButton("")  # 关闭按钮
        self.left_visit = QtWidgets.QPushButton("")  # 空白按钮
        self.left_mini = QtWidgets.QPushButton("")  # 最小化按钮

        self.left_label_1 = QtWidgets.QPushButton("每日推荐")
        self.left_label_1.setObjectName('left_label')
        self.left_label_2 = QtWidgets.QPushButton("我的音乐")
        self.left_label_2.setObjectName('left_label')
        self.left_label_3 = QtWidgets.QPushButton("联系与帮助")
        self.left_label_3.setObjectName('left_label')

        self.left_button_1 = QtWidgets.QPushButton(qtawesome.icon('fa.music', color='white'), "热门歌曲")
        self.left_button_1.setObjectName('left_button')
        self.left_button_2 = QtWidgets.QPushButton(qtawesome.icon('fa.sellsy', color='white'), "热门歌手")
        self.left_button_2.setObjectName('left_button')
        self.left_button_3 = QtWidgets.QPushButton(qtawesome.icon('fa.area-chart', color='white'), "数据分析")
        self.left_button_3.setObjectName('left_button')
        self.left_button_4 = QtWidgets.QPushButton(qtawesome.icon('fa.cloud-download', color='white'), "我的下载")
        self.left_button_4.setObjectName('left_button')
        self.left_button_5 = QtWidgets.QPushButton(qtawesome.icon('fa.star', color='white'), "我的收藏")
        self.left_button_5.setObjectName('left_button')
        self.left_button_6 = QtWidgets.QPushButton(qtawesome.icon('fa.exchange', color='white'), "切换账号")
        self.left_button_6.setObjectName('left_button')
        self.left_button_7 = QtWidgets.QPushButton(qtawesome.icon('fa.comment', color='white'), "开发流程")
        self.left_button_7.setObjectName('left_button')
        self.left_button_8 = QtWidgets.QPushButton(qtawesome.icon('fa.home', color='white'), "作者博客")
        self.left_button_8.setObjectName('left_button')
        self.left_button_9 = QtWidgets.QPushButton(qtawesome.icon('fa.comments', color='white'), "联系作者")
        self.left_button_9.setObjectName('left_button')

        self.left_layout.addWidget(self.left_mini, 0, 0, 1, 1)
        self.left_layout.addWidget(self.left_close, 0, 2, 1, 1)
        self.left_layout.addWidget(self.left_visit, 0, 1, 1, 1)
        self.left_layout.addWidget(self.left_label_1, 1, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_1, 2, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_2, 3, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_3, 4, 0, 1, 3)
        self.left_layout.addWidget(self.left_label_2, 5, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_4, 6, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_5, 7, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_6, 8, 0, 1, 3)
        self.left_layout.addWidget(self.left_label_3, 9, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_7, 10, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_8, 11, 0, 1, 3)
        self.left_layout.addWidget(self.left_button_9, 12, 0, 1, 3)

        self.right_bar_widget = QtWidgets.QWidget()  # 右侧顶部搜索框部件
        self.right_bar_layout = QtWidgets.QGridLayout()  # 右侧顶部搜索框网格布局
        self.right_bar_widget.setLayout(self.right_bar_layout)
        self.search_icon = QtWidgets.QLabel(chr(0xf002) + ' ' + '搜索  ')
        self.search_icon.setFont(qtawesome.font('fa', 20))
        self.right_bar_widget_search_input = QtWidgets.QLineEdit()
        self.right_bar_widget_search_input.setPlaceholderText("输入歌手、歌曲或用户，回车进行搜索")

        self.right_bar_layout.addWidget(self.search_icon, 0, 0, 1, 1)
        self.right_bar_layout.addWidget(self.right_bar_widget_search_input, 0, 1, 1, 8)
        self.right_layout.addWidget(self.right_bar_widget, 0, 0, 1, 9)

        self.right_search_result_lable = QtWidgets.QLabel("搜索结果")
        self.right_search_result_lable.setObjectName('right_lable')
        self.right_operator_lable = QtWidgets.QLabel("执行操作")
        self.right_operator_lable.setObjectName('right_lable')

        self.right_search_result_widget = QtWidgets.QWidget()  # 搜索歌曲部件
        self.right_search_result_layout = QtWidgets.QGridLayout()  # 搜索歌曲部件网格布局
        self.right_search_result_widget.setLayout(self.right_search_result_layout)

        self.search_result_button_1 = QtWidgets.QPushButton()
        self.search_result_button_2 = QtWidgets.QPushButton()
        self.search_result_button_3 = QtWidgets.QPushButton()
        self.search_result_button_4 = QtWidgets.QPushButton()
        self.search_result_button_5 = QtWidgets.QPushButton()
        self.search_result_button_6 = QtWidgets.QPushButton()
        self.search_result_button_7 = QtWidgets.QPushButton()
        self.search_result_button_8 = QtWidgets.QPushButton()
        self.search_result_button_9 = QtWidgets.QPushButton()
        self.search_result_button_10 = QtWidgets.QPushButton()
        self.right_search_result_layout.addWidget(self.search_result_button_1, 0, 1, )
        self.right_search_result_layout.addWidget(self.search_result_button_2, 1, 1, )
        self.right_search_result_layout.addWidget(self.search_result_button_3, 2, 1, )
        self.right_search_result_layout.addWidget(self.search_result_button_4, 3, 1, )
        self.right_search_result_layout.addWidget(self.search_result_button_5, 4, 1, )
        self.right_search_result_layout.addWidget(self.search_result_button_6, 5, 1, )
        self.right_search_result_layout.addWidget(self.search_result_button_7, 6, 1, )
        self.right_search_result_layout.addWidget(self.search_result_button_8, 7, 1, )
        self.right_search_result_layout.addWidget(self.search_result_button_9, 8, 1, )
        self.right_search_result_layout.addWidget(self.search_result_button_10, 9, 1, )
        self.search("陈奕迅")

        self.right_operator_widget = QtWidgets.QWidget()  # 播放歌单部件
        self.right_operator_layout = QtWidgets.QGridLayout()  # 播放歌单网格布局
        self.right_operator_widget.setLayout(self.right_operator_layout)

        self.operator_button_1 = QtWidgets.QToolButton()
        self.operator_button_1.setText("导出所有歌曲信息")
        self.operator_button_1.setIcon(qtawesome.icon('fa.list', color='red'))
        self.operator_button_1.setIconSize(QtCore.QSize(50, 50))
        self.operator_button_1.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)

        self.operator_button_2 = QtWidgets.QToolButton()
        self.operator_button_2.setText("导出所有歌曲歌词")
        self.operator_button_2.setIcon(qtawesome.icon('fa.file-text-o', color='red'))
        self.operator_button_2.setIconSize(QtCore.QSize(50, 50))
        self.operator_button_2.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)

        self.operator_button_3 = QtWidgets.QToolButton()
        self.operator_button_3.setText("下载当前播放歌曲")
        self.operator_button_3.setIcon(qtawesome.icon('fa.download', color='red'))
        self.operator_button_3.setIconSize(QtCore.QSize(50, 50))
        self.operator_button_3.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)

        self.operator_button_4 = QtWidgets.QToolButton()
        self.operator_button_4.setText("收藏当前播放歌曲")
        self.operator_button_4.setIcon(qtawesome.icon('fa.heart', color='red'))
        self.operator_button_4.setIconSize(QtCore.QSize(50, 50))
        self.operator_button_4.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)

        self.operator_button_5 = QtWidgets.QToolButton()
        self.operator_button_5.setText("生成所有歌词词云")
        self.operator_button_5.setIcon(qtawesome.icon('fa.cloud', color='red'))
        self.operator_button_5.setIconSize(QtCore.QSize(50, 50))
        self.operator_button_5.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)

        self.operator_button_6 = QtWidgets.QToolButton()
        self.operator_button_6.setText("热门歌手歌曲占比")
        self.operator_button_6.setIcon(qtawesome.icon('fa.pie-chart', color='red'))
        self.operator_button_6.setIconSize(QtCore.QSize(50, 50))
        self.operator_button_6.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)

        self.right_operator_layout.addWidget(self.operator_button_1, 0, 0)
        self.right_operator_layout.addWidget(self.operator_button_2, 0, 1)
        self.right_operator_layout.addWidget(self.operator_button_3, 1, 0)
        self.right_operator_layout.addWidget(self.operator_button_4, 1, 1)
        self.right_operator_layout.addWidget(self.operator_button_5, 2, 0)
        self.right_operator_layout.addWidget(self.operator_button_6, 2, 1)

        self.right_layout.addWidget(self.right_search_result_lable, 2, 0, 1, 5)
        self.right_layout.addWidget(self.right_operator_lable, 2, 5, 1, 3)
        self.right_layout.addWidget(self.right_search_result_widget, 3, 0, 1, 5)
        self.right_layout.addWidget(self.right_operator_widget, 3, 5, 1, 3)

        self.right_process_bar = QtWidgets.QProgressBar()  # 播放进度部件
        self.process_value = 0
        self.right_process_bar.setValue(self.process_value)
        self.right_process_bar.setFixedHeight(3)  # 设置进度条高度
        self.right_process_bar.setTextVisible(False)  # 不显示进度条文字

        self.right_playconsole_widget = QtWidgets.QWidget()  # 播放控制部件
        self.right_playconsole_layout = QtWidgets.QGridLayout()  # 播放控制部件网格布局层
        self.right_playconsole_widget.setLayout(self.right_playconsole_layout)

        self.console_button_1 = QtWidgets.QPushButton(qtawesome.icon('fa.backward', color='#F76677'), "")
        self.console_button_2 = QtWidgets.QPushButton(qtawesome.icon('fa.forward', color='#F76677'), "")
        self.console_button_3 = QtWidgets.QPushButton(qtawesome.icon('fa.play', color='#F76677', font=18), "")
        self.console_button_3.setIconSize(QtCore.QSize(30, 30))

        self.right_playconsole_layout.addWidget(self.console_button_1, 0, 0)
        self.right_playconsole_layout.addWidget(self.console_button_2, 0, 2)
        self.right_playconsole_layout.addWidget(self.console_button_3, 0, 1)
        self.right_playconsole_layout.setAlignment(QtCore.Qt.AlignCenter)  # 设置布局内部件居中显示

        self.right_layout.addWidget(self.right_process_bar, 9, 0, 1, 9)
        self.right_layout.addWidget(self.right_playconsole_widget, 10, 0, 1, 9)

        self.left_close.setFixedSize(15, 15)  # 设置关闭按钮的大小
        self.left_visit.setFixedSize(15, 15)  # 设置按钮大小
        self.left_mini.setFixedSize(15, 15)  # 设置最小化按钮大小

        self.main_layout.setSpacing(0)  # 设置内部控件间距

        self.left_close.setStyleSheet(
            '''QPushButton{background:#F76677;border-radius:5px;}QPushButton:hover{background:red;}''')
        self.left_visit.setStyleSheet(
            '''QPushButton{background:#F7D674;border-radius:5px;}QPushButton:hover{background:yellow;}''')
        self.left_mini.setStyleSheet(
            '''QPushButton{background:#6DDF6D;border-radius:5px;}QPushButton:hover{background:green;}''')

        self.left_widget.setStyleSheet("\
            QPushButton{border:none;color:white;}\
            QPushButton#left_label{\
                border:none;\
                border-bottom:1px solid white;\
                font-size:18px;\
                font-weight:700;\
                font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;\
            }\
            QPushButton#left_button:hover{border-left:4px solid red;font-weight:700;}\
            QWidget#left_widget{\
                background:gray;\
                border-top:1px solid white;\
                border-bottom:1px solid white;\
                border-left:1px solid white;\
                border-top-left-radius:10px;\
                border-bottom-left-radius:10px;\
            }")

        self.right_bar_widget_search_input.setStyleSheet(
            "QLineEdit{\
                border:1px solid gray;\
                width:300px;\
                border-radius:10px;\
                padding:8px 4px;\
        }")

        self.right_widget.setStyleSheet('''
            QWidget#right_widget{
                color:#232C51;
                background:white;
                border-top:1px solid darkGray;
                border-bottom:1px solid darkGray;
                border-right:1px solid darkGray;
                border-top-right-radius:10px;
                border-bottom-right-radius:10px;
            }
            QLabel#right_lable{
                border:none;
                font-size:20px;
                font-weight:700;
                font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
                text-align:center
            }
        ''')

        self.right_operator_widget.setStyleSheet(
            '''
                QToolButton{border:none; margin-left:15px}
                QToolButton:hover{border-bottom:2px solid #F76677;}
            ''')

        self.right_search_result_widget.setStyleSheet('''
            QPushButton{
                border:none;
                color:gray;
                font-size:18px;
                height:36px;
                padding-left:5px;
                padding-right:10px;
                text-align:left;
            }
            QPushButton:hover{
                color:black;
                border:1px solid #F3F3F5;
                border-radius:10px;
                background:LightGray;
            }
        ''')

        self.right_process_bar.setStyleSheet('''
            QProgressBar::chunk {
                background-color: #F76677;
            }
        ''')

        self.right_playconsole_widget.setStyleSheet('''
            QPushButton{
                border:none;
            }
        ''')

        self.left_button_1.clicked.connect(self.pop_songs)
        self.left_button_2.clicked.connect(self.pop_singers)
        self.left_button_3.clicked.connect(self.analysis)
        self.left_button_4.clicked.connect(self.my_downloads)
        self.left_button_5.clicked.connect(self.my_collects)
        self.left_button_6.clicked.connect(self.change_account)
        self.left_button_7.clicked.connect(lambda: webbrowser.open('https://blog.csdn.net/qq_25046827'))
        self.left_button_8.clicked.connect(lambda: webbrowser.open('https://blog.csdn.net/qq_25046827'))
        self.left_button_9.clicked.connect(lambda: webbrowser.open('https://blog.csdn.net/qq_25046827'))
        self.right_bar_widget_search_input.returnPressed.connect(
            lambda: self.search(self.right_bar_widget_search_input.text()))
        self.search_result_button_1.clicked.connect(lambda: self.play_music(0))
        self.search_result_button_2.clicked.connect(lambda: self.play_music(1))
        self.search_result_button_3.clicked.connect(lambda: self.play_music(2))
        self.search_result_button_4.clicked.connect(lambda: self.play_music(3))
        self.search_result_button_5.clicked.connect(lambda: self.play_music(4))
        self.search_result_button_6.clicked.connect(lambda: self.play_music(5))
        self.search_result_button_7.clicked.connect(lambda: self.play_music(6))
        self.search_result_button_8.clicked.connect(lambda: self.play_music(7))
        self.search_result_button_9.clicked.connect(lambda: self.play_music(8))
        self.search_result_button_10.clicked.connect(lambda: self.play_music(9))
        self.operator_button_1.clicked.connect(lambda: self.export_songs_details())
        self.operator_button_2.clicked.connect(lambda: self.export_songs_lyric())
        self.operator_button_3.clicked.connect(lambda: self.download())
        self.operator_button_4.clicked.connect(lambda: self.collect())
        self.operator_button_5.clicked.connect(lambda: self.lyric_cloud())
        self.operator_button_6.clicked.connect(lambda: self.hot_singer_song())
        self.console_button_1.clicked.connect(self.pre_music)
        self.console_button_3.clicked.connect(self.play_music_by_button)
        self.console_button_2.clicked.connect(self.next_music)

    def search(self, keyword):
        self.play_index_now = -1  # 每次重新搜索都将当前播放序号设置为-1
        urlbase = r'https://www.8lrc.com/search'  # 搜索的基础地址
        params = {'key': keyword}  # 封装搜索的参数
        res_body = requests.get(urlbase, params)  # 拼接url，发送请求
        soup_body = BeautifulSoup(res_body.text, 'html.parser')  # html解析获得响应文本
        self.tags = soup_body.findAll(class_='tGequ')  # 得到查询结果
        self.get_song_detail(keyword)

    def get_song_detail(self, keyword):  # 呈现搜索结果于界面
        result = r'https://www.8lrc.com'  # 搜索结果的基础地址
        pattern = r'(.*) - (.*)'  # 得到歌名的正则表达式
        pattern1 = r'"url":"([^"]*)"'  # 得到歌曲资源的正则表达式
        self.keyword = keyword
        self.names = []
        self.musics = []
        self.num = 0
        for tag in self.tags[0:]:
            if re.match(pattern, tag.text):
                res_body = requests.get(result + tag['href'])
                soup_body = BeautifulSoup(res_body.text, 'html.parser')
                if soup_body.text.__contains__("404"): continue
                script = soup_body.select("body script")[3].get_text()
                pre_music = re.search(pattern1, script).group(1)
                self.names.append(re.split(pattern, tag.text)[1])  # 获取歌名
                self.musics.append(pre_music.replace(r'\/', '/'))  # 获取歌曲资源
                self.num = self.num+1
        self.song_show()

    def song_show(self):  # 呈现"歌手-歌名"的形式
        num = self.num
        if self.num:
            self.search_result_button_1.setText(self.keyword + " - " + self.names[0])
            self.num = self.num-1
        else:
            self.search_result_button_1.setText("")
        if self.num:
            self.search_result_button_2.setText(self.keyword + " - " + self.names[1])
            self.num = self.num-1
        else:
            self.search_result_button_2.setText("")
        if self.num:
            self.search_result_button_3.setText(self.keyword + " - " + self.names[2])
            self.num = self.num-1
        else:
            self.search_result_button_3.setText("")
        if self.num:
            self.search_result_button_4.setText(self.keyword + " - " + self.names[3])
            self.num = self.num-1
        else:
            self.search_result_button_4.setText("")
        if self.num:
            self.search_result_button_5.setText(self.keyword + " - " + self.names[4])
            self.num = self.num-1
        else:
            self.search_result_button_5.setText("")
        if self.num:
            self.search_result_button_6.setText(self.keyword + " - " + self.names[5])
            self.num = self.num-1
        else:
            self.search_result_button_6.setText("")
        if self.num:
            self.search_result_button_7.setText(self.keyword + " - " + self.names[6])
            self.num = self.num-1
        else:
            self.search_result_button_7.setText("")
        if self.num:
            self.search_result_button_8.setText(self.keyword + " - " + self.names[7])
            self.num = self.num-1
        else:
            self.search_result_button_8.setText("")
        if self.num:
            self.search_result_button_9.setText(self.keyword + " - " + self.names[8])
            self.num = self.num-1
        else:
            self.search_result_button_9.setText("")
        if self.num:
            self.search_result_button_10.setText(self.keyword + " - " + self.names[9])
        else:
            self.search_result_button_10.setText("")
        self.num = num

    def process_timer_status(self):  # 进度条进程百分比更新
        try:
            if self.playing is True:
                self.process_value += (100 / (self.duration / 1000))
                # print("当前进度：", self.process_value)
                self.right_process_bar.setValue(self.process_value)
        except Exception as e:
            print(repr(e))

    def check_music_status(self):  # 确认播放咋黄台，播放结束则自动播放下一首
        player_status = self.player.mediaStatus()
        player_duration = self.player.duration()
        # print("音乐时间：",player_duration)
        # print("当前播放器状态",player_status)
        if player_status == 7:
            if not self.play_index_now >= 9:
                self.next_music()

        if player_duration > 0:
            self.duration = player_duration

    def play_music(self, num):  # 播放歌曲
        if num >= self.num:
            msg_box = QMessageBox(QMessageBox.Warning, '温馨提示', '暂无该曲目')
            msg_box.exec_()
            return
        self.process_value = 0
        self.play_index_now = num
        self.playing = True
        self.console_button_3.setIcon(qtawesome.icon('fa.stop', color='#F76677', font=18))
        self.player.setMedia(QMediaContent(QUrl(self.musics[num])))
        self.player.setVolume(50)
        self.player.play()
        self.duration = self.player.duration()  # 音乐的时长
        # print(self.duration)
        self.process_timer = QtCore.QTimer()
        self.process_timer.setInterval(1000)
        self.process_timer.start()
        self.process_timer.timeout.connect(self.process_timer_status)

    def play_music_by_button(self):  # 播放器三个按钮功能设置
        if self.play_index_now == -1:
            if self.playing is False:
                self.process_value = 0
                self.play_music(0)
                self.console_button_3.setIcon(qtawesome.icon('fa.stop', color='#F76677', font=18))
        elif self.playing is False:
            self.playing = True
            self.console_button_3.setIcon(qtawesome.icon('fa.stop', color='#F76677', font=18))
            self.player.play()
        else:
            self.playing = False
            self.console_button_3.setIcon(qtawesome.icon('fa.play', color='#F76677', font=18))
            self.player.pause()

    def pre_music(self):  # 播放前一首
        if self.play_index_now <= 0:
            msg_box = QMessageBox(QMessageBox.Warning, '温馨提示', '已经是第一首了~')
            msg_box.exec_()
        else:
            self.play_music(self.play_index_now - 1)

    def next_music(self):  # 播放后一首
        if self.play_index_now >= 9:
            msg_box = QMessageBox(QMessageBox.Warning, '温馨提示', '已经是最后一首了~')
            msg_box.exec_()
        else:
            self.play_music(self.play_index_now + 1)

    def export_songs_details(self):
        result = r'https://www.8lrc.com'
        row = 0
        if not exists('./songsdetails/'):
            os.makedirs('./songsdetails/')
        workbook = xlsxwriter.Workbook('./songsdetails/'+self.keyword+'.xlsx')
        worksheet = workbook.add_worksheet('music')
        worksheet.write_row(row, 0, ['歌名', '歌手', '歌曲url', '歌曲资源地址'])
        for name in self.names:
            row += 1
            worksheet.write_row(row, 0, [name.replace(' ', ''), self.keyword, result+self.tags[row-1]['href'], self.musics[row-1]])
        workbook.close()
        if os.path.exists('./songsdetails/'+self.keyword+'.xlsx'):
            os.startfile('.\\songsdetails\\'+self.keyword+'.xlsx')
        else:
            msg_box = QMessageBox(QMessageBox.Warning, '提示', '出了点小问题~')
            msg_box.exec_()

    def export_songs_lyric(self):
        result = r'https://www.8lrc.com'
        pattern = r'"lrc":"(.*)","link"'
        num = 0
        if not exists('./lyric/'+self.keyword):
            os.makedirs('./lyric/'+self.keyword)
        for tag in self.tags[0:10]:
            res_body = requests.get(result + tag['href'])
            soup_body = BeautifulSoup(res_body.text, 'html.parser')
            if soup_body.text.__contains__("404"): continue
            script = soup_body.select("body script")[3].get_text()
            lyric = re.search(pattern, script).group(1)
            lyric = lyric.replace(r'\r\n', '\n')
            with open("lyric/"+self.keyword+'/'+self.names[num]+'.txt', 'w+', -1, 'utf-8') as fp:
                fp.write(lyric)
                fp.close()
                num += 1
        msg_box = QMessageBox(QMessageBox.Warning, '提示', '导出成功')
        msg_box.exec_()
        os.startfile(".\\lyric\\"+self.keyword)

    def download(self):
        if self.play_index_now == -1:
            msg_box = QMessageBox(QMessageBox.Warning, '温馨提示', '当前暂无播放歌曲')
            msg_box.exec_()
            return
        response = requests.get(self.musics[self.play_index_now])
        filename = QFileDialog.getSaveFileName(self, '下载文件', '.', '音乐文件(*.MP3)')  # 保存歌曲
        if filename[0] != '':
            try:
                conn = pymysql.connect(host='localhost', user='root', password='129496', db='pyhomework')
                cur = conn.cursor()
            except:
                msg_box = QMessageBox(QMessageBox.Warning, '温馨提示', '数据库连接错误')
                msg_box.exec_()
                return

            sql = 'insert into downloads values("%s","%s", "%s", "%s")' % (
            self.username, self.keyword, self.names[self.play_index_now], self.musics[self.play_index_now])
            try:
                cur.execute(sql)
                conn.commit()
                msg_box = QMessageBox(QMessageBox.Warning, '提示', '下载成功')
                msg_box.exec_()
            except:
                conn.rollback()
                msg_box = QMessageBox(QMessageBox.Warning, '温馨提示', '下载出错')
                msg_box.exec_()
            cur.close()
            conn.close()

            with open(filename[0], 'wb') as m:
                m.write(response.content)

    def collect(self):
        if self.play_index_now == -1:
            msg_box = QMessageBox(QMessageBox.Warning, '温馨提示', '当前暂无播放歌曲')
            msg_box.exec_()
            return
        try:
            conn = pymysql.connect(host='localhost', user='root', password='129496', db='pyhomework')
            cur = conn.cursor()
        except:
            msg_box = QMessageBox(QMessageBox.Warning, '温馨提示', '数据库连接错误')
            msg_box.exec_()
            return

        sql = 'insert into collects values("%s","%s", "%s", "%s")' % (self.username, self.keyword, self.names[self.play_index_now], self.musics[self.play_index_now])
        try:
            cur.execute(sql)
            conn.commit()
            msg_box = QMessageBox(QMessageBox.Warning, '提示', '收藏成功')
            msg_box.exec_()
        except:
            conn.rollback()
            msg_box = QMessageBox(QMessageBox.Warning, '温馨提示', '收藏出错')
            msg_box.exec_()
        cur.close()
        conn.close()

    def lyric_cloud(self):
        result = r'https://www.8lrc.com'
        pattern = r'"lrc":"(.*)","link"'
        lyric = ""
        for tag in self.tags[0:10]:
            res_body = requests.get(result + tag['href'])
            soup_body = BeautifulSoup(res_body.text, 'html.parser')
            if soup_body.text.__contains__("404"): continue
            script = soup_body.select("body script")[3].get_text()
            lyric = lyric + re.search(pattern, script).group(1)
        text = re.findall('[\u4e00-\u9fa5]+', lyric, re.S)  # 提取中文
        text = " ".join(text)
        word = jieba.cut(text, cut_all=True)  # 分词
        new_word = []
        for i in word:
            if len(i) >= 2:
                new_word.append(i)  # 只添加长度大于2的词
        final_text = " ".join(new_word)
        mask = np.array(Image.open("2.jpg"))
        word_cloud = WordCloud(background_color="white", width=800, height=600, max_words=100, max_font_size=80, contour_width=1, contour_color='lightblue', font_path="C:/Windows/Fonts/simfang.ttf", mask=mask).generate(final_text)
        # image_color = ImageColorGenerator(mask)
        # plt.imshow(word_cloud, interpolation="bilinear")
        # plt.axis("off")
        # plt.show()
        word_cloud.to_file(self.keyword+'词云.png')
        os.startfile(self.keyword+'词云.png')

    def hot_singer_song(self):
        url = 'https://www.9ku.com/geshou/all-all-liuxing.htm'
        base = 'https://www.9ku.com'
        singers_url = []
        songs_num = []
        proportion = []
        name = []
        all_num = 0
        res_body = requests.get(url)
        soup_body = BeautifulSoup(res_body.text, 'html.parser')
        singers_body = soup_body.findAll(class_='t-i')
        for singer in singers_body[:10]:
            singers_url.append(base + singer['href'])
        for singer_url in singers_url:
            res_body = requests.get(singer_url)
            soup_body = BeautifulSoup(res_body.text, 'html.parser')
            name.append(soup_body.find(class_="t-t clearfix").h1.text)
            songs = soup_body.findAll(class_="songNameA")
            songs_num.append(len(songs))
            all_num += len(songs)
        for i in songs_num:
            proportion.append(i/all_num)
        explode = [0.1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        plt.figure(figsize=(6, 9))  # 设置图形大小宽高
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 解决中文乱码问题
        plt.axes(aspect=1)  # 设置图形是圆的
        plt.pie(x=proportion, labels=name, explode=explode, autopct='%3.1f %%',
                shadow=True, labeldistance=1.2, startangle=0, pctdistance=0.8)
        plt.title("热门歌手歌曲量占比")
        # plt.show()
        plt.savefig("热门歌手歌曲量占比饼图.jpg")
        os.startfile("热门歌手歌曲量占比饼图.jpg")

    def pop_songs(self):
        row = 0
        base = 'http://m.yue365.com/'
        url = 'http://m.yue365.com/bang/box100_w.shtml'
        pattern = r'width:(.*)%'
        self.hot = []
        self.songs = []
        res_body = requests.get(url)
        res_body.encoding = 'gb2312'
        soup_body = BeautifulSoup(res_body.text, 'lxml')
        songs = soup_body.findAll(class_='name')
        hot = soup_body.findAll('span', class_='dib')
        workbook = xlsxwriter.Workbook('popsongs.xlsx')
        first_format = workbook.add_format({'align': 'center'})
        second_format = workbook.add_format({'align': 'left'})
        worksheet = workbook.add_worksheet('pop500')
        worksheet.set_column(0, 0, 6)
        worksheet.set_column(1, 1, 20)
        worksheet.set_column(2, 2, 46)
        worksheet.set_column(3, 3, 10)
        worksheet.write_row(row, 0, ['排名', '歌名', '歌曲url', '歌曲热度'], first_format)
        for song in songs:
            self.hot.append(int(re.split(pattern, hot[row*2+1]['style'])[1]))
            self.songs.append(song.a.text)
            row += 1
            song_url = base+song.a['href']
            worksheet.write_row(row, 0, [row, song.a.text, song_url, self.hot[row-1]], second_format)
        workbook.close()
        os.startfile('popsongs.xlsx')

    def pop_singers(self):
        url = 'https://www.9ku.com/geshou/all-all-liuxing.htm'
        base = 'https://www.9ku.com'
        self.singers_url = []
        res_body = requests.get(url)
        soup_body = BeautifulSoup(res_body.text, 'html.parser')
        singers_body = soup_body.findAll(class_='t-i')
        for singer in singers_body[:50]:
            self.singers_url.append(base + singer['href'])
        self.get_pop_singers_songs()

    def get_pop_singers_songs(self):
        workbook = xlsxwriter.Workbook('popsingers.xlsx')
        url_base = 'https://www.9ku.com'
        msg_box = QMessageBox(QMessageBox.Warning, '温馨提示', '数据量较大，请耐心等待！')
        msg_box.exec_()
        for singer_url in self.singers_url:
            res_body = requests.get(singer_url)
            soup_body = BeautifulSoup(res_body.text, 'html.parser')
            # self.singers_name.append(soup_body.find(class_="t-t clearfix").h1.text)
            name = soup_body.find(class_="t-t clearfix").h1.text
            worksheet = workbook.add_worksheet(name)
            worksheet.write_row(0, 0, ['歌名', '歌曲url', '歌词url'])
            worksheet.set_column(0, 0, 20)
            worksheet.set_column(1, 2, 40)
            songs = soup_body.findAll(class_="songNameA")
            lyrics = soup_body.findAll(class_="chi")
            row = 1
            for song in songs[:-18]:
                worksheet.write_row(row, 0, [song.text, url_base+song['href'], url_base+lyrics[row-1]['href']])
                row += 1
        workbook.close()
        os.startfile('popsingers.xlsx')

    def analysis(self):
        plt.close()
        # 解决中文显示的问题
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False
        x = ('0-10', '10-20', '20-30', '30-40', '40-50', '>50')
        data = [0, 0, 0, 0, 0, 0]
        if len(self.hot) == 0:
            msg_box = QMessageBox(QMessageBox.Warning, '温馨提示', '正在获取热门歌曲')
            msg_box.exec_()
            self.pop_songs()
        for hot in self.hot:
            if int(hot) < 10:
                data[0] += 1
            elif int(hot) < 20:
                data[1] += 1
            elif int(hot) < 30:
                data[2] += 1
            elif int(hot) < 40:
                data[3] += 1
            elif int(hot) < 50:
                data[4] += 1
            else:
                data[5] += 1
        plt.bar(x, data, color='steelblue', alpha=0.8)
        plt.title("pop500歌曲热度")
        plt.xlabel("歌曲热度范围")
        plt.ylabel("歌曲数量")
        plt.show()

    def my_collects(self):
        try:
            conn = pymysql.connect(host='localhost', user='root', password='129496', db='pyhomework')
            cur = conn.cursor()
        except:
            msg_box = QMessageBox(QMessageBox.Warning, '温馨提示', '数据库连接错误')
            msg_box.exec_()
            return

        try:
            sql = 'select * from collects where user="%s"' % (self.username)
            cur.execute(sql)
            conn.commit()
        except:
            msg_box = QMessageBox(QMessageBox.Warning, '错误提示', '系统错误')
            msg_box.exec_()

        row = 0
        collects = cur.fetchall()
        cur.close()
        conn.close()
        workbook = xlsxwriter.Workbook(self.username+'\'s collects.xlsx')
        worksheet = workbook.add_worksheet('music')
        worksheet.write_row(row, 0, ['歌手', '歌名', '歌曲资源地址'])
        for collect in collects:
            row += 1
            worksheet.write_row(row, 0, [collect[1], collect[2], collect[3]])
        workbook.close()
        os.startfile(self.username+'\'s collects.xlsx')

    def my_downloads(self):
        try:
            conn = pymysql.connect(host='localhost', user='root', password='129496', db='pyhomework')
            cur = conn.cursor()
        except:
            msg_box = QMessageBox(QMessageBox.Warning, '温馨提示', '数据库连接错误')
            msg_box.exec_()
            return

        try:
            sql = 'select * from downloads where user="%s"' % (self.username)
            cur.execute(sql)
            conn.commit()
        except:
            msg_box = QMessageBox(QMessageBox.Warning, '错误提示', '系统错误')
            msg_box.exec_()

        row = 0
        collects = cur.fetchall()
        cur.close()
        conn.close()
        workbook = xlsxwriter.Workbook(self.username + '\'s downloads.xlsx')
        worksheet = workbook.add_worksheet('music')
        worksheet.write_row(row, 0, ['歌手', '歌名', '歌曲资源地址'])
        for collect in collects:
            row += 1
            worksheet.write_row(row, 0, [collect[1], collect[2], collect[3]])
        workbook.close()
        os.startfile(self.username + '\'s downloads.xlsx')

    def change_account(self):
        self.close()
        dialog = LoginDialog()
        if dialog.exec_() == QDialog.Accepted:
            gui = MainUi(dialog.get_username())
            gui.show()


class LoginDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle('登录')
        self.setWindowIcon(QIcon('favicon.ico'))
        self.setFixedSize(960, 700)
        self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)

        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap('1.jpg')))
        self.setPalette(palette)

        # 设置界面控件
        self.frame = QFrame(self)
        self.frame.move(260, 110)
        self.mainLayout = QVBoxLayout(self.frame)

        self.nameEd1 = QLineEdit(self)
        self.nameEd1.setPlaceholderText("Admin")
        self.nameEd1.setFont(QFont('微软雅黑', 22))
        op2 = QGraphicsOpacityEffect()
        op2.setOpacity(0.5)
        self.nameEd1.setGraphicsEffect(op2)
        self.nameEd1.setStyleSheet('''QLineEdit{border-radius:5px; padding: 8px}''')

        self.nameEd2 = QLineEdit(self)
        self.nameEd2.setPlaceholderText("Password")
        self.nameEd2.setFont(QFont('微软雅黑', 22))
        self.nameEd2.setEchoMode(QLineEdit.Password)
        op5 = QGraphicsOpacityEffect()
        op5.setOpacity(0.5)
        self.nameEd2.setGraphicsEffect(op5)
        self.nameEd2.setStyleSheet('''QLineEdit{border-radius:5px; padding: 8px}''')

        self.btnLG = QPushButton('Login')
        op3 = QGraphicsOpacityEffect()
        op3.setOpacity(0.5)
        self.btnLG.setGraphicsEffect(op3)
        self.btnLG.setStyleSheet(
            '''QPushButton{background:#1E90FF;border-radius:5px;}QPushButton:hover{background:#4169E1;}\
            QPushButton{font-family:'Arial';color:#FFFFFF; padding:6px}''')

        self.btnRG = QPushButton('Register')
        op3 = QGraphicsOpacityEffect()
        op3.setOpacity(0.5)
        self.btnRG.setGraphicsEffect(op3)
        self.btnRG.setStyleSheet(
            '''QPushButton{background:#1E90FF;border-radius:5px;}QPushButton:hover{background:#4169E1;}\
            QPushButton{font-family:'Arial';color:#FFFFFF; padding:6px}''')
        #
        self.btnLG.setFont(QFont('Microsoft YaHei', 22))
        self.btnRG.setFont(QFont('Microsoft YaHei', 22))

        self.mainLayout.addWidget(self.nameEd1)
        self.mainLayout.addWidget(self.nameEd2)
        self.mainLayout.addWidget(self.btnLG)
        self.mainLayout.addWidget(self.btnRG)

        self.mainLayout.setSpacing(60)

        # 绑定按钮事件
        self.btnLG.clicked.connect(self.login)
        self.btnRG.clicked.connect(self.register)

    def login(self, event):  # 登录
        username = self.nameEd1.text()
        password = self.nameEd2.text()
        if username == "" or password == "":
            msg_box = QMessageBox(QMessageBox.Warning, '温馨提示', '请输入用户名和密码')
            msg_box.exec_()
            return

        try:
            conn = pymysql.connect(host='localhost', user='root', password='129496', db='pyhomework')
            cur = conn.cursor()
        except:
            msg_box = QMessageBox(QMessageBox.Warning, '温馨提示', '数据库连接错误')
            msg_box.exec_()
            return

        try:
            sql = 'select * from users where username="%s"' % (username)
            cur.execute(sql)
            conn.commit()
        except:
            msg_box = QMessageBox(QMessageBox.Warning, '错误提示', '系统错误')
            msg_box.exec_()
            cur.close()
            conn.close()
            return

        user = cur.fetchone()
        cur.close()
        conn.close()
        if user is None:
            msg_box = QMessageBox(QMessageBox.Warning, '错误提示', '该用户不存在')
            msg_box.exec_()
            self.nameEd1.setText("")
            self.nameEd2.setText("")
            return

        if username == user[0] and password == user[1]:
            msg_box = QMessageBox(QMessageBox.Warning, '恭喜', '登陆成功')
            msg_box.exec_()
            self.username = username
            self.accept()

        else:
            msg_box = QMessageBox(QMessageBox.Warning, '错误提示', '用户名或者密码错误')
            msg_box.exec_()
            self.nameEd1.setText("")
            self.nameEd2.setText("")
            return

    def register(self, event):  # 注册
        username = self.nameEd1.text()
        password = self.nameEd2.text()
        if username == "" or password == "":
            msg_box = QMessageBox(QMessageBox.Warning, '温馨提示', '用户名和密码不能为空')
            msg_box.exec_()
            return

        if len(username) > 10 or len(password) > 16:
            msg_box = QMessageBox(QMessageBox.Warning, '温馨提示', '用户名或密码过长')
            msg_box.exec_()
            return

        try:
            conn = pymysql.connect(host='localhost', user='root', password='129496', db='pyhomework')
            cur = conn.cursor()
        except:
            msg_box = QMessageBox(QMessageBox.Warning, '错误提示', '数据库连接失败')
            msg_box.exec_()
            return

        sql = 'insert into users values("%s","%s")' % (username, password)
        try:
            cur.execute(sql)
            conn.commit()
            msg_box = QMessageBox(QMessageBox.Warning, '恭喜', '注册成功')
            msg_box.exec_()
            self.nameEd1.setText("")
            self.nameEd2.setText("")
        except:
            conn.rollback()
            msg_box = QMessageBox(QMessageBox.Warning, '温馨提示', '用户名已经存在')
            msg_box.exec_()
            self.nameEd1.setText("")
            self.nameEd2.setText("")
        cur.close()
        conn.close()

    def get_username(self):
        return self.username


def main():
    app = QtWidgets.QApplication(sys.argv)
    dialog = LoginDialog()
    if dialog.exec_() == QDialog.Accepted:
        gui = MainUi(dialog.get_username())
        gui.show()
        sys.exit(app.exec_())


if __name__ == '__main__':
    main()
