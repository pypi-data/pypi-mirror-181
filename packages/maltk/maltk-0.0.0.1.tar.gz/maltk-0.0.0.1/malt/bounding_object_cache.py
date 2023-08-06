from malt.movable_objects import SQ, LocInfo

import cv2
from dataclasses import dataclass
from pascal_voc_writer import Writer
import uuid
import numpy as np


@dataclass
class FrameIndex:
    frame: np.ndarray
    index: int
    cords: LocInfo
    label: str = None


class BoundingObjectCache:
    def __init__(self):
        self.current_sq_holder = {}
        self.cached_changes = {}
        self.not_yet_saved = {}

    def remove_box(self, id: str):
        if id in self.current_sq_holder:
            sq = self.current_sq_holder[id]
            if (self.cached_changes.get(sq.index, {}) or {}).get(id):
                del self.cached_changes[sq.index][id]
                del self.not_yet_saved[id]
            self.current_sq_holder[id].delete()
            del self.current_sq_holder[id]

    def add_box(self, box: SQ):
        self.current_sq_holder[box.id] = box
        if box.index not in self.cached_changes:
            self.cached_changes[box.index] = {}
        self.cached_changes[box.index][box.id] = box.cv_cords
        self.not_yet_saved[box.id] = FrameIndex(
            box.frame, box.index, box.cv_cords, box.image_manager.current_label
        )

    def get_all_boxes_from_index(self, index: int):
        boxes = self.cached_changes.get(index, {}) or {}
        return boxes

    def get_box(self, id: str):
        return self.current_sq_holder[id]

    def clear_sq(self):
        for sq in self.current_sq_holder.values():
            sq.delete()
        self.current_sq_holder.clear()

    def update(self, index, id, locinfo, frame, label):
        if index not in self.cached_changes:
            self.cached_changes[index] = {}
        self.cached_changes[index][id] = locinfo
        self.not_yet_saved[id] = FrameIndex(frame, index, locinfo, label)

    def add_sq_box_only(self, sq):
        self.current_sq_holder[sq.id] = sq

    def save_data(self, image_path: str, voc_path: str, backup_label: str):
        indexs = {}
        for key, value in self.not_yet_saved.items():
            if value.index not in indexs:
                indexs[value.index] = []
            indexs[value.index].append(value)

        for index, frame_list in indexs.items():
            first_frame = frame_list[0].frame
            image_id = str(uuid.uuid4())
            if image_path[-1] != "/":
                image_path = image_path + "/"
            if voc_path[-1] != "/":
                voc_path = voc_path + "/"
            img = f"{image_path}{index}_{image_id}.jpg"
            voc = f"{voc_path}{index}_{image_id}.xml"
            print(img, voc)
            cv2.imwrite(img, first_frame)
            h, w, _ = first_frame.shape
            pascal_writer = Writer(img, w, h)
            for frame_index_item in frame_list:
                assert np.array_equal(first_frame, frame_index_item.frame)
                pascal_writer.addObject(
                    frame_index_item.label if frame_index_item.label else backup_label,
                    int(frame_index_item.cords.x),
                    int(frame_index_item.cords.y),
                    int(frame_index_item.cords.xmax),
                    int(frame_index_item.cords.ymax),
                )
                print(pascal_writer)
            pascal_writer.save(voc)
        self.not_yet_saved.clear()
