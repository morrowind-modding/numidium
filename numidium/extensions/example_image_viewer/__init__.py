from PySide6.QtCore import Qt
from PySide6.QtGui import QImage, QImageReader, QPixmap, QWheelEvent
from PySide6.QtWidgets import (
    QFileDialog,
    QFrame,
    QGraphicsPixmapItem,
    QGraphicsScene,
    QGraphicsView,
    QToolButton,
    QVBoxLayout,
    QWidget,
)

from numidium.config import config
from numidium.tes3 import dds
from numidium.ui.activity_bar import ActivityBar, ActivityBarItem


class ImageViewer(QGraphicsView):
    """An image viewer that supports panning and zooming."""

    item: QGraphicsPixmapItem
    zoom: int = 0

    supported_formats: list[str] = [fmt.data().decode() for fmt in QImageReader().supportedImageFormats()]
    supported_formats += ["dds"]

    def __init__(self) -> None:
        super().__init__()

        self.item = QGraphicsPixmapItem()
        self.zoom = 0

        self.setScene(QGraphicsScene())
        self.scene().addItem(self.item)

        self.setFrameShape(QFrame.NoFrame)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def setPixmap(self, pixmap: QPixmap | None = None) -> None:
        self.zoom = 0
        if pixmap and not pixmap.isNull():
            self.setDragMode(QGraphicsView.ScrollHandDrag)
            self.item.setPixmap(pixmap)
            self.setSceneRect(pixmap.rect())
            if not self.parent().rect().contains(pixmap.rect()):
                self.fitInView(self.item, Qt.AspectRatioMode.KeepAspectRatio)
        else:
            self.setDragMode(QGraphicsView.NoDrag)
            self.item.setPixmap(QPixmap())

    def wheelEvent(self, event: QWheelEvent) -> None:
        if not self.item.pixmap().isNull():
            if event.angleDelta().y() > 0:
                self.zoom += 1
                self.scale(1.20, 1.20)
            else:
                self.zoom -= 1
                self.scale(0.80, 0.80)


class Container(QWidget):
    """Simple container for an ImageViewer that adds a 'Load Image' button."""

    viewer: ImageViewer

    def __init__(self) -> None:
        super().__init__()

        self.viewer = ImageViewer()

        button = QToolButton()
        button.setText("Load Image")
        button.clicked.connect(self.load_image)

        layout = QVBoxLayout()
        layout.addWidget(button)
        layout.addWidget(self.viewer)

        self.setLayout(layout)

    def load_image(self) -> None:
        workspace, _ = QFileDialog().getOpenFileName(
            parent=self,
            dir=config.active_workspace,
            caption="Load Image",
            filter=" *.".join(self.viewer.supported_formats),
            options=QFileDialog.Option.DontUseNativeDialog,  # type: ignore[arg-type]
        )
        if workspace.lower().endswith(".dds"):
            self.viewer.setPixmap(self._load_dds(workspace))
        else:
            self.viewer.setPixmap(QPixmap(workspace))

    @staticmethod
    def _load_dds(filepath: str) -> QPixmap:
        data, width, height = dds.decompress(filepath)
        image = QImage(data, width, height, QImage.Format.Format_ARGB32)
        image.rgbSwapped_inplace()
        return QPixmap.fromImage(image)


item = ActivityBarItem(widget=Container(), icon="icons:circle_24dp.svg", text="Image Viewer")


def register() -> None:
    ActivityBar.instance().add_item(item)


def unregister() -> None:
    ActivityBar.instance().remove_item(item)
