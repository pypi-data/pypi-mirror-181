from malt.movable_objects import SQ
from malt.bounding_object_cache import BoundingObjectCache
from PySide6.QtCore import QCoreApplication
from PySide6.QtWidgets import QFileDialog, QGraphicsScene
from malt.object_detector import ObjectDetector
import uuid


class ImageManager:
    def __init__(self, video_manager) -> None:
        self.object_detector = ObjectDetector()
        self.current_label = None
        self.current_frame = None
        self.current_frame_index = None
        self.saved_image_dir = None
        self.saved_voc_dir = None
        self.cache = BoundingObjectCache()
        self.focus_boxes = set()
        self.current_pix_map = None
        self.video_manager = video_manager
        self.ui = video_manager.parent.ui
        self.scene = QGraphicsScene()
        self.ui.newBoxButton.clicked.connect(self.manage_box_button_click)
        self.ui.setLabelButton.clicked.connect(self.set_label)
        self._set_defaults("Not Set")
        self.ui.setVoc.clicked.connect(self.set_voc_foler)
        self.ui.setImg.clicked.connect(self.set_saved_image_dir)
        self.ui.pushButton_2.clicked.connect(self.set_model)
        self.ui.pushButton_3.clicked.connect(self.save)

    def save(self):
        if (
            self.saved_image_dir != None
            and self.saved_voc_dir != None
            and self.current_label != None
        ):
            self.cache.save_data(
                self.saved_image_dir, self.saved_voc_dir, self.current_label
            )
            self._set_unsaved_mods_text(f"No Unsaved Changes")

        else:
            print("issue")

    def maybe_set_current_label(self, name):
        if name and not self.ui.checkBox.isChecked():
            self.ui.textEdit.setText(name)
            self.set_label()

    def set_model(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self.video_manager.parent,
            "Select video media",
            ".",
            "ModelFiles (*.tflite)",
        )
        if file_path:
            self.object_detector.set_detector(file_path)
            model_name = file_path.split("/")[-1]
            self._set_model_target_text(model_name)

    def set_voc_foler(self):
        folder = str(
            QFileDialog.getExistingDirectory(
                self.video_manager.parent, "Select Directory"
            )
        )
        if folder:
            self.saved_voc_dir = folder
            if len(folder) > 15:
                folder = folder[-15:]
            self._set_voc_target_text(folder)

    def set_saved_image_dir(self):
        folder = str(
            QFileDialog.getExistingDirectory(
                self.video_manager.parent, "Select Directory"
            )
        )
        if folder:
            self.saved_image_dir = folder
            if len(folder) > 15:
                folder = folder[-15:]
            self._set_img_target_text(folder)

    def set_object_focus(self, id: str, focus: bool = True):
        if focus:
            self.focus_boxes.add(id)
            self._set_new_box_text("Delete Box")
        else:
            if id in self.focus_boxes:
                self.focus_boxes.remove(id)
            if len(self.focus_boxes) == 0:
                self._set_new_box_text("New Box")

    def delete_boxes(self):
        for id in self.focus_boxes:
            self.cache.remove_box(id)
        self.focus_boxes.clear()
        self._set_new_box_text("New Box")

    def manage_box_button_click(self):
        if len(self.focus_boxes) > 0:
            self.delete_boxes()
            return
        self.draw_new_box()

    def draw_new_box(self):
        if self.current_pix_map is not None:
            sq = SQ(self, self.current_frame, self.current_frame_index)
            self.cache.add_box(sq)

    def update_focus_image(self, pixmap, frame, frame_index):
        self.current_pix_map = pixmap
        self.current_frame = frame
        self.current_frame_index = frame_index
        self.scene.addItem(pixmap)
        self.add_boxes(frame_index)

    def add_boxes(self, index):
        boxes = self.cache.get_all_boxes_from_index(index)
        has_boxes = False
        for id, box in boxes.items():
            has_boxes = True
            sq = SQ(self, self.current_frame, index, id, box)
            self.cache.add_sq_box_only(sq)
        if not has_boxes:
            self.add_object_detection_boxes(index)

    def add_object_detection_boxes(self, index):
        if self.object_detector.detector:
            detections = self.object_detector.get_detected_loc_info(self.current_frame)
            for detection in detections:
                id = str(uuid.uuid4())
                self.add_sq(index, id, detection)
            print(detections)

    def add_sq(self, index, id, box):
        sq = SQ(self, self.current_frame, index, id, box)
        self.cache.add_sq_box_only(sq)

    def update_box_loc(self, index, id, locinfo):
        self.cache.update(index, id, locinfo, self.current_frame, self.current_label)
        unsaved = len(self.cache.not_yet_saved)
        if unsaved == 0:
            unsaved = "No"
        self._set_unsaved_mods_text(f"{unsaved} Unsaved Changes")

    def set_label(self):
        text = self.ui.textEdit.toPlainText()
        if text != "":
            self.current_label = text
            self._set_label_text(self.current_label)
            for id in self.focus_boxes:
                box = self.cache.get_box(id)
                box.update_label(text)

    def _set_defaults(self, text):
        self._set_label_text(text)
        self._set_model_target_text(text)
        self._set_img_target_text(text)
        self._set_vid_target_text(text)
        self._set_voc_target_text(text)
        self._set_unsaved_mods_text("No Unsaved Changes")

    def _set_label_text(self, text):
        self.ui.currentLabelTarget.setText(
            QCoreApplication.translate("MainWindow", text, None)
        )

    def _set_model_target_text(self, text):
        self.ui.modelTarget.setText(
            QCoreApplication.translate("MainWindow", text, None)
        )

    def _set_vid_target_text(self, text):
        self.ui.vidTarget.setText(QCoreApplication.translate("MainWindow", text, None))

    def _set_unsaved_mods_text(self, text):
        self.ui.unsavedMods.setText(
            QCoreApplication.translate("MainWindow", text, None)
        )

    def _set_img_target_text(self, text):
        self.ui.imgTarget.setText(QCoreApplication.translate("MainWindow", text, None))

    def _set_voc_target_text(self, text):
        self.ui.vocTarget.setText(QCoreApplication.translate("MainWindow", text, None))

    def _set_new_box_text(self, text):
        self.ui.newBoxButton.setText(
            QCoreApplication.translate("MainWindow", text, None)
        )

    def clear_sq_holder(self):
        self.cache.clear_sq()
