    # Copyright (C) 2017  Ahmed Abdelkareem <eng.a7mad93@gmail.com>
    #
    # This program is free software: you can redistribute it and/or modify
    # it under the terms of the GNU General Public License as published by
    # the Free Software Foundation, either version 3 of the License, or
    # (at your option) any later version.
    #
    # This program is distributed in the hope that it will be useful,
    # but WITHOUT ANY WARRANTY; without even the implied warranty of
    # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    # GNU General Public License for more details.
    #
    # You should have received a copy of the GNU General Public License
    # along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Importing the required modules
import requests
from time import sleep
import socket
from bs4 import BeautifulSoup
import re
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QFileDialog, QMessageBox, QDialog

global allMails
allMails = []  # The list that will contain the found emails
openedFile = ""  # The file name for the file to search in for emails
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8

    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

# Defining the UI window class


class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(460, 280)
        MainWindow.setMinimumSize(QtCore.QSize(460, 280))
        MainWindow.setMaximumSize(QtCore.QSize(460, 280))
        MainWindow.setBaseSize(QtCore.QSize(300, 100))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("icons/iconbig.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayoutWidget = QtGui.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 0, 451, 234))
        self.gridLayoutWidget.setObjectName(_fromUtf8("gridLayoutWidget"))
        self.gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(-1, 7, -1, -1)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_2 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_2.setIndent(5)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.pushButton = QtGui.QPushButton(self.gridLayoutWidget)  # The browse button
        self.pushButton.clicked.connect(self.browse)   # Adding the function browse to the pushbutton
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.gridLayout.addWidget(self.pushButton, 1, 3, 1, 1)
        self.lineEdit = QtGui.QLineEdit(self.gridLayoutWidget)  # The text box for the URL
        self.lineEdit.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.lineEdit.setFocus()                  # Setting focus for lineEdit
        self.lineEdit.setPlaceholderText("http://www.example.com")  # Setting a placerholder for an example url
        self.lineEdit.returnPressed.connect(self.find)  # To run the find fuction when the user press after writting in the lineEdit
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.gridLayout.addWidget(self.lineEdit, 0, 2, 1, 1)
        self.lineEdit_2 = QtGui.QLineEdit(self.gridLayoutWidget)  # The text box for the browsed file ( The file to search in)
        self.lineEdit_2.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.lineEdit_2.returnPressed.connect(self.find)
        self.lineEdit_2.setObjectName(_fromUtf8("lineEdit_2"))
        self.gridLayout.addWidget(self.lineEdit_2, 1, 2, 1, 1)       
        self.label = QtGui.QLabel(self.gridLayoutWidget)
        self.label.setIndent(5)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.pushButton_2 = QtGui.QPushButton(self.gridLayoutWidget)  # The find pushbutton
        self.pushButton_2.clicked.connect(self.find)  # Adding the function find to the pushbutton
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.gridLayout.addWidget(self.pushButton_2, 3, 2, 1, 1)
        self.textBrowser = QtGui.QTextBrowser(self.gridLayoutWidget)
        self.textBrowser.setObjectName(_fromUtf8("textBrowser"))
        self.gridLayout.addWidget(self.textBrowser, 2, 2, 1, 1)
        self.pushButton_3 = QtGui.QPushButton(self.gridLayoutWidget)  # The save pushbutton
        self.pushButton_3.setEnabled(False)  # Making the pushbutton disabled in the beginning
        self.pushButton_3.clicked.connect(self.save)  # Adding the function save to the pushbutton
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.gridLayout.addWidget(self.pushButton_3, 3, 3, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 460, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuAbout = QtGui.QMenu(self.menubar)
        self.menuAbout.setObjectName(_fromUtf8("menuAbout"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionSave = QtGui.QAction(MainWindow)
        self.actionSave.setObjectName(_fromUtf8("actionSave"))
        self.actionSave.setShortcut("Ctrl+s")  # Setting ctrl+s as a shortcut for save
        self.actionSave.triggered.connect(self.save)
        self.actionExit = QtGui.QAction(MainWindow)
        self.actionExit.setObjectName(_fromUtf8("actionExit"))
        self.actionExit.triggered.connect(QtGui.qApp.quit)  # Setting the action Exit in the file menu to exit the application
        self.actionAbout = QtGui.QAction(MainWindow)
        self.actionAbout.setObjectName(_fromUtf8("actionAbout"))
        self.actionAbout.triggered.connect(self.about)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionExit)
        self.menuAbout.addAction(self.actionAbout)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Email Find", None))
        self.label_2.setText(_translate("MainWindow", "File", None))
        self.pushButton.setText(_translate("MainWindow", "Browse", None))
        self.label.setText(_translate("MainWindow", "URL", None))
        self.pushButton_2.setText(_translate("MainWindow", "Find", None))
        self.pushButton_3.setText(_translate("MainWindow", "Save", None))
        self.menuFile.setTitle(_translate("MainWindow", "File", None))
        self.menuAbout.setTitle(_translate("MainWindow", "About", None))
        self.actionSave.setText(_translate("MainWindow", "Save", None))
        self.actionExit.setText(_translate("MainWindow", "Exit", None))
        self.actionAbout.setText(_translate("MainWindow", "About", None))

    # Defining the functions of the program

    def isConnected(self, REMOTE_SERVER):
        try:
            # see if we can resolve the host name -- tells us if there is
            # a DNS listening
            host = socket.gethostbyname(REMOTE_SERVER)

            return True
        except:
            pass
        return False

    # For displaying error messages
    def error(self, text, informtxt, title):
        sleep(0.3)  # Waiting a little before showing the error popup, thrust me it is better
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(text)
        msg.setInformativeText(informtxt)
        msg.setWindowTitle(title)
        msg.setStandardButtons(QMessageBox.Ok)
        retval = msg.exec_()  # The returned value when clicking the ok button (not used but needed for the program to work)

    def browse(self):
        dlg = QFileDialog()
        dlg.setAcceptMode(QFileDialog.AcceptOpen)
        self.lineEdit_2.setText(dlg.getOpenFileName(None,"Open File","","Text Files (*.txt)"))

    def find(self):
        global allMails
        allMails = []
        countFalse = 0 # Counts false mails
        openedFile = self.lineEdit_2.text()  # The file to search in
        url = self.lineEdit.text().strip()  # The url to webpage to search in
        netStauts = self.isConnected('www.google.com')  # The status of the internet connection by trying to connect to google
        regex = r'\b[\w.-]+?@\w+?\.\w+?\b' # The email pattern using regular expressions


        if netStauts is False:
            self.error("Error Message:", "There is no internet connection, Try again when you have a proper connection",
                       "Error")
        else:

            if url == "" and openedFile == "":
                self.error("Error Message:", "You must enter a URL or a File name.", "Error")

            if url != "" and openedFile != "":
                self.error("Error Message:", "You can't use both URL and File in the same time.", "Error")
            

            if url != "" and openedFile == "":  # Which means when url is not empty

                try:
                        
                    if not (url.startswith("http://") or url.startswith("https://")):
                        url = "http://" + url
                    source_code = requests.get(url)  # Getting the webpage source code object
                    self.textBrowser.append("Please wait while finding email addresses ....")  # Message for the user to wait until emails are found
                    plain_text = source_code.text    # Getting the webpage source code as plain text
                    soup = BeautifulSoup(plain_text, "html.parser")  # Getting the source code clean and ready to be used
                    allMails = re.findall(regex, str(soup))     # Finding emails in

                    # Sometimes an image name in the website looks like emails (eg. imag1@.png) so it
                    # needs to be excluded from the allMails list
                    for i in allMails:
                        if i.endswith(".png") or i.endswith(".jpg") or i.endswith(".jpeg") or i.endswith(".gif"):
                            countFalse = countFalse + 1


                    self.textBrowser.append(str(str(len(allMails) - countFalse) + " email(s) were found.")) # Displaying the number of found emails

                except:
                    self.error("URL Error:", "Could not connect to that url, check if it is written right.", "Error")

            if openedFile != "" and url == "":  # which means there is a chosen file

               try:
                    with open(openedFile, "r") as infile:
                        self.textBrowser.append("Please wait while finding email addresses ....")
                        while True:
                            lines = infile.readlines(65536)
                            if not lines:
                                break  # Break the while loop when there is no new lines in the file
                            for line in lines:
                                x = re.findall(regex, line)
                                allMails = allMails + x
                    self.textBrowser.append(str(str(len(allMails) - countFalse) + " email(s) were found."))
               except:
                   self.error("File Error:", "Could not open "+openedFile, "Error")

            
            
            if len(allMails) > 0:
                self.pushButton_3.setEnabled(True)  # If there are emails found activate the save button
            else:
                self.pushButton_3.setEnabled(False)  # If not return the save button to disabled

            return allMails

    def save(self):
        global allMails

        if len(allMails) > 0:
            dlg = QFileDialog()  # Dialog to save the file
            dlg.setAcceptMode(QFileDialog.AcceptSave)
            saveFile = QFileDialog.getSaveFileName(None,"Save File","","Text Files (*.txt)")
            with open(saveFile, 'w', encoding="UTF-8") as file:
                for i in allMails:
                    file.write(str(i) + "\n")
        else:
            self.error("Save Error:", "No emails were found to save!", "Error")
            

    def about(self):  # The About dialog
        Dialog = QDialog()
        Dialog.resize(341, 251)
        Dialog.setMinimumSize(QtCore.QSize(341, 251))
        Dialog.setMaximumSize(QtCore.QSize(341, 251))
        Dialog.setBaseSize(QtCore.QSize(341, 251))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("icons/iconbig.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        self.textEdit = QtGui.QTextEdit(Dialog)
        self.textEdit.setGeometry(QtCore.QRect(0, 0, 341, 251))
        self.textEdit.setAutoFillBackground(False)
        self.textEdit.setReadOnly(True)
        Dialog.setWindowTitle(_translate("Dialog", "About", None))
        self.textEdit.setHtml(_translate("Dialog",
                                         "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                         "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                         "p, li { white-space: pre-wrap; }\n"
                                         "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
                                         "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt; font-weight:600; text-decoration: underline;\">Email Find v1.0</span></p>\n"
                                         "<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:14pt;\"><br /></p>\n"
                                         "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">It is a Freeware to extract email addresses from webpages and files.</span></p>\n"
                                         "<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:14pt;\"><br /></p>\n"
                                         "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">Programmed By / </span><span style=\" font-size:14pt; font-weight:600;\">Ahmed Abdelkareem</span><span style=\" font-size:14pt;\"> &lt;eng.a7mad93@gmail.com&gt;</span></p>\n"
                                         "<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:14pt;\"><br /></p>\n"
                                         "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">Under GNU/GPLv3</span></p></body></html>",
                                         None))

        Dialog.show()
        Dialog.exec_()
