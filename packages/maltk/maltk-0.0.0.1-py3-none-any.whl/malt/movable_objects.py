import sys
from PySide6.QtWidgets import QGraphicsEllipseItem, QGraphicsRectItem, QGraphicsTextItem
from PySide6.QtCore import Qt, QPointF
import uuid
from dataclasses import dataclass


class MovingObject(QGraphicsEllipseItem):
    def __init__(self, x, y, r, pixmap):
        super().__init__(0, 0, r, r)
        self.setPos(x, y)
        self.setBrush(Qt.green)
        self.setOpacity(0.2)
        self.setAcceptHoverEvents(True)
        self.max_width = pixmap.width
        self.max_height = pixmap.height

    def mousePressEvent(self, event):
        pass

    def mouseMoveEvent(self, event, outside_event: bool = False):
        orig_cursor_position = event.lastScenePos()
        updated_cursor_position = event.scenePos()

        orig_position = self.scenePos()

        updated_cursor_x = (
            updated_cursor_position.x() - orig_cursor_position.x() + orig_position.x()
        )
        updated_cursor_y = (
            updated_cursor_position.y() - orig_cursor_position.y() + orig_position.y()
        )

        if updated_cursor_x > self.max_width() - 5:
            updated_cursor_x = self.max_width() - 5
        if updated_cursor_y > self.max_height() - 5:
            updated_cursor_y = self.max_height() - 5
        if updated_cursor_x < 0:
            updated_cursor_x = 0
        if updated_cursor_y < 0:
            updated_cursor_y = 0
        self.forcePos(updated_cursor_x, updated_cursor_y, outside_event)

    def forcePos(self, updated_cursor_x, updated_cursor_y, outside_event: bool = False):
        pass

    def mouseReleaseEvent(self, event):
        # print('x: {0}, y: {1}'.format(self.pos().x(), self.pos().y()))
        self.updateCache()

    def updateCache(self):
        pass

    def moveXY(self, x: int, y: int):
        org_pos = self.scenePos()
        self.setX(x + org_pos.x())
        self.setY(y + org_pos.y())


@dataclass
class LocInfo:
    x: float
    y: float
    w: float
    h: float
    cat_name: str = None

    @property
    def xmax(self):
        return self.x + self.w

    @property
    def ymax(self):
        return self.y + self.h

    def get_adjusted_dims(self, x_scale: float, y_scale: float, up: bool = True):
        return LocInfo(
            self.x * x_scale if up else self.x / x_scale,
            self.y * y_scale if up else self.y / y_scale,
            self.w * x_scale if up else self.w / x_scale,
            self.h * y_scale if up else self.h / y_scale,
        )


class MovingBox(QGraphicsRectItem):
    def __init__(self, locinfo: LocInfo, sq) -> None:
        super().__init__(locinfo.x, locinfo.y, locinfo.w, locinfo.h)
        self.sq = sq
        self.setBrush(Qt.green)
        self.setOpacity(0.2)

    def mouseDoubleClickEvent(self, event):
        self.setBrush(Qt.red)
        self.sq.image_manager.set_object_focus(self.sq.id)
        print("double", event)

    def mousePressEvent(self, event):
        self.setBrush(Qt.green)
        self.sq.image_manager.set_object_focus(self.sq.id, focus=False)

    def mouseMoveEvent(self, event):
        pass

    def mouseReleaseEvent(self, event):
        # print('x: {0}, y: {1}'.format(self.pos().x(), self.pos().y()))
        self.updateCache()

    def updateCache(self):
        pass


class SQ:
    ADJUST = 5

    def __init__(self, image_manager, frame, index, id=None, cords=None):
        self.index = index
        self.frame = frame
        self.id = id if id else str(uuid.uuid4())
        self.pixmap = image_manager.current_pix_map.pixmap()
        self.scene = image_manager.scene
        self.image_manager = image_manager

        x, y, deep_x, deep_y = self.get_starting_locs(cords)  # 50, 50, 500, 500

        self.point_one = MovingObject(x, y, 10, self.pixmap)
        self.point_two = MovingObject(deep_x, y, 10, self.pixmap)
        self.point_three = MovingObject(x, deep_y, 10, self.pixmap)
        self.point_four = MovingObject(deep_x, deep_y, 10, self.pixmap)
        locinfo = self.getLocInfo()
        self.rec = MovingBox(locinfo, self)
        self.image_manager.maybe_set_current_label(cords.cat_name if cords else None)
        self.text = QGraphicsTextItem(self.image_manager.current_label)
        self.text.setPos(locinfo.x, locinfo.y)

        self.rec.mouseMoveEvent = self.box_move

        self.point_one.forcePos = self.forcePos(
            self.point_one, self.point_three, self.point_two
        )
        self.point_two.forcePos = self.forcePos(
            self.point_two, self.point_four, self.point_one
        )
        self.point_three.forcePos = self.forcePos(
            self.point_three, self.point_one, self.point_four
        )
        self.point_four.forcePos = self.forcePos(
            self.point_four, self.point_two, self.point_three
        )

        self.point_one.updateCache = self.updateCache
        self.point_two.updateCache = self.updateCache
        self.point_three.updateCache = self.updateCache
        self.point_four.updateCache = self.updateCache
        self.rec.updateCache = self.updateCache

        self.add()

    def get_starting_locs(self, cords):
        if not cords:
            x, y = self.pixmap.width() // 1.6, self.pixmap.height() // 1.6
            deep_x, deep_y = self.pixmap.width() // 2.4, self.pixmap.height() // 2.4
        else:
            print("recived: ", cords)
            cords = cords.get_adjusted_dims(self.x_scale, self.y_scale, False)
            print("adjusted: ", cords)
            x, y = cords.x - self.ADJUST, cords.y - self.ADJUST
            deep_x, deep_y = (
                cords.w + cords.x - self.ADJUST,
                cords.h + cords.y - self.ADJUST,
            )
            print(x, y, deep_x, deep_y)
        return x, y, deep_x, deep_y

    def box_move(self, event):
        self.point_one.mouseMoveEvent(event, True)
        self.point_two.mouseMoveEvent(event, True)
        self.point_three.mouseMoveEvent(event, True)
        self.point_four.mouseMoveEvent(event, True)

    def forcePos(
        self,
        target_node: MovingObject,
        connected_x: MovingObject,
        connected_y: MovingObject,
        outside_event: bool = False,
    ):
        def forcePos(
            updated_cursor_x: int, updated_cursor_y: int, outside_event: bool = False
        ):
            original_x = connected_x.scenePos()
            original_y = connected_y.scenePos()
            target_node.setPos(QPointF(updated_cursor_x, updated_cursor_y))
            if not outside_event:
                connected_x.setPos(QPointF(updated_cursor_x, original_x.y()))
                connected_y.setPos(QPointF(original_y.x(), updated_cursor_y))
            locinfo = self.getLocInfo()
            self.text.setPos(locinfo.x, locinfo.y)
            self.rec.setRect(locinfo.x, locinfo.y, locinfo.w, locinfo.h)

        return forcePos

    def updateCache(self):
        print("saving:", self.cv_cords, "from: ", self.getLocInfo())
        self.image_manager.update_box_loc(self.index, self.id, self.cv_cords)

    def getLocInfo(self) -> LocInfo:
        all_x = [
            self.point_one.scenePos().x() + self.ADJUST,
            self.point_two.scenePos().x() + self.ADJUST,
            self.point_three.scenePos().x() + self.ADJUST,
            self.point_four.scenePos().x() + self.ADJUST,
        ]
        all_y = [
            self.point_one.scenePos().y() + self.ADJUST,
            self.point_two.scenePos().y() + self.ADJUST,
            self.point_three.scenePos().y() + self.ADJUST,
            self.point_four.scenePos().y() + self.ADJUST,
        ]
        x = min(all_x)
        y = min(all_y)
        return LocInfo(
            x,
            y,
            max(all_x) - x,
            max(all_y) - y,
        )

    @property
    def cv_cords(self):
        locinfo = self.getLocInfo()
        return locinfo.get_adjusted_dims(self.x_scale, self.y_scale)

    def get_pixmap_cords_from_cv(self, locinfo: LocInfo):
        return locinfo.get_adjusted_dims(self.x_scale, self.y_scale, False)

    @property
    def x_scale(self):
        return self.frame.shape[1] / self.pixmap.width()

    @property
    def y_scale(self):
        return self.frame.shape[0] / self.pixmap.height()

    def add(self):
        self.scene.addItem(self.rec)
        self.scene.addItem(self.point_one)
        self.scene.addItem(self.point_two)
        self.scene.addItem(self.point_three)
        self.scene.addItem(self.point_four)
        self.scene.addItem(self.text)

    def delete(self):
        if self.rec in self.scene.items():
            self.scene.removeItem(self.rec)
            self.scene.removeItem(self.point_one)
            self.scene.removeItem(self.point_two)
            self.scene.removeItem(self.point_three)
            self.scene.removeItem(self.point_four)
            self.scene.removeItem(self.text)

    def update_label(self, text: str):
        self.text.setPlainText(text)
