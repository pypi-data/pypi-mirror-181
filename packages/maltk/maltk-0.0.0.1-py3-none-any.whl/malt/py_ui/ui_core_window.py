# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'core_window.ui'
##
## Created by: Qt User Interface Compiler version 6.2.4
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (
    QCoreApplication,
    QDate,
    QDateTime,
    QLocale,
    QMetaObject,
    QObject,
    QPoint,
    QRect,
    QSize,
    QTime,
    QUrl,
    Qt,
)
from PySide6.QtGui import (
    QBrush,
    QColor,
    QConicalGradient,
    QCursor,
    QFont,
    QFontDatabase,
    QGradient,
    QIcon,
    QImage,
    QKeySequence,
    QLinearGradient,
    QPainter,
    QPalette,
    QPixmap,
    QRadialGradient,
    QTransform,
)
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QFrame,
    QGraphicsView,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QSpinBox,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1009, 713)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.mainFrameContainer = QFrame(self.centralwidget)
        self.mainFrameContainer.setObjectName("mainFrameContainer")
        self.mainFrameContainer.setFrameShape(QFrame.StyledPanel)
        self.mainFrameContainer.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.mainFrameContainer)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.mainFrame = QGraphicsView(self.mainFrameContainer)
        self.mainFrame.setObjectName("mainFrame")

        self.verticalLayout_3.addWidget(self.mainFrame)

        self.navFrame = QFrame(self.mainFrameContainer)
        self.navFrame.setObjectName("navFrame")
        self.navFrame.setMinimumSize(QSize(0, 25))
        self.navFrame.setMaximumSize(QSize(16777215, 30))
        self.navFrame.setStyleSheet("background-color:  rgb(25, 25, 25)")
        self.navFrame.setFrameShape(QFrame.StyledPanel)
        self.navFrame.setFrameShadow(QFrame.Raised)

        self.verticalLayout_3.addWidget(self.navFrame)

        self.horizontalLayout.addWidget(self.mainFrameContainer)

        self.info = QFrame(self.centralwidget)
        self.info.setObjectName("info")
        self.info.setMaximumSize(QSize(180, 16777215))
        self.info.setFrameShape(QFrame.StyledPanel)
        self.info.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.info)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setContentsMargins(2, 2, 2, 2)
        self.loader = QFrame(self.info)
        self.loader.setObjectName("loader")
        self.loader.setMinimumSize(QSize(0, 96))
        self.loader.setMaximumSize(QSize(16777215, 96))
        self.loader.setFrameShape(QFrame.StyledPanel)
        self.loader.setFrameShadow(QFrame.Raised)
        self.gridLayout = QGridLayout(self.loader)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.pushButton_2 = QPushButton(self.loader)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setMinimumSize(QSize(45, 45))
        self.pushButton_2.setIconSize(QSize(30, 16))

        self.gridLayout.addWidget(self.pushButton_2, 0, 0, 1, 1)

        self.pushButton = QPushButton(self.loader)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setMinimumSize(QSize(45, 45))

        self.gridLayout.addWidget(self.pushButton, 0, 1, 1, 1)

        self.setImg = QPushButton(self.loader)
        self.setImg.setObjectName("setImg")
        self.setImg.setMinimumSize(QSize(45, 45))
        font = QFont()
        font.setPointSize(13)
        self.setImg.setFont(font)
        self.setImg.setLayoutDirection(Qt.LeftToRight)
        self.setImg.setStyleSheet("padding: 2;")
        self.setImg.setIconSize(QSize(50, 50))

        self.gridLayout.addWidget(self.setImg, 1, 1, 1, 1)

        self.setVoc = QPushButton(self.loader)
        self.setVoc.setObjectName("setVoc")
        self.setVoc.setMinimumSize(QSize(45, 45))
        self.setVoc.setFont(font)
        self.setVoc.setStyleSheet("padding: 2;")
        self.setVoc.setIconSize(QSize(30, 60))

        self.gridLayout.addWidget(self.setVoc, 1, 0, 1, 1)

        self.verticalLayout.addWidget(self.loader)

        self.modelContainer = QFrame(self.info)
        self.modelContainer.setObjectName("modelContainer")
        self.modelContainer.setMinimumSize(QSize(0, 100))
        self.modelContainer.setMaximumSize(QSize(16777215, 100))
        self.modelContainer.setFrameShape(QFrame.StyledPanel)
        self.modelContainer.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.modelContainer)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.modelTxtBox = QFrame(self.modelContainer)
        self.modelTxtBox.setObjectName("modelTxtBox")
        self.modelTxtBox.setMinimumSize(QSize(0, 18))
        self.modelTxtBox.setFrameShape(QFrame.StyledPanel)
        self.modelTxtBox.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.modelTxtBox)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.modelName = QLabel(self.modelTxtBox)
        self.modelName.setObjectName("modelName")

        self.horizontalLayout_4.addWidget(self.modelName)

        self.modelTarget = QLabel(self.modelTxtBox)
        self.modelTarget.setObjectName("modelTarget")

        self.horizontalLayout_4.addWidget(self.modelTarget)

        self.verticalLayout_2.addWidget(self.modelTxtBox)

        self.vidTxtBox = QFrame(self.modelContainer)
        self.vidTxtBox.setObjectName("vidTxtBox")
        self.vidTxtBox.setMinimumSize(QSize(0, 18))
        self.vidTxtBox.setFrameShape(QFrame.StyledPanel)
        self.vidTxtBox.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.vidTxtBox)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.vidName = QLabel(self.vidTxtBox)
        self.vidName.setObjectName("vidName")

        self.horizontalLayout_5.addWidget(self.vidName)

        self.vidTarget = QLabel(self.vidTxtBox)
        self.vidTarget.setObjectName("vidTarget")

        self.horizontalLayout_5.addWidget(self.vidTarget)

        self.verticalLayout_2.addWidget(self.vidTxtBox)

        self.imgTxtBox = QFrame(self.modelContainer)
        self.imgTxtBox.setObjectName("imgTxtBox")
        self.imgTxtBox.setMinimumSize(QSize(0, 18))
        self.imgTxtBox.setFrameShape(QFrame.StyledPanel)
        self.imgTxtBox.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_6 = QHBoxLayout(self.imgTxtBox)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.imgName = QLabel(self.imgTxtBox)
        self.imgName.setObjectName("imgName")
        self.imgName.setFont(font)

        self.horizontalLayout_6.addWidget(self.imgName)

        self.imgTarget = QLabel(self.imgTxtBox)
        self.imgTarget.setObjectName("imgTarget")

        self.horizontalLayout_6.addWidget(self.imgTarget)

        self.verticalLayout_2.addWidget(self.imgTxtBox)

        self.vocTxtBox = QFrame(self.modelContainer)
        self.vocTxtBox.setObjectName("vocTxtBox")
        self.vocTxtBox.setMinimumSize(QSize(0, 18))
        self.vocTxtBox.setFrameShape(QFrame.StyledPanel)
        self.vocTxtBox.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_7 = QHBoxLayout(self.vocTxtBox)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.vocName = QLabel(self.vocTxtBox)
        self.vocName.setObjectName("vocName")

        self.horizontalLayout_7.addWidget(self.vocName)

        self.vocTarget = QLabel(self.vocTxtBox)
        self.vocTarget.setObjectName("vocTarget")

        self.horizontalLayout_7.addWidget(self.vocTarget)

        self.verticalLayout_2.addWidget(self.vocTxtBox)

        self.currentLabel = QFrame(self.modelContainer)
        self.currentLabel.setObjectName("currentLabel")
        self.currentLabel.setFrameShape(QFrame.StyledPanel)
        self.currentLabel.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.currentLabel)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, -1, 0)
        self.currentLabelName = QLabel(self.currentLabel)
        self.currentLabelName.setObjectName("currentLabelName")

        self.horizontalLayout_3.addWidget(self.currentLabelName)

        self.currentLabelTarget = QLabel(self.currentLabel)
        self.currentLabelTarget.setObjectName("currentLabelTarget")

        self.horizontalLayout_3.addWidget(self.currentLabelTarget)

        self.verticalLayout_2.addWidget(self.currentLabel)

        self.verticalLayout.addWidget(self.modelContainer)

        self.scrollArea = QScrollArea(self.info)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents_2 = QWidget()
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.scrollAreaWidgetContents_2.setGeometry(QRect(0, 0, 172, 177))
        self.scrollArea.setWidget(self.scrollAreaWidgetContents_2)

        self.verticalLayout.addWidget(self.scrollArea)

        self.frame = QFrame(self.info)
        self.frame.setObjectName("frame")
        self.frame.setMinimumSize(QSize(0, 260))
        self.frame.setMaximumSize(QSize(16777215, 260))
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.frame)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout_2.setContentsMargins(1, 1, 1, 1)
        self.frame_4 = QFrame(self.frame)
        self.frame_4.setObjectName("frame_4")
        self.frame_4.setMaximumSize(QSize(16777215, 65))
        self.frame_4.setStyleSheet("padding: 0;")
        self.frame_4.setFrameShape(QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.verticalLayout_9 = QVBoxLayout(self.frame_4)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.textEdit = QTextEdit(self.frame_4)
        self.textEdit.setObjectName("textEdit")

        self.verticalLayout_9.addWidget(self.textEdit)

        self.setLabelButton = QPushButton(self.frame_4)
        self.setLabelButton.setObjectName("setLabelButton")

        self.verticalLayout_9.addWidget(self.setLabelButton)

        self.gridLayout_2.addWidget(self.frame_4, 2, 0, 1, 2)

        self.frame_3 = QFrame(self.frame)
        self.frame_3.setObjectName("frame_3")
        self.frame_3.setMaximumSize(QSize(16777215, 100))
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.frame_3)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.spinBox = QSpinBox(self.frame_3)
        self.spinBox.setObjectName("spinBox")
        self.spinBox.setMaximum(1000)
        self.spinBox.setValue(50)

        self.verticalLayout_5.addWidget(self.spinBox)

        self.label_2 = QLabel(self.frame_3)
        self.label_2.setObjectName("label_2")

        self.verticalLayout_5.addWidget(self.label_2)

        self.gridLayout_2.addWidget(self.frame_3, 1, 1, 1, 1)

        self.frame_2 = QFrame(self.frame)
        self.frame_2.setObjectName("frame_2")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.frame_2)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.skipBok = QSpinBox(self.frame_2)
        self.skipBok.setObjectName("skipBok")

        self.verticalLayout_4.addWidget(self.skipBok)

        self.label = QLabel(self.frame_2)
        self.label.setObjectName("label")
        self.label.setAlignment(Qt.AlignCenter)

        self.verticalLayout_4.addWidget(self.label)

        self.gridLayout_2.addWidget(self.frame_2, 1, 0, 1, 1)

        self.checkBox = QCheckBox(self.frame)
        self.checkBox.setObjectName("checkBox")

        self.gridLayout_2.addWidget(self.checkBox, 3, 0, 1, 2)

        self.newBoxButton = QPushButton(self.frame)
        self.newBoxButton.setObjectName("newBoxButton")

        self.gridLayout_2.addWidget(self.newBoxButton, 5, 0, 1, 1)

        self.pushButton_3 = QPushButton(self.frame)
        self.pushButton_3.setObjectName("pushButton_3")
        font1 = QFont()
        font1.setPointSize(10)
        self.pushButton_3.setFont(font1)

        self.gridLayout_2.addWidget(self.pushButton_3, 5, 1, 1, 1)

        self.unsavedMods = QLabel(self.frame)
        self.unsavedMods.setObjectName("unsavedMods")

        self.gridLayout_2.addWidget(self.unsavedMods, 6, 0, 1, 2)

        self.verticalLayout.addWidget(self.frame)

        self.horizontalLayout.addWidget(self.info)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(
            QCoreApplication.translate("MainWindow", "MainWindow", None)
        )
        self.pushButton_2.setText(
            QCoreApplication.translate("MainWindow", "Model", None)
        )
        self.pushButton.setText(QCoreApplication.translate("MainWindow", "Video", None))
        self.setImg.setText(QCoreApplication.translate("MainWindow", "Img Dir", None))
        self.setVoc.setText(QCoreApplication.translate("MainWindow", "Voc Dir", None))
        self.modelName.setText(QCoreApplication.translate("MainWindow", "Model", None))
        self.modelTarget.setText(
            QCoreApplication.translate("MainWindow", "TextLabel", None)
        )
        self.vidName.setText(QCoreApplication.translate("MainWindow", "Video", None))
        self.vidTarget.setText(
            QCoreApplication.translate("MainWindow", "TextLabel", None)
        )
        self.imgName.setText(QCoreApplication.translate("MainWindow", "Img Dir", None))
        self.imgTarget.setText(
            QCoreApplication.translate("MainWindow", "TextLabel", None)
        )
        self.vocName.setText(QCoreApplication.translate("MainWindow", "Voc Dir", None))
        self.vocTarget.setText(
            QCoreApplication.translate("MainWindow", "TextLabel", None)
        )
        self.currentLabelName.setText(
            QCoreApplication.translate("MainWindow", "Current Label", None)
        )
        self.currentLabelTarget.setText(
            QCoreApplication.translate("MainWindow", "TextLabel", None)
        )
        self.setLabelButton.setText(
            QCoreApplication.translate("MainWindow", "Set Label", None)
        )
        self.label_2.setText(QCoreApplication.translate("MainWindow", "Batch", None))
        self.label.setText(QCoreApplication.translate("MainWindow", "Skip", None))
        self.checkBox.setText(
            QCoreApplication.translate("MainWindow", "Override Model Label", None)
        )
        self.newBoxButton.setText(
            QCoreApplication.translate("MainWindow", "New Box", None)
        )
        self.pushButton_3.setText(
            QCoreApplication.translate("MainWindow", "Save Mods", None)
        )
        self.unsavedMods.setText(
            QCoreApplication.translate("MainWindow", "TextLabel", None)
        )

    # retranslateUi
