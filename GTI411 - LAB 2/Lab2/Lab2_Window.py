# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Lab2_Window.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


import cv2
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap, QDoubleValidator
from PyQt5.QtWidgets import QFileDialog
from PIL import Image

from Lab2.views import SpatialFilterWidget, CannyFilterWidget, FrequencyFilterWidget
from Lab2.events import event_manager


class Ui_Lab2_Window(object):
    imageAdded = False
    src = np.zeros((200, 200, 4), np.uint8)
    isJpg = False

    def display_Image(self, fileName):
        self.src = cv2.imread(fileName, cv2.IMREAD_UNCHANGED)
        # afficher l'image originale
        pixmap = QPixmap(fileName)
        self.label_3.setPixmap(pixmap)
        self.imageAdded = True

    def openImage(self):
        # read image from file dialog window
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getOpenFileName(self.centralwidget, "Open Image", "",
                                                  "Images (*.jpg);;Images (*.png);;All Files (*)", options=options)
        event_manager.trigger("on_load_image", filename)


    def filterChanged(self):
        if (self.comboBox_5.currentText() == 'Mean'):
            self.lineEdit.setText('0,11')
            self.lineEdit_2.setText('0,11')
            self.lineEdit_3.setText('0,11')
            self.lineEdit_4.setText('0,11')
            self.lineEdit_5.setText('0,11')
            self.lineEdit_6.setText('0,11')
            self.lineEdit_7.setText('0,11')
            self.lineEdit_8.setText('0,11')
            self.lineEdit_9.setText('0,11')
            self.lineEdit.setEnabled(False)
            self.lineEdit_2.setEnabled(False)
            self.lineEdit_3.setEnabled(False)
            self.lineEdit_4.setEnabled(False)
            self.lineEdit_5.setEnabled(False)
            self.lineEdit_6.setEnabled(False)
            self.lineEdit_7.setEnabled(False)
            self.lineEdit_8.setEnabled(False)
            self.lineEdit_9.setEnabled(False)
        else:
            self.lineEdit.setText('')
            self.lineEdit_2.setText('')
            self.lineEdit_3.setText('')
            self.lineEdit_4.setText('')
            self.lineEdit_5.setText('')
            self.lineEdit_6.setText('')
            self.lineEdit_7.setText('')
            self.lineEdit_8.setText('')
            self.lineEdit_9.setText('')
            self.lineEdit.setEnabled(True)
            self.lineEdit_2.setEnabled(True)
            self.lineEdit_3.setEnabled(True)
            self.lineEdit_4.setEnabled(True)
            self.lineEdit_5.setEnabled(True)
            self.lineEdit_6.setEnabled(True)
            self.lineEdit_7.setEnabled(True)
            self.lineEdit_8.setEnabled(True)
            self.lineEdit_9.setEnabled(True)

    def applyFilter(self):
        if (str(self.comboBox_5.currentText()) == 'Mean' and str(self.comboBox_7.currentText()) == '0' and str(
                self.comboBox_6.currentText()) == 'Clamp 0 ... 255' and self.imageAdded):
            # appliquer le filtre moyenneur 3*3
            blur = cv2.blur(self.src, (3, 3))
            # clamp 0 ... 255
            for i in range(len(blur)):
                for j in range(len(blur[0])):
                    pixel_b = blur[i][j][0]
                    pixel_g = blur[i][j][1]
                    pixel_r = blur[i][j][2]
                    if (pixel_b < 0 and pixel_g < 0 and pixel_r < 0):
                        blur[i][j] = [0, 0, 0]
                        if (self.isJpg == False): #image png
                            alpha = blur[i][j][3]
                            blur[i][j] = [0, 0, 0, alpha]
                        print('valeur inférieure à 0 trouvée')
                    if (pixel_b > 255 and pixel_g > 255 and pixel_r > 255):
                        blur[i][j] = [255, 255, 255]
                        if (self.isJpg == False): #image png
                            alpha = blur[i][j][3]
                            blur[i][j] = [255, 255, 255, alpha]
                        print('valeur supérieure à 255 trouvée')
            # border
            #jpg image has 3 channels
            if (self.isJpg == True):
                blur[0] = [0, 0, 0]  # ligne y = 0
                blur[blur.shape[0] - 1] = [0, 0, 0]  # ligne y = (height - 1)
                blur[:, 0] = [0, 0, 0]  # colonne x = 0
                blur[:, blur.shape[1] - 1] = [0, 0, 0]  # colonne y = (width - 1)
                cv2.imwrite('blurred_image.jpg', blur)
                # afficher l'image filtrée
                pixmap = QPixmap('blurred_image.jpg')
                self.label_21.setPixmap(pixmap)
            # png image has 4 channels
            if (self.isJpg == False):
                blur[0] = [0, 0, 0, 255]  # ligne y = 0
                blur[blur.shape[0] - 1] = [0, 0, 0, 255]  # ligne y = (height - 1)
                blur[:, 0] = [0, 0, 0, 255]  # colonne x = 0
                blur[:, blur.shape[1] - 1] = [0, 0, 0, 255]  # colonne y = (width - 1)
                cv2.imwrite('blurred_image.png', blur)
                # afficher l'image filtrée
                pixmap = QPixmap('blurred_image.png')
                self.label_21.setPixmap(pixmap)

    def setupUi(self, Lab2_Window):
        Lab2_Window.setObjectName("Lab2_Window")
        #Lab2_Window.resize(832, 629)
        Lab2_Window.showMaximized()
        self.centralwidget = QtWidgets.QWidget(Lab2_Window)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        
        self.partie1 = SpatialFilterWidget()
        self.partie1.setObjectName("partie1")
        self.tabWidget.addTab(self.partie1, "")

        self.partie2 = CannyFilterWidget()
        self.partie2.setObjectName("partie2")
        self.tabWidget.addTab(self.partie2, "")

        self.partie3 = FrequencyFilterWidget()
        self.partie1.setObjectName("partie3")
        self.tabWidget.addTab(self.partie3, "")

        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)
        Lab2_Window.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(Lab2_Window)
        self.statusbar.setObjectName("statusbar")
        Lab2_Window.setStatusBar(self.statusbar)
        self.menuBar = QtWidgets.QMenuBar(Lab2_Window)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 832, 21))
        self.menuBar.setObjectName("menuBar")
        self.menuFile = QtWidgets.QMenu(self.menuBar)
        self.menuFile.setObjectName("menuFile")
        self.menuFilter = QtWidgets.QMenu(self.menuBar)
        self.menuFilter.setObjectName("menuFilter")
        Lab2_Window.setMenuBar(self.menuBar)
        self.actionExit = QtWidgets.QAction(Lab2_Window)
        self.actionExit.setObjectName("actionExit")
        self.actionAdd_Image = QtWidgets.QAction(Lab2_Window)
        self.actionAdd_Image.setObjectName("actionAdd_Image")
        self.actionApply_Filter = QtWidgets.QAction(Lab2_Window)
        self.actionApply_Filter.setObjectName("actionApply_Filter")
        self.menuFile.addAction(self.actionExit)
        self.menuFilter.addAction(self.actionAdd_Image)
        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuBar.addAction(self.menuFilter.menuAction())
        
        self.actionAdd_Image.triggered.connect(self.openImage)

        self.retranslateUi(Lab2_Window)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Lab2_Window)

    def retranslateUi(self, Lab2_Window):
        _translate = QtCore.QCoreApplication.translate
        Lab2_Window.setWindowTitle(_translate("Lab2_Window", "Lab2_Window"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.partie1), _translate("Lab2_Window", "Spatial Filters"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.partie2), _translate("Lab2_Window", "Canny Algorithm"))

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.partie3), _translate("Lab2_Window", "Frequency Filters"))
        self.menuFile.setTitle(_translate("Lab2_Window", "File"))
        self.menuFilter.setTitle(_translate("Lab2_Window", "Add"))
        self.actionExit.setText(_translate("Lab2_Window", "Exit"))
        self.actionAdd_Image.setText(_translate("Lab2_Window", "Add Image"))
        self.actionApply_Filter.setText(_translate("Lab2_Window", "Apply Filter"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Lab2_Window = QtWidgets.QMainWindow()
    ui = Ui_Lab2_Window()
    ui.setupUi(Lab2_Window)
    Lab2_Window.show()
    sys.exit(app.exec_())
