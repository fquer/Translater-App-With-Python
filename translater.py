from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from PyQt5.QtWidgets import QCheckBox, QMessageBox
import pytesseract
import pyautogui
import keyboard
import time
from googletrans import Translator
from screeninfo import get_monitors
import getpass
import os
from PIL import ImageGrab
from functools import partial
ImageGrab.grab = partial(ImageGrab.grab, all_screens=True)
import ctypes
myappid = 'translater.app' # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

translator = Translator()
username = getpass.getuser()

class Worker(QObject):
    
    text = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, parent=None):
        QObject.__init__(self, parent=parent)
        self.continue_run = True 

    def do_work(self):
        
        while True:
            if self.continue_run == True:
                screen = pyautogui.screenshot()
                self.img_res = screen.crop((self.top_leftx, self.top_lefty, self.bottom_rightx, self.bottom_righty))
                sentence = pytesseract.image_to_string(self.img_res)
                sentence = str(sentence).replace("\n"," ")
                
                try:
                    self.tr = translator.translate(sentence , src = self.language1, dest=self.language2)
                    tr_text = str(self.tr.text)
                    time.sleep(1)
                    self.text.emit(tr_text)
                except:
                    self.text.emit("")


            

    def set_coordinates(self,topx,topy,botx,boty,l1,l2,monitor):
        self.top_leftx=topx
        self.top_lefty=topy
        self.bottom_rightx=botx
        self.bottom_righty=boty
        self.language1=l1
        self.language2=l2

        if monitor == 1:
            for m in get_monitors():
                if m.x < 0:
                    left_monitor = m.x * -1
            self.top_leftx = self.top_leftx + left_monitor
            self.bottom_rightx = self.bottom_rightx + left_monitor


    def get_trans(self):
        self.self.textBrowser.setText(self.tr)

    def stop(self):
        self.continue_run = False  

    def check(self,boolean):
        self.continue_run = boolean  

class Ui_MainWindow(QtWidgets.QWidget):

    stop_signal = pyqtSignal()
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(600, 350)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setGeometry(QtCore.QRect(20, 20, 751, 541))
        self.stackedWidget.setObjectName("stackedWidget")
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        self.translate_button = QtWidgets.QPushButton(self.page)
        self.translate_button.setGeometry(QtCore.QRect(410, 230, 75, 23))
        self.translate_button.setObjectName("translate_button")
        self.bottomright = QtWidgets.QLabel(self.page)
        self.bottomright.setGeometry(QtCore.QRect(40, 80, 111, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.bottomright.setFont(font)
        self.bottomright.setObjectName("bottomright")
        self.topleft = QtWidgets.QLabel(self.page)
        self.topleft.setGeometry(QtCore.QRect(40, 30, 71, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.topleft.setFont(font)
        self.topleft.setObjectName("topleft")
        self.topleft_coordinate = QtWidgets.QLabel(self.page)
        self.topleft_coordinate.setGeometry(QtCore.QRect(150, 30, 181, 20))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.topleft_coordinate.setFont(font)
        self.topleft_coordinate.setObjectName("topleft_coordinate")
        self.bottomright_coordinate = QtWidgets.QLabel(self.page)
        self.bottomright_coordinate.setGeometry(QtCore.QRect(150, 80, 191, 20))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.bottomright_coordinate.setFont(font)
        self.bottomright_coordinate.setObjectName("bottomright_coordinate")
        self.coordinate_status = QtWidgets.QLabel(self.page)
        self.coordinate_status.setGeometry(QtCore.QRect(70, 170, 291, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.coordinate_status.setFont(font)
        self.coordinate_status.setObjectName("coordinate_status")
        self.setup_button = QtWidgets.QPushButton(self.page)
        self.setup_button.setGeometry(QtCore.QRect(100, 130, 75, 23))
        self.setup_button.setObjectName("setup_button")

        self.help_button = QtWidgets.QPushButton(self.page)
        self.help_button.setGeometry(QtCore.QRect(115, 250, 45, 23))
        self.help_button.setObjectName("help_button")
        self.help_button.setText("Help")
        self.help_button.clicked.connect(lambda:QMessageBox.about(MainWindow,"Help", "Top left coordinates with - key\nBottom right coordinates with + key\nJust move your mouse to any coordinate and press it !"))

        self.language_1 = QtWidgets.QLineEdit(self.page)
        self.language_1.setGeometry(QtCore.QRect(380, 180, 41, 20))
        self.language_1.setObjectName("language_1")

        self.label = QtWidgets.QLabel(self.page)
        self.label.setGeometry(QtCore.QRect(440, 180, 31, 20))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.language_2 = QtWidgets.QLineEdit(self.page)
        self.language_2.setGeometry(QtCore.QRect(470, 180, 41, 20))
        self.language_2.setObjectName("language_2")
        self.label_3 = QtWidgets.QLabel(self.page)
        self.label_3.setGeometry(QtCore.QRect(380, 150, 161, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.stackedWidget.addWidget(self.page)
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.textBrowser = QtWidgets.QTextBrowser(self.page_2)
        self.textBrowser.setGeometry(QtCore.QRect(30, 30, 711, 461))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.textBrowser.setFont(font)
        self.textBrowser.setObjectName("textBrowser")

        self.textBrowser.setStyleSheet("background-color: rgb(202, 202, 202);")
        

        self.monitor_helper = QtWidgets.QLabel(self.page)
        self.monitor_helper.setGeometry(QtCore.QRect(340, 60, 190, 18))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.monitor_helper.setFont(font)
        self.monitor_helper.setObjectName("monitor_helper")
        self.monitor_helper.setText("Set your multiple-monitor setup")
        self.monitor_helper.setEnabled(False)

        self.monitor = QCheckBox(self.page)
        self.monitor.setText("Multiple-Monitors")
        self.monitor.setGeometry(QtCore.QRect(380, 25, 161, 21))
        self.monitor.stateChanged.connect(lambda:self.check_state(self.monitor))

        self.monitor_1 = QCheckBox(self.page)
        self.monitor_1.setText("|2|1|")
        self.monitor_1.setGeometry(QtCore.QRect(450, 100, 70, 21))
        self.monitor_1.stateChanged.connect(lambda:self.check_state(self.monitor_1))
        self.monitor_1.setEnabled(False)

        self.monitor_0 = QCheckBox(self.page)
        self.monitor_0.setText("|1|2|")
        self.monitor_0.setGeometry(QtCore.QRect(355, 100, 70, 21))
        self.monitor_0.stateChanged.connect(lambda:self.check_state(self.monitor_0))
        self.monitor_0.setEnabled(False)

        self.monitor_state = 0

        self.back_button = QtWidgets.QPushButton(self.page_2)
        self.back_button.setGeometry(QtCore.QRect(30, 510, 75, 23))
        self.back_button.setObjectName("back_button")
        
        self.status = QtWidgets.QLabel(self.page_2)
        self.status.setGeometry(QtCore.QRect(550, 510, 161, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.status.setFont(font)
        self.status.setObjectName("status")
        self.status.setText("Status : Waiting...")
        self.stackedWidget.addWidget(self.page_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.stackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.topleft_coordinate.setText("Setup Needed")
        self.bottomright_coordinate.setText("Setup Needed")
        
        self.translate_button.clicked.connect(self.b_translate)
        self.back_button.clicked.connect(self.b_back)
        self.setup_button.clicked.connect(self.setup)

        self.thread = QThread()
        self.worker = Worker()
        self.stop_signal.connect(self.worker.stop)  
        self.worker.moveToThread(self.thread)

        self.worker.finished.connect(self.thread.quit)  
        self.worker.finished.connect(self.worker.deleteLater)  
        self.thread.finished.connect(self.thread.deleteLater)  

        self.worker.text.connect(self.add_text)

        self.start_button = QtWidgets.QPushButton(self.page_2)
        self.start_button.setGeometry(QtCore.QRect(400, 510, 75, 23))
        self.start_button.setObjectName("start_button")
        self.stop_button = QtWidgets.QPushButton(self.page_2)
        self.stop_button.setGeometry(QtCore.QRect(300, 510, 75, 23))
        self.stop_button.setObjectName("stop_button")

        self.thread.started.connect(self.worker.do_work)
        self.thread.finished.connect(self.worker.stop)
        # Start Button action:
        self.start_button.clicked.connect(self.thread.start)
        self.start_button.clicked.connect(self.signal_start)
        # Stop Button action:
        self.back_button.clicked.connect(self.stop_thread)
        self.back_button.clicked.connect(self.signal_stop)
        self.stop_button.clicked.connect(self.stop_thread)
        self.stop_button.clicked.connect(self.signal_stop)

        self.topleft_status = False
        self.bottomright_status = False

        self.retranslateUi(MainWindow)

    def check_state(self,b):
        if b.text() == "Multiple-Monitors":
            if b.isChecked() == True:
                self.monitor_0.setEnabled(True)
                self.monitor_1.setEnabled(True)
                self.monitor_helper.setEnabled(True)
            else:
                self.monitor_0.setChecked(False)
                self.monitor_0.setEnabled(False)
                self.monitor_1.setEnabled(False)
                self.monitor_1.setChecked(False)
                self.monitor_helper.setEnabled(False)
				
        if b.text() == "|1|2|":
            if b.isChecked() == True:
                self.monitor_state = 0
                self.monitor_1.setEnabled(False)
            else:
                self.monitor_state = 1
                self.monitor_1.setEnabled(True)

        if b.text() == "|2|1|":
            if b.isChecked() == True:
                self.monitor_state = 1
                self.monitor_0.setEnabled(False)
            else:
                self.monitor_state = 0
                self.monitor_0.setEnabled(True)

    def signal_stop(self):
        self.status.setText("Status : Waiting...")
        self.worker.check(False)

    def signal_start(self):
        self.status.setText("Status : Working.")
        self.worker.check(True)

    def add_text(self,text):
        self.textBrowser.setText(text)
        
    def stop_thread(self):
        self.stop_signal.emit()
        
    def b_translate(self):
        if self.topleft_status == False and self.bottomright_status == False:
            QMessageBox.about(MainWindow,"Error !", "Coordinate setup needed !")
        else:
            self.worker.set_coordinates(self.top_left.x, self.top_left.y, self.bottom_right.x, self.bottom_right.y,self.language_1.text(),self.language_2.text(),self.monitor_state)
            MainWindow.setFixedSize(800, 600)
            MainWindow.setStyleSheet("background-color: rgb(67, 67, 67);")
            self.stackedWidget.setCurrentIndex(1)

            if os.path.exists('C:\\Users\\'+ username +'\\AppData\\Local\\Programs\\Tesseract-OCR\\tesseract.exe'):
                pytesseract.pytesseract.tesseract_cmd = 'C:\\Users\\'+ username +'\\AppData\\Local\\Programs\\Tesseract-OCR\\tesseract.exe'

            elif os.path.exists('C:\\Program Files\\Tesseract-OCR\\tesseract.exe'):
                pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

            else:
                QMessageBox.about(MainWindow,"Error !", "Tesseract Not Found !")
                exit() 
            
    def b_back(self):
        MainWindow.setStyleSheet("background-color: rgb(202, 202, 202);")
        MainWindow.setFixedSize(600, 350)
        self.stackedWidget.setCurrentIndex(0)

    def setup(self):

        self.topleft_status = False
        self.bottomright_status = False
    
        self.topleft_coordinate.setText("Coordinates : Waiting...")
        self.bottomright_coordinate.setText("Coordinates : Waiting...")

        while True:
            if keyboard.is_pressed('-') and self.topleft_status == False:
                self.top_left = pyautogui.position()
                self.topleft_status = True
                self.topleft_coordinate.setText("Coordinates : "+str(self.top_left.x)+","+str(self.top_left.y)+" OK.")

            if keyboard.is_pressed('+') and self.bottomright_status == False:
                self.bottom_right = pyautogui.position()
                self.bottomright_status = True
                self.bottomright_coordinate.setText("Coordinates : "+str(self.bottom_right.x)+","+str(self.bottom_right.y)+" OK.")
                
            if self.bottomright_status == True and self.topleft_status == True :
                self.coordinate_status.setText("Coordinates OK.")
                self.worker.set_coordinates(self.top_left.x, self.top_left.y, self.bottom_right.x, self.bottom_right.y,self.language_1.text(),self.language_2.text(),self.monitor_state)
                break

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Translater"))
        self.translate_button.setText(_translate("MainWindow", "Translate"))
        self.bottomright.setText(_translate("MainWindow", "Bottom Right"))
        self.topleft.setText(_translate("MainWindow", "Top Left"))
        self.topleft_coordinate.setText(_translate("MainWindow", "Coordinates :"))
        self.bottomright_coordinate.setText(_translate("MainWindow", "Coordinates :"))
        self.coordinate_status.setText(_translate("MainWindow", "Looking for coordinates"))
        self.setup_button.setText(_translate("MainWindow", "Setup"))
        self.language_1.setText(_translate("MainWindow", "eng"))
        self.label.setText(_translate("MainWindow", "to"))
        self.language_2.setText(_translate("MainWindow", "tr"))
        self.label_3.setText(_translate("MainWindow", "Language Settings"))
        self.back_button.setText(_translate("MainWindow", "Back"))
        self.start_button.setText(_translate("MainWindow", "Start"))
        self.stop_button.setText(_translate("MainWindow", "Stop"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())