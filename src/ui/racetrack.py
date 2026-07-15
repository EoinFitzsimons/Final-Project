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
from src.ui.colours import CHECKPOINT, RACE_BACKGROUND, ROAD


class RaceTrackWidget(QWidget): #This line defines a new class called RaceTrackWidget that inherits from QWidget
	def __init__(self, track: TrackDefinition, parent: QWidget | None = None) -> None: #This line defines the constructor method for the RaceTrackWidget class. It takes three parameters: self, which refers to the instance of the class being created; track, which is expected to be an instance of TrackDefinition that contains the data for the racetrack layout, and parent, which is an optional parameter that can be used to specify a parent widget for this widget. The constructor does not return any value, the return type is None.
		super().__init__(parent)
		self._track = track
		self.setMinimumSize(900, 600)

	def paintEvent(self, event) -> None:  # type: ignore[override] #This line defines a method called paintEvent that takes an event parameter and returns None. The paintEvent method is a special method in PyQt6 that is called whenever the widget needs to be repainted, such as when it is first shown or when it is resized. The type: ignore[override] comment is used to suppress a type checking error that occurs because the paintEvent method does not have the same signature as the one defined in the base class QWidget.
		painter = QPainter(self)
		painter.setRenderHint(QPainter.RenderHint.Antialiasing)
		painter.fillRect(self.rect(), QColor(RACE_BACKGROUND))

		outer_path, inner_path, center, half_straight, turn_r, _ = build_layout_paths(self._track, float(self.width()), float(self.height())) #This line calls the build_layout_paths function from the track_geometry module, passing in the track definition and the width and height of the widget as floating-point numbers. The function returns six values: outer_path, inner_path, center, half_straight, turn_r, and tw. These values represent the geometric properties of the racetrack layout, such as the paths for the outer and inner edges of the track, the center point of the track, the length of the straight sections, the radius of the turns, and the track width.
		track_band = outer_path.subtracted(inner_path)

		painter.setPen(Qt.PenStyle.NoPen)
		painter.setBrush(QColor(ROAD))
		painter.drawPath(track_band)

		painter.setPen(QPen(QColor(CHECKPOINT), 1))
		painter.setBrush(QColor(CHECKPOINT))
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


def main() -> int: #This line defines a function called main that takes no parameters and returns an integer. The main function is the entry point of the program, where the application is initialised and the main window is created and shown.
	app = QApplication(sys.argv)
	track_path = Path(__file__).resolve().parents[1] / "data" / "track.json"
	track = load_track_definition(track_path)

	window = TrackPreviewWindow(track)
	window.resize(1920, 1080)
	window.show()
	return app.exec()


if __name__ == "__main__":
	raise SystemExit(main())
