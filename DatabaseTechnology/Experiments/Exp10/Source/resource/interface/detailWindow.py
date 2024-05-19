# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'detailWindowEkAapA.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class UI_DetailWindow(object):
    def setupUi(self, detailWindow):
        if not detailWindow.objectName():
            detailWindow.setObjectName(u"detailWindow")
        detailWindow.resize(480, 640)
        self.verticalLayout = QVBoxLayout(detailWindow)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.detailTable = QTableWidget(detailWindow)
        if (self.detailTable.columnCount() < 2):
            self.detailTable.setColumnCount(2)
        __qtablewidgetitem = QTableWidgetItem()
        self.detailTable.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.detailTable.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        self.detailTable.setObjectName(u"detail")

        self.verticalLayout.addWidget(self.detailTable)

        self.buttonZone = QWidget(detailWindow)
        self.buttonZone.setObjectName(u"buttonZone")
        self.horizontalLayout = QHBoxLayout(self.buttonZone)
        self.horizontalLayout.setSpacing(12)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.saveModify = QPushButton(self.buttonZone)
        self.saveModify.setObjectName(u"saveModify")

        self.horizontalLayout.addWidget(self.saveModify)

        self.close = QPushButton(self.buttonZone)
        self.close.setObjectName(u"pushButton")

        self.horizontalLayout.addWidget(self.close)


        self.verticalLayout.addWidget(self.buttonZone)


        self.retranslateUi(detailWindow)

        QMetaObject.connectSlotsByName(detailWindow)
    # setupUi

    def retranslateUi(self, detailWindow):
        detailWindow.setWindowTitle(QCoreApplication.translate("detailWindow", u"Form", None))
        ___qtablewidgetitem = self.detailTable.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("detailWindow", u"\u6761\u76ee", None));
        ___qtablewidgetitem1 = self.detailTable.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("detailWindow", u"\u5185\u5bb9", None));
        self.saveModify.setText(QCoreApplication.translate("detailWindow", u"\u4fdd\u5b58\u66f4\u6539", None))
        self.close.setText(QCoreApplication.translate("detailWindow", u"\u53d6\u6d88", None))
    # retranslateUi

