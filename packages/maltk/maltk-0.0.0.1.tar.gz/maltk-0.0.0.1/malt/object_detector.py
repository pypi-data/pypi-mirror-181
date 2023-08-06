import cv2
from tflite_support.task import core
from tflite_support.task import processor
from tflite_support.task import vision

from malt.movable_objects import LocInfo


class ObjectDetector:
    def __init__(self):
        self.detector = None
        self.model_path = None
        self.max_results = 1
        self.score_threshold = 0.2
        self.num_threads = 4
        self.enable_edgetpu = False

    @property
    def base_options(self):
        if self.model_path:
            return core.BaseOptions(
                file_name=self.model_path,
                use_coral=self.enable_edgetpu,
                num_threads=self.num_threads,
            )

    @property
    def detection_options(self):
        return processor.DetectionOptions(
            max_results=self.max_results, score_threshold=self.score_threshold
        )

    @property
    def options(self):
        if self.model_path:
            return vision.ObjectDetectorOptions(
                base_options=self.base_options, detection_options=self.detection_options
            )

    def get_detection_results(self, frame):
        input_tensor = vision.TensorImage.create_from_array(frame)
        return self.detector.detect(input_tensor)

    def get_detected_loc_info(self, frame):
        detections = self.get_detection_results(frame)
        res = []
        if self.detector:
            detections = self.get_detection_results(frame)
            print(detections)
            for i, detection in enumerate(detections.detections):
                box = detection.bounding_box
                locinfo = LocInfo(
                    box.origin_x,
                    box.origin_y,
                    box.width,
                    box.height,
                    detection.categories[0].category_name,
                )
                res.append(locinfo)
        return res

    def set_detector(self, path: str):
        self.model_path = path
        self.detector = vision.ObjectDetector.create_from_options(self.options)
