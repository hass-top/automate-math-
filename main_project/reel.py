
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QTextEdit, QScrollArea, 
                             QInputDialog, QDialog, QListWidget, QDialogButtonBox,QMessageBox)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
###########
import os

from new_button import AutomateGUI
from modify_button import ModifyGUI
from graphviz import Digraph
from Alphabet import Alphabet
from Transition import Transition
from AAutomate import Automate

from determinst import DeterministicCheckGUI
from interface_complete import CompleteCheckGUI
from minimise_gui import MinimizeCheckGUI
from wordgeneration import WordGeneratorGUI 
from automationoperation import AutomataOperationsGUI
from equivanlente import EquivalenceCheckGUI
from AutomataIndex import AutomataIndex
#from user_manager import UserManagement
# cree un class de automate pour GUI 

          
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        
        self.MainWindow = MainWindow
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1280, 732)
        MainWindow.setStyleSheet("")
        MainWindow.showMaximized()
        
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.formLayout = QtWidgets.QFormLayout(self.centralwidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setSpacing(0)
        self.formLayout.setObjectName("formLayout")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame.setObjectName("frame")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.frame_7 = QtWidgets.QFrame(self.frame)
        self.frame_7.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_7.setObjectName("frame_7")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_7)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.frame_10 = QtWidgets.QFrame(self.frame_7)
        self.frame_10.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_10.setObjectName("frame_10")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame_10)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.openmenu = QtWidgets.QPushButton(self.frame_10)
        self.openmenu.setMinimumSize(QtCore.QSize(30, 30))
        self.openmenu.setStyleSheet("QPushButton {\n"
"    border-radius: 6px;\n"
"   \n"
"}")
        self.openmenu.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icon/right.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.openmenu.setIcon(icon)
        self.openmenu.setIconSize(QtCore.QSize(20, 20))
        self.openmenu.setCheckable(True)
        self.openmenu.setObjectName("openmenu")
        self.horizontalLayout_3.addWidget(self.openmenu)
        self.label_5 = QtWidgets.QLabel(self.frame_10)
        self.label_5.setMinimumSize(QtCore.QSize(40, 19))
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_3.addWidget(self.label_5, 0, QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.horizontalLayout_2.addWidget(self.frame_10, 0, QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.frame_11 = QtWidgets.QFrame(self.frame_7)
        self.frame_11.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_11.setObjectName("frame_11")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame_11)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_6 = QtWidgets.QLabel(self.frame_11)
        self.label_6.setObjectName("label_6")
        self.gridLayout_2.addWidget(self.label_6, 0, 0, 1, 1, QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.horizontalLayout_2.addWidget(self.frame_11)
        self.frame_12 = QtWidgets.QFrame(self.frame_7)
        self.frame_12.setMinimumSize(QtCore.QSize(161, 39))
        self.frame_12.setStyleSheet("QFrame {\n"
"    background-color: #1e1e1e;  /* Dark background for the frame */\n"
"    border: 2px solid #444;\n"
"    border-radius: 10px;\n"
"}\n"
"QPushButton {\n"
"    background-color: white;\n"
"    color: white;\n"
"    border: 1px solid #5c5c5c;\n"
"    border-radius: 5px;\n"
"    padding: 5px 10px;\n"
"    font-size: 14px;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: #3a3a3d;\n"
"    border: 1px solid #8a8a8a;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #0078d7;\n"
"}\n"
"")
        self.frame_12.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_12.setObjectName("frame_12")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.frame_12)
        self.horizontalLayout_4.setContentsMargins(5, 5, 5, 5)
        self.horizontalLayout_4.setSpacing(5)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.pushButton = QtWidgets.QPushButton(self.frame_12)
        self.pushButton.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setMinimumSize(QtCore.QSize(98, 30))
        self.pushButton.setText("")
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_4.addWidget(self.pushButton)
        self.background = QtWidgets.QPushButton(self.frame_12)
        self.background.setMinimumSize(QtCore.QSize(0, 24))
        self.background.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icon/background.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.background.setIcon(icon1)
        self.background.setObjectName("background")
        self.horizontalLayout_4.addWidget(self.background, 0, QtCore.Qt.AlignRight)
        self.fullscreen = QtWidgets.QPushButton(self.frame_12)
        self.fullscreen.setMinimumSize(QtCore.QSize(0, 24))
        self.fullscreen.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icon/fullscreen.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.fullscreen.setIcon(icon2)
        self.fullscreen.setObjectName("fullscreen")
        self.horizontalLayout_4.addWidget(self.fullscreen, 0, QtCore.Qt.AlignRight|QtCore.Qt.AlignTop)
        self.exit = QtWidgets.QPushButton(self.frame_12)
        self.exit.setMinimumSize(QtCore.QSize(0, 24))
        self.exit.setStyleSheet("")
        self.exit.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icon/close.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.exit.setIcon(icon3)
        self.exit.setObjectName("exit")
        self.horizontalLayout_4.addWidget(self.exit, 0, QtCore.Qt.AlignRight|QtCore.Qt.AlignTop)
        self.horizontalLayout_2.addWidget(self.frame_12)
        self.verticalLayout_6.addWidget(self.frame_7)
        self.content = QtWidgets.QFrame(self.frame)
        self.content.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.content.setObjectName("content")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.content)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.stackedWidget = QtWidgets.QStackedWidget(self.content)
        self.stackedWidget.setObjectName("stackedWidget")

        ####

        self.list_page = QtWidgets.QWidget()
        self.list_page.setObjectName("list_page")
        self.formLayout_2 = QtWidgets.QFormLayout(self.list_page)
        self.formLayout_2.setObjectName("formLayout_2")
        self.widget = QtWidgets.QWidget(self.list_page)
        self.widget.setObjectName("widget")
        self.label_9 = QtWidgets.QLabel(self.widget)
        self.label_9.setGeometry(QtCore.QRect(90, 120, 70, 19))
        self.label_9.setObjectName("label_9")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.widget)
        self.listView = QtWidgets.QListView(self.list_page)
        self.listView.setMinimumSize(QtCore.QSize(0, 0))
        self.listView.setObjectName("listView")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.listView)
        self.stackedWidget.addWidget(self.list_page)

        ######

        self.modifier_page = QtWidgets.QWidget()
        self.modifier_page.setObjectName("modifier_page")
        self.label_19 = QtWidgets.QLabel(self.modifier_page)
        self.label_19.setGeometry(QtCore.QRect(240, 100, 70, 19))
        self.label_19.setObjectName("label_19")
        self.stackedWidget.addWidget(self.modifier_page)

        ######achange 
        self.deterministe_page = QtWidgets.QWidget()
        self.deterministe_page.setObjectName("deterministe_page")
        self.deterministe_label = QtWidgets.QLabel(self.deterministe_page)
        #------ inside ------# 
        self.deterministe_label = QtWidgets.QLabel(self.deterministe_page)
        self.deterministe_label.setGeometry(QtCore.QRect(240, 100, 200, 30))
        self.deterministe_label.setObjectName("textdeterministe")
        self.deterministe_label.setText("Automate Déterministe")
        self.deterministe_label.setStyleSheet("font-size: 16px; font-weight: bold;")
      
        self.stackedWidget.addWidget(self.deterministe_page)
        
        ######

        self.main_page = QtWidgets.QWidget()
        self.main_page.setObjectName("main_page")
        
        self.label_18 = QtWidgets.QLabel(self.main_page)
        self.label_18.setGeometry(QtCore.QRect(160, 100, 600, 40))
        self.label_18.setObjectName("label_18")
        
        self.label_24 = QtWidgets.QLabel(self.main_page)
        self.label_24.setGeometry(QtCore.QRect(100, 170, 800, 19))
        self.label_24.setObjectName("label_24")
        
        self.label_25 = QtWidgets.QLabel(self.main_page)
        self.label_25.setGeometry(QtCore.QRect(100, 210, 800, 19))
        self.label_25.setObjectName("label_25")
        
        
       
        self.label_TEXT2 = QtWidgets.QLabel(self.main_page)
        self.label_TEXT2.setGeometry(QtCore.QRect(100, 250, 800, 19))
        self.label_TEXT2.setObjectName("label_TEXT2")
        
        self.label_TEXT3 = QtWidgets.QLabel(self.main_page)
        self.label_TEXT3.setGeometry(QtCore.QRect(100, 290, 800, 19))
        self.label_TEXT3.setObjectName("label_TEXT1")

        self.label_TEXT4 = QtWidgets.QLabel(self.main_page)
        self.label_TEXT4.setGeometry(QtCore.QRect(100, 330, 800, 19))
        self.label_TEXT4.setObjectName("label_TEXT4")

        self.label_TEXT5 = QtWidgets.QLabel(self.main_page)
        self.label_TEXT5.setGeometry(QtCore.QRect(100, 370, 800, 19))
        self.label_TEXT5.setObjectName("label_TEXT5")

        self.label_TEXT6 = QtWidgets.QLabel(self.main_page)
        self.label_TEXT6.setGeometry(QtCore.QRect(100, 410, 800, 19))
        self.label_TEXT6.setObjectName("label_TEXT6")

        self.label_TEXT7 = QtWidgets.QLabel(self.main_page)
        self.label_TEXT7.setGeometry(QtCore.QRect(100, 450, 800, 19))
        self.label_TEXT7.setObjectName("label_TEXT7")

        self.label_TEXT8 = QtWidgets.QLabel(self.main_page)
        self.label_TEXT8.setGeometry(QtCore.QRect(100, 490, 800, 19))
        self.label_TEXT8.setObjectName("label_TEXT8")
        self.label_18.setStyleSheet("""
    QLabel {
        font-size: 15px;
        font-weight: bold;
        font-family: 'Segoe UI', sans-serif;
        color: #2E4053;
        background-color: #F0F0F0;
        padding: 10px;
        border-radius: 10px;
        border: 1px solid #CCC;
    }
""")
        self.label_25.setStyleSheet("""
    QLabel {
        font-size: 15px;
        font-weight: bold;
        font-family: 'Segoe UI', sans-serif;
        color: #2E4053;
        background-color: #F0F0F0;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #CCC;
    }
""")
        self.label_24.setStyleSheet("""
    QLabel {
        font-size: 15px;
        font-weight: bold;
        font-family: 'Segoe UI', sans-serif;
        color: #2E4053;
        background-color: #F0F0F0;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #CCC;
    }
""")
        self.label_TEXT2.setStyleSheet("""
    QLabel {
        font-size: 15px;
        font-weight: bold;
        font-family: 'Segoe UI', sans-serif;
        color: #2E4053;
        background-color: #F0F0F0;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #CCC;
    }
""")
        self.label_TEXT3.setStyleSheet("""
    QLabel {
        font-size: 15px;
        font-weight: bold;
        font-family: 'Segoe UI', sans-serif;
        color: #2E4053;
        background-color: #F0F0F0;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #CCC;
    }
""")
        self.label_TEXT4.setStyleSheet("""
    QLabel {
        font-size: 15px;
        font-weight: bold;
        font-family: 'Segoe UI', sans-serif;
        color: #2E4053;
        background-color: #F0F0F0;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #CCC;
    }
""")
        self.label_TEXT5.setStyleSheet("""
    QLabel {
        font-size: 15px;
        font-weight: bold;
        font-family: 'Segoe UI', sans-serif;
        color: #2E4053;
        background-color: #F0F0F0;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #CCC;
    }
""")
        self.label_TEXT6.setStyleSheet("""
    QLabel {
        font-size: 15px;
        font-weight: bold;
        font-family: 'Segoe UI', sans-serif;
        color: #2E4053;
        background-color: #F0F0F0;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #CCC;
    }
""")
        self.label_TEXT7.setStyleSheet("""
    QLabel {
        font-size: 15px;
        font-weight: bold;
        font-family: 'Segoe UI', sans-serif;
        color: #2E4053;
        background-color: #F0F0F0;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #CCC;
    }
""")
        self.label_TEXT8.setStyleSheet("""
    QLabel {
        font-size: 15px;
        font-weight: bold;
        font-family: 'Segoe UI', sans-serif;
        color: #2E4053;
        background-color: #F0F0F0;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #CCC;
    }
""")
        self.stackedWidget.addWidget(self.main_page)
      
       
       
        #####

        self.newpage = QtWidgets.QWidget()
        self.newpage.setObjectName("newpage")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.newpage)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.frame_8 = QtWidgets.QFrame(self.newpage)
        self.frame_8.setMaximumSize(QtCore.QSize(177, 16777215))
        self.frame_8.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_8.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_8.setObjectName("frame_8")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame_8)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame_9 = QtWidgets.QFrame(self.frame_8)
        self.frame_9.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_9.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_9.setObjectName("frame_9")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.frame_9)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.frame_20 = QtWidgets.QFrame(self.frame_9)
        self.frame_20.setMaximumSize(QtCore.QSize(16777215, 161))
        self.frame_20.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_20.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_20.setObjectName("frame_20")
        self.verticalLayout_14 = QtWidgets.QVBoxLayout(self.frame_20)
        self.verticalLayout_14.setObjectName("verticalLayout_14")
        self.frame_18 = QtWidgets.QFrame(self.frame_20)
        self.frame_18.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_18.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_18.setObjectName("frame_18")
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout(self.frame_18)
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.pushButton_2 = QtWidgets.QPushButton(self.frame_18)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout_11.addWidget(self.pushButton_2)
        self.verticalLayout_14.addWidget(self.frame_18)
        self.checkBox = QtWidgets.QCheckBox(self.frame_20)
        self.checkBox.setMinimumSize(QtCore.QSize(100, 24))
        self.checkBox.setMaximumSize(QtCore.QSize(79, 23))
        self.checkBox.setObjectName("checkBox")
        self.verticalLayout_14.addWidget(self.checkBox, 0, QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.checkBox_2 = QtWidgets.QCheckBox(self.frame_20)
        self.checkBox_2.setMinimumSize(QtCore.QSize(78, 13))
        self.checkBox_2.setMaximumSize(QtCore.QSize(102, 24))
        self.checkBox_2.setObjectName("checkBox_2")
        self.verticalLayout_14.addWidget(self.checkBox_2, 0, QtCore.Qt.AlignTop)
        self.checkBox_3 = QtWidgets.QCheckBox(self.frame_20)
        self.checkBox_3.setMaximumSize(QtCore.QSize(99, 20))
        self.checkBox_3.setObjectName("checkBox_3")
        self.verticalLayout_14.addWidget(self.checkBox_3)
        self.verticalLayout_7.addWidget(self.frame_20)
        self.frame_21 = QtWidgets.QFrame(self.frame_9)
        self.frame_21.setMaximumSize(QtCore.QSize(130, 100))
        self.frame_21.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_21.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_21.setObjectName("frame_21")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_21)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.frame_21)
        self.pushButton_3.setObjectName("pushButton_3")
        self.verticalLayout_2.addWidget(self.pushButton_3)
        self.frame_19 = QtWidgets.QFrame(self.frame_21)
        self.frame_19.setMaximumSize(QtCore.QSize(16777215, 54))
        self.frame_19.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_19.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_19.setObjectName("frame_19")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(self.frame_19)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.label_10 = QtWidgets.QLabel(self.frame_19)
        self.label_10.setMinimumSize(QtCore.QSize(41, 18))
        self.label_10.setMaximumSize(QtCore.QSize(49, 19))
        self.label_10.setObjectName("label_10")
        self.horizontalLayout_9.addWidget(self.label_10)
        self.lineEdit = QtWidgets.QLineEdit(self.frame_19)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout_9.addWidget(self.lineEdit)
        self.verticalLayout_2.addWidget(self.frame_19)
        self.verticalLayout_7.addWidget(self.frame_21)
        self.frame_14 = QtWidgets.QFrame(self.frame_9)
        self.frame_14.setMaximumSize(QtCore.QSize(158, 212))
        self.frame_14.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_14.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_14.setObjectName("frame_14")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.frame_14)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.frame_24 = QtWidgets.QFrame(self.frame_14)
        self.frame_24.setMinimumSize(QtCore.QSize(130, 42))
        self.frame_24.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_24.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_24.setObjectName("frame_24")
        self.horizontalLayout_14 = QtWidgets.QHBoxLayout(self.frame_24)
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")
        self.pushButton_4 = QtWidgets.QPushButton(self.frame_24)
        self.pushButton_4.setObjectName("pushButton_4")
        self.horizontalLayout_14.addWidget(self.pushButton_4)
        self.verticalLayout_8.addWidget(self.frame_24, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.frame_23 = QtWidgets.QFrame(self.frame_14)
        self.frame_23.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_23.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_23.setObjectName("frame_23")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout(self.frame_23)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.frame_35 = QtWidgets.QFrame(self.frame_23)
        self.frame_35.setMinimumSize(QtCore.QSize(83, 0))
        self.frame_35.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_35.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_35.setObjectName("frame_35")
        self.verticalLayout_16 = QtWidgets.QVBoxLayout(self.frame_35)
        self.verticalLayout_16.setObjectName("verticalLayout_16")
        self.label_13 = QtWidgets.QLabel(self.frame_35)
        self.label_13.setObjectName("label_13")
        self.verticalLayout_16.addWidget(self.label_13)
        self.label_14 = QtWidgets.QLabel(self.frame_35)
        self.label_14.setObjectName("label_14")
        self.verticalLayout_16.addWidget(self.label_14)
        self.label_12 = QtWidgets.QLabel(self.frame_35)
        self.label_12.setObjectName("label_12")
        self.verticalLayout_16.addWidget(self.label_12)
        self.horizontalLayout_10.addWidget(self.frame_35)
        self.frame_13 = QtWidgets.QFrame(self.frame_23)
        self.frame_13.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_13.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_13.setObjectName("frame_13")
        self.verticalLayout_15 = QtWidgets.QVBoxLayout(self.frame_13)
        self.verticalLayout_15.setObjectName("verticalLayout_15")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.frame_13)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.verticalLayout_15.addWidget(self.lineEdit_2)
        self.lineEdit_4 = QtWidgets.QLineEdit(self.frame_13)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.verticalLayout_15.addWidget(self.lineEdit_4)
        self.lineEdit_3 = QtWidgets.QLineEdit(self.frame_13)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.verticalLayout_15.addWidget(self.lineEdit_3)
        self.horizontalLayout_10.addWidget(self.frame_13)
        self.verticalLayout_8.addWidget(self.frame_23)
        self.verticalLayout_7.addWidget(self.frame_14)
        self.verticalLayout.addWidget(self.frame_9, 0, QtCore.Qt.AlignTop)
        self.horizontalLayout_5.addWidget(self.frame_8)
        self.frame_2 = QtWidgets.QFrame(self.newpage)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout_13 = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout_13.setObjectName("verticalLayout_13")
        self.frame_25 = QtWidgets.QFrame(self.frame_2)
        self.frame_25.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_25.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_25.setObjectName("frame_25")
        self.verticalLayout_18 = QtWidgets.QVBoxLayout(self.frame_25)
        self.verticalLayout_18.setObjectName("verticalLayout_18")
        self.frame_30 = QtWidgets.QFrame(self.frame_25)
        self.frame_30.setMaximumSize(QtCore.QSize(16777215, 50))
        self.frame_30.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_30.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_30.setObjectName("frame_30")
        self.horizontalLayout_16 = QtWidgets.QHBoxLayout(self.frame_30)
        self.horizontalLayout_16.setObjectName("horizontalLayout_16")
        self.label_21 = QtWidgets.QLabel(self.frame_30)
        self.label_21.setObjectName("label_21")
        self.horizontalLayout_16.addWidget(self.label_21)
        self.lineEdit_6 = QtWidgets.QLineEdit(self.frame_30)
        self.lineEdit_6.setObjectName("lineEdit_6")
        self.horizontalLayout_16.addWidget(self.lineEdit_6)
        self.label_22 = QtWidgets.QLabel(self.frame_30)
        self.label_22.setObjectName("label_22")
        self.horizontalLayout_16.addWidget(self.label_22)
        self.lineEdit_7 = QtWidgets.QLineEdit(self.frame_30)
        self.lineEdit_7.setObjectName("lineEdit_7")
        self.horizontalLayout_16.addWidget(self.lineEdit_7)
        self.label_23 = QtWidgets.QLabel(self.frame_30)
        self.label_23.setObjectName("label_23")
        self.horizontalLayout_16.addWidget(self.label_23)
        self.lineEdit_8 = QtWidgets.QLineEdit(self.frame_30)
        self.lineEdit_8.setObjectName("lineEdit_8")
        self.horizontalLayout_16.addWidget(self.lineEdit_8)
        self.pushButton_6 = QtWidgets.QPushButton(self.frame_30)
        self.pushButton_6.setObjectName("pushButton_6")
        self.horizontalLayout_16.addWidget(self.pushButton_6)
        self.verticalLayout_18.addWidget(self.frame_30)
        self.frame_28 = QtWidgets.QFrame(self.frame_25)
        self.frame_28.setMaximumSize(QtCore.QSize(16777215, 50))
        self.frame_28.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_28.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_28.setObjectName("frame_28")
        self.horizontalLayout_15 = QtWidgets.QHBoxLayout(self.frame_28)
        self.horizontalLayout_15.setObjectName("horizontalLayout_15")
        self.label_20 = QtWidgets.QLabel(self.frame_28)
        self.label_20.setObjectName("label_20")
        self.horizontalLayout_15.addWidget(self.label_20)
        self.lineEdit_5 = QtWidgets.QLineEdit(self.frame_28)
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.horizontalLayout_15.addWidget(self.lineEdit_5)
        self.pushButton_5 = QtWidgets.QPushButton(self.frame_28)
        self.pushButton_5.setObjectName("pushButton_5")
        self.horizontalLayout_15.addWidget(self.pushButton_5)
        self.verticalLayout_18.addWidget(self.frame_28)
        self.verticalLayout_13.addWidget(self.frame_25, 0, QtCore.Qt.AlignTop)
        self.frame_27 = QtWidgets.QFrame(self.frame_2)
        self.frame_27.setMinimumSize(QtCore.QSize(0, 426))
        self.frame_27.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_27.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_27.setObjectName("frame_27")
        self.verticalLayout_13.addWidget(self.frame_27)
        self.horizontalLayout_5.addWidget(self.frame_2)
        self.stackedWidget.addWidget(self.newpage)
        self.verticalLayout_9.addWidget(self.stackedWidget)
        self.verticalLayout_6.addWidget(self.content)
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.frame)
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setMinimumSize(QtCore.QSize(174, 19))
        self.label_8.setObjectName("label_8")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_8)
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setObjectName("label_7")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.label_7)
        self.frame_33 = QtWidgets.QFrame(self.centralwidget)
        self.frame_33.setMaximumSize(QtCore.QSize(321, 701))
        self.frame_33.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_33.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_33.setObjectName("frame_33")
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout(self.frame_33)
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.frame_22 = QtWidgets.QFrame(self.frame_33)
        self.frame_22.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_22.sizePolicy().hasHeightForWidth())
        self.frame_22.setSizePolicy(sizePolicy)
        self.frame_22.setMinimumSize(QtCore.QSize(71, 539))
        self.frame_22.setMaximumSize(QtCore.QSize(200, 700))
        self.frame_22.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_22.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_22.setObjectName("frame_22")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame_22)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.frame_32 = QtWidgets.QFrame(self.frame_22)
        self.frame_32.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_32.setObjectName("frame_32")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.frame_32)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.label_15 = QtWidgets.QLabel(self.frame_32)
        self.label_15.setMaximumSize(QtCore.QSize(40, 40))
        self.label_15.setText("")
        self.label_15.setPixmap(QtGui.QPixmap(":/icon/Downloads/technology.png"))
        self.label_15.setScaledContents(True)
        self.label_15.setObjectName("label_15")
        self.horizontalLayout_8.addWidget(self.label_15)
        self.verticalLayout_3.addWidget(self.frame_32)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem)
        self.label_17 = QtWidgets.QLabel(self.frame_22)
        self.label_17.setObjectName("label_17")
        self.verticalLayout_3.addWidget(self.label_17)
        self.horizontalLayout_12.addWidget(self.frame_22)
        self.main_open = QtWidgets.QFrame(self.frame_33)
        self.main_open.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.main_open.setFrameShadow(QtWidgets.QFrame.Raised)
        self.main_open.setObjectName("main_open")
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout(self.main_open)
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.widget_menu = QtWidgets.QWidget(self.main_open)
        self.widget_menu.setObjectName("widget_menu")
        self.gridLayout = QtWidgets.QGridLayout(self.widget_menu)
        self.gridLayout.setObjectName("gridLayout")
        self.frame_5 = QtWidgets.QFrame(self.widget_menu)
        self.frame_5.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_5.setObjectName("frame_5")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.frame_5)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_3 = QtWidgets.QLabel(self.frame_5)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_4.addWidget(self.label_3)
        self.frame_16 = QtWidgets.QFrame(self.frame_5)
        self.frame_16.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_16.setObjectName("frame_16")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.frame_16)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.deterministe = QtWidgets.QPushButton(self.frame_16)
        self.deterministe.setStyleSheet("QPushButton {\n"
" \n"
"    border: 1px solid #444;\n"
"    border-radius: 6px;\n"
"    padding: 6px 12px;\n"
"    font-size: 14px;\n"
"}")
        self.deterministe.setStyleSheet("QPushButton {\n"
"    background-color: #2e2e3e;\n"
"    color: #ffffff;\n"
"    border: 1px solid #444;\n"
"    border-radius: 6px;\n"
"    padding: 6px 12px;\n"
"    font-size: 14px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #3d3d5c;\n"
"    border: 1px solid #666;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #5c5cff;\n"
"}")
        self.deterministe.setCheckable(True)
        self.deterministe.setAutoExclusive(True)
        self.deterministe.setObjectName("deterministe")
        self.verticalLayout_11.addWidget(self.deterministe)
      

       
        self.mini_button = QtWidgets.QPushButton(self.frame_16)
        self.mini_button.setStyleSheet("QPushButton {\n"
" \n"
"    border: 1px solid #444;\n"
"    border-radius: 6px;\n"
"    padding: 6px 12px;\n"
"    font-size: 14px;\n"
"}")
        self.mini_button.setStyleSheet("QPushButton {\n"
"    background-color: #2e2e3e;\n"
"    color: #ffffff;\n"
"    border: 1px solid #444;\n"
"    border-radius: 6px;\n"
"    padding: 6px 12px;\n"
"    font-size: 14px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #3d3d5c;\n"
"    border: 1px solid #666;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #5c5cff;\n"
"}")
        self.mini_button.setCheckable(True)
        self.mini_button.setAutoExclusive(True)
        self.mini_button.setObjectName("mini_button")
        self.verticalLayout_11.addWidget(self.mini_button)
        self.auto_complet_button = QtWidgets.QPushButton(self.frame_16)
        self.auto_complet_button.setStyleSheet("QPushButton {\n"
"    background-color: #2e2e3e;\n"
"    color: #ffffff;\n"
"    border: 1px solid #444;\n"
"    border-radius: 6px;\n"
"    padding: 6px 12px;\n"
"    font-size: 14px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #3d3d5c;\n"
"    border: 1px solid #666;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #5c5cff;\n"
"}")
        self.auto_complet_button.setCheckable(True)
        self.auto_complet_button.setAutoExclusive(True)
        self.auto_complet_button.setObjectName("auto_complet_button")
        self.verticalLayout_11.addWidget(self.auto_complet_button)
        self.verticalLayout_4.addWidget(self.frame_16)
        self.gridLayout.addWidget(self.frame_5, 2, 1, 1, 1)
        self.frame_6 = QtWidgets.QFrame(self.widget_menu)
        self.frame_6.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_6.setObjectName("frame_6")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.frame_6)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label_4 = QtWidgets.QLabel(self.frame_6)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_5.addWidget(self.label_4)
        self.frame_17 = QtWidgets.QFrame(self.frame_6)
        self.frame_17.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_17.setObjectName("frame_17")
        self.verticalLayout_12 = QtWidgets.QVBoxLayout(self.frame_17)
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        
        self.generate_button = QtWidgets.QPushButton(self.frame_17)
        self.generate_button.setStyleSheet("QPushButton {\n"
"    background-color: #2e2e3e;\n"
"    color: #ffffff;\n"
"    border: 1px solid #444;\n"
"    border-radius: 6px;\n"
"    padding: 6px 12px;\n"
"    font-size: 14px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #3d3d5c;\n"
"    border: 1px solid #666;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #5c5cff;\n"
"}")
        self.generate_button.setCheckable(True)
        self.generate_button.setAutoExclusive(True)
        self.generate_button.setObjectName("generate_button")
        self.verticalLayout_12.addWidget(self.generate_button)
        self.compare_button = QtWidgets.QPushButton(self.frame_17)
        self.compare_button.setStyleSheet("QPushButton {\n"
"    background-color: #2e2e3e;\n"
"    color: #ffffff;\n"
"    border: 1px solid #444;\n"
"    border-radius: 6px;\n"
"    padding: 6px 12px;\n"
"    font-size: 14px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #3d3d5c;\n"
"    border: 1px solid #666;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #5c5cff;\n"
"}")
        
        self.compare_button.setCheckable(True)
        self.compare_button.setAutoExclusive(True)
        self.compare_button.setObjectName("compare_button")
        self.verticalLayout_12.addWidget(self.compare_button)
        self.equivalence = QtWidgets.QPushButton(self.frame_17)
        self.equivalence.setStyleSheet("QPushButton {\n"
"    background-color: #2e2e3e;\n"
"    color: #ffffff;\n"
"    border: 1px solid #444;\n"
"    border-radius: 6px;\n"
"    padding: 6px 12px;\n"
"    font-size: 14px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #3d3d5c;\n"
"    border: 1px solid #666;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #5c5cff;\n"
"}")
        self.equivalence.setCheckable(True)
        self.equivalence.setAutoExclusive(True)
        self.equivalence.setObjectName("equivalence")
        self.verticalLayout_12.addWidget(self.equivalence)
        self.verticalLayout_5.addWidget(self.frame_17)
        self.gridLayout.addWidget(self.frame_6, 3, 1, 1, 1)
        self.frame_4 = QtWidgets.QFrame(self.widget_menu)
        self.frame_4.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_4.setObjectName("frame_4")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.frame_4)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.frame_15 = QtWidgets.QFrame(self.frame_4)
        self.frame_15.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_15.setObjectName("frame_15")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.frame_15)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.news = QtWidgets.QPushButton(self.frame_15)
        self.news.setStyleSheet("QPushButton {\n"
"    background-color: #2e2e3e;\n"
"    color: #ffffff;\n"
"    border: 1px solid #444;\n"
"    border-radius: 6px;\n"
"    padding: 6px 12px;\n"
"    font-size: 14px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #3d3d5c;\n"
"    border: 1px solid #666;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #5c5cff;\n"
"}")
        self.news.setCheckable(True)
        self.news.setAutoExclusive(True)
        self.news.setObjectName("news")
        self.verticalLayout_10.addWidget(self.news)
        self.list = QtWidgets.QPushButton(self.frame_15)
        self.list.setStyleSheet("QPushButton {\n"
" \n"
"    border: 1px solid #444;\n"
"    border-radius: 6px;\n"
"    padding: 6px 12px;\n"
"    font-size: 14px;\n"
"}")
        self.list.setStyleSheet("QPushButton {\n"
"    background-color: #2e2e3e;\n"
"    color: #ffffff;\n"
"    border: 1px solid #444;\n"
"    border-radius: 6px;\n"
"    padding: 6px 12px;\n"
"    font-size: 14px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #3d3d5c;\n"
"    border: 1px solid #666;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #5c5cff;\n"
"}")
        self.list.setCheckable(True)
        self.list.setAutoExclusive(True)
        self.list.setObjectName("list")
        self.verticalLayout_10.addWidget(self.list)
        










        self.Modify = QtWidgets.QPushButton(self.frame_15)
        self.Modify.setStyleSheet("QPushButton {\n"
" \n"
"    border: 1px solid #444;\n"
"    border-radius: 6px;\n"
"    padding: 6px 12px;\n"
"    font-size: 14px;\n"
"}")
        self.Modify.setStyleSheet("QPushButton {\n"
"    background-color: #2e2e3e;\n"
"    color: #ffffff;\n"
"    border: 1px solid #444;\n"
"    border-radius: 6px;\n"
"    padding: 6px 12px;\n"
"    font-size: 14px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #3d3d5c;\n"
"    border: 1px solid #666;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #5c5cff;\n"
"}")
        self.Modify.setCheckable(True)
        self.Modify.setAutoExclusive(True)
        self.Modify.setObjectName("list")
        self.verticalLayout_10.addWidget(self.Modify)





        
        self.gridLayout_3.addWidget(self.frame_15, 1, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.frame_4)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setStyleSheet("QPushButton {\n"
"    background-color: #2e2e3e;\n"
"    color: #ffffff;\n"
"    border: 1px solid #444;\n"
"    border-radius: 6px;\n"
"    padding: 6px 12px;\n"
"    font-size: 14px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #3d3d5c;\n"
"    border: 1px solid #666;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #5c5cff;\n"
"}")
        self.label.setObjectName("label")
        self.gridLayout_3.addWidget(self.label, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.frame_4, 1, 1, 1, 1)
        self.frame_3 = QtWidgets.QFrame(self.widget_menu)
        self.frame_3.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_3.setObjectName("frame_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame_3)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_11 = QtWidgets.QLabel(self.frame_3)
        self.label_11.setMaximumSize(QtCore.QSize(40, 40))
        self.label_11.setText("")
        self.label_11.setPixmap(QtGui.QPixmap(":/icon/technology.png"))
        self.label_11.setScaledContents(True)
        self.label_11.setObjectName("label_11")
        self.horizontalLayout.addWidget(self.label_11)
        self.label_2 = QtWidgets.QLabel(self.frame_3)
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.gridLayout.addWidget(self.frame_3, 0, 1, 1, 1)
        self.horizontalLayout_13.addWidget(self.widget_menu)
        self.horizontalLayout_12.addWidget(self.main_open)
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.frame_33)
        MainWindow.setCentralWidget(self.centralwidget)


        self.menu_animation = QtCore.QPropertyAnimation(self.frame_33, b"maximumWidth")
        self.menu_animation.setDuration(300)
        self.menu_animation.setEasingCurve(QtCore.QEasingCurve.InOutQuad)
        ####
        self.frame_22.setMaximumWidth(200)
        self.widget_menu.setMaximumWidth(0)
       
        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(3)

        self.exit.clicked.connect(MainWindow.close)
        self.background.clicked.connect(MainWindow.showMinimized)
        self.fullscreen.toggled.connect(self.toggle_fullscreen)
        self.fullscreen.setCheckable(True)
        self.openmenu.toggled.connect(self.toggle_menu)
        self.news.clicked.connect(self.open_new_window)
       
        self.list.clicked.connect(self.show_saved_automata)
        self.Modify.clicked.connect(self.modify_automate)
        self.mini_button.clicked.connect ( self.open_minimal)
        self.deterministe.clicked.connect(self.open_deterministic_checker)
        self.generate_button.clicked.connect(self.open_word_generation)
        self.auto_complet_button.clicked.connect(self.auto_complete)
        self.compare_button.clicked.connect(self.open_operation) 
        self.equivalence.clicked.connect(self.open_equivalence) 
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
#------
        
        
        



    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_5.setText(_translate("MainWindow", "menu"))
        self.label_6.setText(_translate("MainWindow", ""))#dashbord"))
        self.label_9.setText(_translate("MainWindow", "label 1 "))
       
        self.deterministe_label.setText(_translate("MainWindow", "deterministe_label"))
        self.label_18.setText(_translate("MainWindow", "Bienvenue dans notre application de gestion et d'analyse d'automates finis."))
        self.label_24.setText(_translate("MainWindow", "ici il ya 3 case dans le menu 1/ automate 2/analyse et 3/ avance "))
        self.label_25.setText(_translate("MainWindow", "new ==>  creation d'un automate + visualise + save  + open  + test mot  "))
        
        self.label_TEXT2.setText(_translate("MainWindow", "list ==> voir les automate + supprime un automate "))
        self.label_TEXT3.setText(_translate("MainWindow", "deterministe ==> check deterministic + convert to DFA  "))
        self.label_TEXT4.setText(_translate("MainWindow", "minimal auto ==> check Minimal and minimize automation + sauvgarder"))
        self.label_TEXT5.setText(_translate("MainWindow", "auto complet ==>  check complete Automate + sauvarder "))
        self.label_TEXT6.setText(_translate("MainWindow", "generer ==> generate accepted words + generate rejected words  +sauvgarder"))
        self.label_TEXT7.setText(_translate("MainWindow", "compare ==>  union + intersection + complement + saugarder "))
        self.label_TEXT8.setText(_translate("MainWindow", "equivalence ==>check equivalence "))
        self.pushButton_2.setText(_translate("MainWindow", "add state"))
        self.checkBox.setText(_translate("MainWindow", "source "))
        self.checkBox_2.setText(_translate("MainWindow", "intermidate"))
        self.checkBox_3.setText(_translate("MainWindow", "final"))
        self.pushButton_3.setText(_translate("MainWindow", "erase state"))
        self.label_10.setText(_translate("MainWindow", "ID :"))
        self.pushButton_4.setText(_translate("MainWindow", "delete trans"))
        self.label_13.setText(_translate("MainWindow", "start"))
        self.label_14.setText(_translate("MainWindow", "alpha"))
        self.label_12.setText(_translate("MainWindow", "end"))
        self.label_21.setText(_translate("MainWindow", "transition start "))
        self.label_22.setText(_translate("MainWindow", "alphabet"))
        self.label_23.setText(_translate("MainWindow", "end"))
        self.pushButton_6.setText(_translate("MainWindow", "PushButton"))
        self.label_20.setText(_translate("MainWindow", "autorise alphabet :"))
        self.pushButton_5.setText(_translate("MainWindow", "PushButton"))
        self.label_8.setText(_translate("MainWindow", ""))#APP_VERSION = \"v1.0.0\""))
        self.label_7.setText(_translate("MainWindow", ""))#created with a cup of  ☕"))
        self.label_17.setText(_translate("MainWindow", ""))#with friend "))
        self.label_3.setText(_translate("MainWindow", "analyse"))
        self.deterministe.setText(_translate("MainWindow", "deterministe "))
       
        self.mini_button.setText(_translate("MainWindow", "minimal auto"))
        self.auto_complet_button.setText(_translate("MainWindow", "auto complet"))
        self.label_4.setText(_translate("MainWindow", "avance "))
        
        self.generate_button.setText(_translate("MainWindow", "générer/test mots"))
        self.compare_button.setText(_translate("MainWindow", "compare"))
        self.equivalence.setText(_translate("MainWindow", "equivalence"))
        self.news.setText(_translate("MainWindow", "new"))
        self.list.setText(_translate("MainWindow", "list"))
        self.Modify.setText(_translate("MainWindow","modifier"))
        self.label.setText(_translate("MainWindow", "automate"))
        self.label_2.setText(_translate("MainWindow", "auto_tic"))
    def open_equivalence( self ) :
        self.gui_equivalent=EquivalenceCheckGUI () 
        self.gui_equivalent.show() 
    def open_operation( self ) :
        self.gui_operation=AutomataOperationsGUI () 
        self.gui_operation.show() 
    def open_word_generation( self ) :
        self.gui_generation = WordGeneratorGUI() 
        self.gui_generation.show() 
    def open_minimal(self) : 
        self.minimal_gui=MinimizeCheckGUI()
        self.minimal_gui .show ()
    def open_deterministic_checker(self):
        self.deterministic_window = DeterministicCheckGUI()
        self.deterministic_window.show()
#       
    def auto_complete( self) :
        self.complete_interface = CompleteCheckGUI()
        self.complete_interface.show() 
    def show_saved_automata(self):
        dialog = QDialog(self.MainWindow)
        dialog.setWindowTitle("Automates sauvegardés")
        dialog.setGeometry(200, 200, 400, 300)
    
        layout = QVBoxLayout(dialog)

        label = QLabel("Sélectionnez un automate à supprimer :")
        layout.addWidget(label)

        list_widget = QListWidget()
        if os.path.exists(Automate.saveDir):

            json_files = [f for f in os.listdir(Automate.saveDir) if f.endswith(Automate.saveExt)]
        else:
            json_files = []
    
        if not json_files:
                list_widget.addItem("Aucun automate trouvé")
                list_widget.setEnabled(False)
        else:
                list_widget.addItems(json_files)
    
        layout.addWidget(list_widget)

         # Zone des boutons : Supprimer
        button_layout = QHBoxLayout()

        

        delete_button = QPushButton("Supprimer")
        def delete_selected():
            selected_item = list_widget.currentItem()
            if selected_item:
                file_name = selected_item.text()
                file_name = os.path.basename(file_name)
                file_name = Automate.saveDir+file_name

                reply = QMessageBox.warning(
                    dialog,
                    "Confirmer la suppression",
                    f"Voulez-vous vraiment supprimer « {file_name} » ?",
                    QMessageBox.Yes | QMessageBox.No
                )
                if reply == QMessageBox.Yes:
                    try:
                        os.remove(file_name)
                        QMessageBox.information(dialog, "Succès", f"Fichier {file_name} supprimé.")
                        # Mise à jour de la liste
                        list_widget.clear()
                        if os.path.exists(Automate.saveDir):
                            new_files = [f for f in os.listdir(Automate.saveDir) if f.endswith(Automate.saveExt)]
                        else:
                            json_files = []
                        if not new_files:
                            list_widget.addItem("Aucun automate trouvé")
                            list_widget.setEnabled(False)
                        else:
                            list_widget.setEnabled(True)
                            list_widget.addItems(new_files)
                    except Exception as e:
                        QMessageBox.critical(dialog, "Erreur", f"Erreur lors de la suppression : {e}")
            else:
                QMessageBox.warning(dialog, "Aucun fichier", "Veuillez sélectionner un fichier à supprimer.")
        
        delete_button.clicked.connect(delete_selected)
        button_layout.addWidget(delete_button)

        layout.addLayout(button_layout)

        # Boutons Ok / Cancel si tu veux les garder
        buttons = QDialogButtonBox(QDialogButtonBox.Cancel)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)

        dialog.exec_()
# def toggle_fullscreen

    def toggle_fullscreen(self, checked):
        if checked:
           
            self.MainWindow.showFullScreen()
        else:
          
            self.MainWindow.showNormal()

        ####
    def open_new_window(self):
        self.AutomateGUI = AutomateGUI()
        self.AutomateGUI.show()
        ###

#def toggle_menu 

    def toggle_menu(self, checked):
        if checked:
            self.menu_animation.setStartValue(150)
            self.menu_animation.setEndValue(321)
            self.openmenu.setIcon(QtGui.QIcon(":/icon/left.png"))
            self.frame_22.hide()
            self.widget_menu.show()
            self.frame_22.setMaximumWidth(0)
            self.widget_menu.setMaximumWidth(200)
        else:
            self.menu_animation.setStartValue(321)
            self.menu_animation.setEndValue(150)
            self.openmenu.setIcon(QtGui.QIcon(":/icon/right.png"))
            self.frame_22.show()
            self.widget_menu.hide()
            self.frame_22.setMaximumWidth(100)
            self.widget_menu.setMaximumWidth(0)
        self.frame_7.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        self.menu_animation.start()
        self.frame_7.updateGeometry()
    def modify_automate(self):
        self.modifyGUI = ModifyGUI()
        self.modifyGUI.show()
    def lancer_reel_ui(self):
        import sys
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        #ui = Ui_MainWindow()
        self.setupUi(MainWindow)
        MainWindow.show()
        sys.exit(app.exec_())
import ressource_rc

    
if __name__ == "__main__":
    ui = Ui_MainWindow()
    ui.lancer_reel_ui()