# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject
import threading 
from processor import Processor
import threading
import init
import sys  
import os
import untitled
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QSlider, QStyle, QSizePolicy, QFileDialog
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtGui import QIcon, QPalette
from PyQt5.QtCore import Qt, QUrl, QTimer, QDateTime


class ExampleApp(QtWidgets.QMainWindow, untitled.Ui_MainWindow):
   
    def __init__(self):    # Main Processor ui class...
        super().__init__()
        
        self.setupUi(self)
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
      

        self.mediaPlayer.positionChanged.connect(self.position_changed)
        self.mediaPlayer.durationChanged.connect(self.duration_changed)
        self.mediaPlayer.stateChanged.connect(self.mediastate_changed)
        self.horizontalSlider.sliderMoved.connect(self.set_position)
        self.horizontalSlider_2.sliderMoved.connect(self.set_volume)


        self.mediaPlayer.setVideoOutput(self.widget)
        self.pushButton.clicked.connect(self.open_file)
        self.pushButton_2.clicked.connect(self.play_video)
        self.pushButton_2.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.horizontalSlider.setSliderPosition(0)

        self.mediaPlayer.setVolume(50)  


    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open Video")

        if filename != '':
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(filename)))
            self.pushButton_2.setEnabled(True)

    def play_video(self):

        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()


        else:
            self.mediaPlayer.play()


    def mediastate_changed(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.pushButton_2.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPause)

            )

        else:
            self.pushButton_2.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPlay)

            )

    def position_changed(self, position):
        self.horizontalSlider.setValue(position)


    def duration_changed(self, duration):
        self.horizontalSlider.setRange(0, duration)


    def set_position(self, position):
        self.mediaPlayer.setPosition(position)

    def set_volume(self, position):
        value = self.horizontalSlider_2.value()
        self.mediaPlayer.setVolume(value)
        self.statusBar.showMessage("Громкость " + str(value) + " %")


   
   
def main():
    app = QtWidgets.QApplication(sys.argv)
    window = ExampleApp()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()