from __future__ import annotations #annotations is used to indicate the expected types of variables and function return values, which can help with code readability and debugging.

from pathlib import Path #Path is a class from the pathlib module that provides an object-oriented interface for working with file system paths.
import sys #sys is a module that provides access to some variables used or maintained by the interpreter and to functions that interact strongly with the interpreter. Interpreter means a program that executes instructions written in a programming language. In this case, sys is used to manipulate the Python path, which is a list of directories that the interpreter searches for modules when importing.

from PyQt6.QtCore import Qt #Qt is a module from the PyQt6 library that provides various classes and functions for working with the Qt framework, which is a popular framework for developing graphical user interfaces (GUIs) in Python. In this code, Qt is used to access some constants and flags related to alignment and pen styles.
from PyQt6.QtGui import QColor, QPainter, QPen #QColor is a class from the PyQt6 library that represents a color in the RGB color space. QPainter is a class that provides functions for drawing on widgets and other paint devices. QPen is a class that defines the style of lines and outlines used for drawing shapes and text. In this code, these classes are used to set the colors and styles for drawing the racetrack and checkpoints.
from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget #QApplication is a class that manages the GUI application's control flow and main settings. QLabel is a widget that displays text or an image. QVBoxLayout is a layout manager that arranges widgets vertically. QWidget is the base class for all UI objects in PyQt6. In this code, these classes are used to create the main application window, display the track name and location, and arrange the widgets in a vertical layout.

PROJECT_ROOT = Path(__file__).resolve().parents[2] #This line defines a constant called PROJECT_ROOT, which is set to the parent directory of the parent directory of the current file. The __file__ variable contains the path to the current file, and resolve() is a method that returns the absolute path. The parents attribute is a sequence of parent directories, and [2] accesses the second parent directory, which is assumed to be the root of the project. This constant can be used to construct paths to other files in the project, such as data files or modules.
if str(PROJECT_ROOT) not in sys.path:
	sys.path.insert(0, str(PROJECT_ROOT))

from src.core.track_geometry import build_layout_paths, checkpoint_point_on_layout
from src.models.track import TrackDefinition, load_track_definition


class RaceTrackWidget(QWidget):
	def __init__(self, track: TrackDefinition, parent: QWidget | None = None) -> None:
		super().__init__(parent)
		self._track = track
		self.setMinimumSize(900, 600)

	def paintEvent(self, event) -> None:  # type: ignore[override]
		painter = QPainter(self)
		painter.setRenderHint(QPainter.RenderHint.Antialiasing)
		painter.fillRect(self.rect(), QColor("#10131a"))

		outer_path, inner_path, center, half_straight, turn_r, tw = build_layout_paths(self._track, float(self.width()), float(self.height()))
		track_band = outer_path.subtracted(inner_path)

		painter.setPen(Qt.PenStyle.NoPen)
		painter.setBrush(QColor("#303640"))
		painter.drawPath(track_band)

		painter.setPen(QPen(QColor("#ffd166"), 1))
		painter.setBrush(QColor("#ffd166"))
		for checkpoint in self._track.checkpoints:
			point = checkpoint_point_on_layout(center, half_straight, turn_r, checkpoint.position)
			painter.drawEllipse(point, 5.0, 5.0)
			painter.drawText(int(point.x() + 8.0), int(point.y() - 8.0), checkpoint.name)


class TrackPreviewWindow(QWidget):
	def __init__(self, track: TrackDefinition, parent: QWidget | None = None) -> None:
		super().__init__(parent)
		self.setWindowTitle(track.name)

		layout = QVBoxLayout(self)
		header = QLabel(f"{track.name} - {track.location}")
		header.setAlignment(Qt.AlignmentFlag.AlignCenter)
		layout.addWidget(header)
		layout.addWidget(RaceTrackWidget(track))


def main() -> int:
	app = QApplication(sys.argv)
	track_path = Path(__file__).resolve().parents[1] / "data" / "track.json"
	track = load_track_definition(track_path)

	window = TrackPreviewWindow(track)
	window.resize(1100, 800)
	window.show()
	return app.exec()


if __name__ == "__main__":
	raise SystemExit(main())
