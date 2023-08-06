from PySide6.QtWidgets import QFileDialog, QGraphicsPixmapItem
from PySide6.QtCore import Qt, QCoreApplication
from PySide6.QtGui import QImage, QPixmap
from malt.image_manager import ImageManager
from malt.movable_objects import SQ

import cv2


class VideoManager:
    video_path = None
    video_file_name = None
    clean_video_name = None
    cap = None
    cap_len = None
    scroller_ratio = 0
    frame_bump = 0
    max_frames = 50
    last_img = None
    last_frame_index = 0
    painter = None
    last_rolling_index = 0

    def __init__(self, parent) -> None:
        self.parent = parent
        self.parent.ui.pushButton.clicked.connect(self.set_video)
        self.parent.ui.navFrame.mouseMoveEvent = self.set_frame
        self.parent.ui.mainFrame.resizeEvent = self.resize_img
        self.parent.ui.navFrame.mouseReleaseEvent = self.set_frame_list
        self.parent.listWidget.currentItemChanged.connect(self.new_frame_click)
        self.image_manager = ImageManager(self)
        self.scene = self.image_manager.scene

    def pass_keypress(self, event):
        command = event.text()
        event_key = event.key()

        print(command, event_key)
        if command == "n":
            self.set_next_item()
        if command == "b":
            self.go_back_an_item()

        if event_key == 16777219 or event_key == 16777223:  # delete keys
            self.image_manager.delete_boxes()

        if command == "d":
            self.image_manager.draw_new_box()

    def go_back_an_item(self):
        if self.parent.listWidget.currentRow() > 0:
            self.parent.listWidget.setCurrentRow(
                self.parent.listWidget.currentRow() - 1
            )

    def set_next_item(self):
        if self.parent.listWidget.currentRow() >= 0:
            self.parent.listWidget.setCurrentRow(
                self.parent.listWidget.currentRow() + 1
            )

    def new_frame_click(self, data=None):
        if data != None:
            index = int(data.text().split(" ")[-1])

            self.last_frame_index = index
            self.set_frame()

    def set_video(self):
        fileName, _ = QFileDialog.getOpenFileName(
            self.parent,
            "Select video media",
            ".",
            "Video Files (*.mp4 *.flv *.ts *.mts *.avi)",
        )
        if fileName:
            self.cap = cv2.VideoCapture(fileName)
            self.video_path = fileName
        if self.cap:
            self.cap_len = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
            self.video_file_name = fileName.split("/")[-1]
            self.clean_video_name = self.video_file_name.split(".")[0]
            self.set_video_scroller()
            self.parent.ui.vidTarget.setText(
                QCoreApplication.translate("MainWindow", self.video_file_name, None)
            )
            self.set_frame(move=False)

    def set_video_scroller(self):
        w = int(self.parent.ui.navFrame.width() - 1)
        if self.cap:
            self.scroller_ratio = self.cap_len / w
            self.frame_bump = int(w / self.max_frames)

    def set_frame(self, e=None, move=False):
        if self.cap:
            if e:
                n = int(e.x() * self.scroller_ratio) + (self.max_frames // 2)
                n = int(n - (n % self.max_frames))
                frame_index = int(n)
                if frame_index == self.last_rolling_index:
                    return
                else:
                    self.last_rolling_index = frame_index
            else:
                frame_index = self.last_frame_index
            frame = self.get_display_frame(frame_index)
            img = self.get_q_image(frame)
            self.scene.clear()
            self.parent.ui.mainFrame.setScene(self.scene)
            pic = QGraphicsPixmapItem()
            pic.setPixmap(QPixmap.fromImage(img))
            self.image_manager.clear_sq_holder()
            self.image_manager.update_focus_image(pic, frame, frame_index)

    def set_frame_list(self, e):
        if self.cap:
            self.parent.listWidget.clear()
            inc = self.parent.ui.skipBok.value() + 1
            i = self.last_frame_index
            for _ in range(self.parent.ui.spinBox.value()):
                if i < self.cap_len:
                    self.parent.listWidget.addItem(f"{self.clean_video_name} {i}")
                i += inc
            self.parent.listWidget.setCurrentRow(0)

    def get_display_frame(self, frame_index: int) -> QImage:
        """Gets the frame from the CV cap and converts it into a
        a QImage."""
        if frame_index > self.cap_len:
            frame_index = self.cap_len - 1
        if frame_index < 0:
            frame_index = 0
        self.last_frame_index = frame_index
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
        _, frame = self.cap.read()
        return frame

    def get_q_image(self, frame):
        color_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = color_frame.shape
        img = QImage(color_frame.data, w, h, ch * w, QImage.Format_RGB888)
        width, height = self.getFrameWH()
        return img.scaled(width, height, Qt.KeepAspectRatio)

    def resize_img(self, e):
        self.set_video_scroller()
        if self.cap:
            self.set_frame(move=True)

    def getFrameWH(self):
        h = self.parent.ui.mainFrame.height() - 5
        w = self.parent.ui.mainFrame.width() - 5
        return w, h
