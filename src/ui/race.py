from __future__ import annotations #Postpones evaluation of annotations: They are stored as strings in __annotations__ instead of evaluated immediately.
# Useful for:
# Avoiding circular import issues in type hints.
# Reducing runtime overhead from evaluating annotations.
# Cleaner forward references.

import sys
from pathlib import Path
from typing import Callable #callable checks if an object can be called like a function. https://www.geeksforgeeks.org/python/callable-in-python/

# Qt provides the event loop, timers, drawing primitives, and widget classes used to build the live race window.
from PyQt6.QtCore import QPointF, QTimer, Qt
from PyQt6.QtGui import QColor, QPainter, QPainterPath, QPen
from PyQt6.QtWidgets import ( 
    QApplication,
    QAbstractItemView,
    QHeaderView,
    QStackedWidget,
    QLabel,
    QHBoxLayout,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
) 

# Add the repository root to sys.path so this file can be run directly and still import the src package.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Local project imports keep the race simulation, track model, and layout math separate from the UI layer.
from src.core.race_controller import RaceController, RaceTelemetry
from src.core.track_geometry import build_layout_paths, checkpoint_point_on_layout
from src.models.track import TrackDefinition, load_track_definition
from src.ui.colours import CAR_COLOURS, CHECKPOINT, FINISHED_CAR, RACE_BACKGROUND, ROAD, TEXT


class RaceOnTrackWidget(QWidget): #This class is a custom QWidget that displays the racetrack, checkpoints, and cars in a live race simulation
    def __init__(
        self,
        track: TrackDefinition,
        controller: RaceController,
        telemetry_callback: Callable[[list[RaceTelemetry]], None] | None = None,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        # Store the loaded track definition so the widget knows the layout and checkpoints to draw.
        self._track = track
        # Store the simulation controller so the widget can read race progress and advance the race.
        self._controller = controller
        # Keep a callback so the race window can refresh telemetry tables each tick.
        self._telemetry_callback = telemetry_callback
        # Keep the latest QPointF for each car so the paint routine can draw them without recomputing everything.
        self._car_positions: dict[int, QPointF] = {}
        # QTimer drives the animation by calling _advance_race at a fixed interval.
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._advance_race)
        self._timer.start(33)#30 is not 30 frames, the format is milliseconds, so 33 milliseconds per frame is precisely 30.3 frames per second.

        # Give the race canvas enough space for a readable oval track and car labels.
        self.setMinimumSize(1000, 700)
        # Populate the initial coordinate cache so the first paint has valid positions.
        self._refresh_car_positions()

    def _advance_race(self) -> None:
        # Active cars are the ones still moving; once none remain the animation can stop.
        active_cars = [car for car in self._controller.cars if car.race_status == "Active"]
        if not active_cars:
            self._timer.stop()
            self._refresh_car_positions()
            self._publish_telemetry()
            self.update()
            return

        # Advance the simulation by one tick, then refresh the cached screen coordinates.
        self._controller.step()
        self._refresh_car_positions()
        self._publish_telemetry()
        # Trigger a repaint so the cars appear to move on screen.
        self.update()

    def _publish_telemetry(self) -> None:
        if self._telemetry_callback is None:
            return

        telemetry = self._controller.get_telemetry()
        self._telemetry_callback(telemetry)

    def _build_centerline_path(
        self,
        center,
        half_straight: float,
        turn_r: float,
    ) -> QPainterPath:
        # QPainterPath is used here as the visible centreline that cars travel along.
        path = QPainterPath()
        path.moveTo(center.x() + half_straight, center.y() - turn_r) # Start at the top right corner of the track.
        path.lineTo(center.x() - half_straight, center.y() - turn_r) # Draw the straight section
        path.arcTo( #Draw the top left corner of the track.
            center.x() - half_straight - turn_r,
            center.y() - turn_r, 
            turn_r * 2.0, 
            turn_r * 2.0,
            90.0,
            180.0,
        )
        path.lineTo(center.x() + half_straight, center.y() + turn_r) # Draw the straight section
        path.arcTo( #Draw the bottom right corner of the track.
            center.x() + half_straight - turn_r,
            center.y() - turn_r,
            turn_r * 2.0,
            turn_r * 2.0,
            270.0,
            180.0,
        )
        path.closeSubpath() #Close the path to ensure it is a continuous loop.
        return path

    def _progress_fraction(self, progress_m: float) -> float:
        # Convert total distance travelled into a lap fraction between 0.0 and 1.0.
        lap_distance = max(self._controller.lap_distance, 1.0)
        return (progress_m % lap_distance) / lap_distance

    def _refresh_car_positions(self) -> None:
        # Build the track geometry for the current widget size so coordinates stay aligned to the visible track.
        outer_path, inner_path, center, half_straight, turn_r, _ = build_layout_paths(
            self._track,
            float(self.width()),
            float(self.height()),
        )
        # The outer and inner paths define the track band, while the centerline is used for car coordinates.
        _ = outer_path.subtracted(inner_path)
        centerline = self._build_centerline_path(center, half_straight, turn_r)

        # Convert each car's race progress into a point on the centerline and cache it by car id.
        for car in self._controller.cars:
            progress = self._controller._progress.get(car.id, 0.0)
            fraction = self._progress_fraction(progress)
            self._car_positions[car.id] = centerline.pointAtPercent(fraction)

    def paintEvent(self, event) -> None:  # type: ignore[override] this does not have an underscore as it is a Qt event handler, not a private method. https://doc.qt.io/qt-6/qwidget.html#paintEvent
        # QPainter is the Qt drawing API used to render the track, checkpoints, and car markers.
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing) #Antialiasing smooths the edges of the track and car markers for a cleaner appearance. It is computationally expensive for complex shapes, but the track is a simple shape. https://runebook.dev/en/docs/qt/quick3d-asset-conditioning-anti-aliasing
        painter.fillRect(self.rect(), QColor(RACE_BACKGROUND))

        # Rebuild the layout paths for the current window size before drawing.
        outer_path, inner_path, center, half_straight, turn_r, _ = build_layout_paths(
            self._track,
            float(self.width()),
            float(self.height()),
        )
        # Subtract the inner path from the outer path to create the visible track surface.
        track_band = outer_path.subtracted(inner_path)

        painter.setPen(Qt.PenStyle.NoPen)
        # Fill the track with a solid dark colour so the cars and checkpoints stand out.
        painter.setBrush(QColor(ROAD))
        painter.drawPath(track_band)

        # Checkpoints are drawn as markers on the track so the user can see the lap structure.
        painter.setPen(QPen(QColor(CHECKPOINT), 1))
        painter.setBrush(QColor(CHECKPOINT))
        for checkpoint in self._track.checkpoints:
            # Use the checkpoint's stored track position so the live race matches the track definition.
            point = checkpoint_point_on_layout(center, half_straight, turn_r, checkpoint.position)
            painter.drawEllipse(point, 5.0, 5.0)
            painter.drawText(int(point.x() + 8.0), int(point.y() - 8.0), checkpoint.name)

        # These colours are used to differentiate cars visually when multiple drivers are on track.
        # Draw each car at its cached coordinate, matching the order of the simulation controller.
        for index, (car, driver) in enumerate(zip(self._controller.cars, self._controller.drivers)):
            # Pull the latest point from the coordinate cache.
            point = self._car_positions.get(car.id)
            if point is None:
                # Fallback path for safety if a car position was not cached yet.
                progress = self._controller._progress.get(car.id, 0.0)
                fraction = self._progress_fraction(progress)
                centerline = self._build_centerline_path(center, half_straight, turn_r)
                point = centerline.pointAtPercent(fraction)
                self._car_positions[car.id] = point

            # Finished cars are muted so they are visually distinct from active cars.
            color = QColor(CAR_COLOURS[index % len(CAR_COLOURS)])
            if car.race_status == "Finished":
                color = QColor(FINISHED_CAR)

            painter.setBrush(color)
            painter.setPen(QPen(QColor(TEXT), 1))
            painter.drawEllipse(point, 8.0, 8.0)

            # Draw the driver's first name beside the car so the simulation is easier to follow.
            label = f"{driver.name.split()[0]}"
            painter.setPen(QPen(QColor(TEXT), 1))
            painter.drawText(int(point.x() + 10), int(point.y() - 10), label)

    def sizeHint(self):
        # Tell Qt the preferred size for this custom widget.
        return self.minimumSize()


class RaceWindow(QWidget): #This class is the main window for the live race
    def __init__(
        self,
        track: TrackDefinition,
        controller: RaceController | None = None,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        # The window title identifies the live race screen.
        self.setWindowTitle("Race View")

        # Reuse an existing controller when the menu and race view need to stay in sync.
        if controller is None:
            controller = RaceController(track, num_cars=10, max_ticks=5000)
            controller.setup()
        self._controller = controller
        self._telemetry_history: list[list[RaceTelemetry]] = []

        # QVBoxLayout stacks the status label above the race canvas.
        layout = QVBoxLayout(self)
        # QLabel shows the final race state once the simulation has finished.
        self._status = QLabel("Race running...")
        self._status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._status.setWordWrap(True)

        self._lap_counter = QLabel("Lap: 0 / 0")
        self._lap_counter.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self._end_race_button = QPushButton("End Race")
        self._end_race_button.clicked.connect(self.end_race)

        status_layout = QHBoxLayout()
        status_layout.addWidget(self._status)
        status_layout.addWidget(self._lap_counter)
        status_layout.addWidget(self._end_race_button)

        layout.addLayout(status_layout)

        self._race_stack = QStackedWidget()

        self._race_widget = RaceOnTrackWidget(
            track,
            self._controller,
            telemetry_callback=self._update_telemetry_tables,
        )

        self._results_widget = QWidget()

        self._race_stack.addWidget(self._race_widget)
        self._race_stack.addWidget(self._results_widget)

        layout.addWidget(self._race_stack, 3)

        tables_layout = QHBoxLayout()
        self._race_info_table = self._create_table(
            ["Position", "Driver Name", "Gap to Leader", "Current Lap", "Race Status"]
        )
        self._vehicle_table = self._create_table(
            ["Driver Name", "Current Checkpoint", "Current Speed", "Tyre Condition", "Fuel Load"]
        )
        tables_layout.addWidget(self._race_info_table, 1)
        tables_layout.addWidget(self._vehicle_table, 1)
        layout.addLayout(tables_layout, 2)

        self._update_telemetry_tables(self._controller.get_telemetry())

        self.resize(1920, 1080)

        # Check periodically whether the race has completed so the status label can update.
        self._finish_timer = QTimer(self)
        self._finish_timer.timeout.connect(self._check_finished)
        self._finish_timer.start(200)

    def _check_finished(self) -> None:
        # If any cars are still active, the race is not done yet.
        active = [car for car in self._controller.cars if car.race_status == "Active"]
        if active:
            return

        ordered = self._controller.get_telemetry()

        # Build a plain text result summary for the finished race.
        lines = ["Race finished", ""]
        for record in ordered:
            lines.append(
                f"{record.position}. {record.driver_name} - Lap {record.current_lap} - {record.race_status}"
            )

        self._finish_timer.stop()

        self._create_results_screen(
            self._telemetry_history
        )
        # Switch the stacked widget to show the results screen instead of the live race.
        self._race_stack.setCurrentIndex(1)

    def _create_table(self, headers: list[str]) -> QTableWidget:
        table = QTableWidget(0, len(headers), self)
        table.setHorizontalHeaderLabels(headers)
        table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        table.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        vertical_header = table.verticalHeader()
        assert vertical_header is not None
        vertical_header.setVisible(False)

        header = table.horizontalHeader()
        assert header is not None

        header.setStretchLastSection(True)
        for column in range(len(headers)):
            header.setSectionResizeMode(column, QHeaderView.ResizeMode.Stretch)
        return table

    def _set_table_item(self, table: QTableWidget, row: int, column: int, text: str) -> None:
        item = QTableWidgetItem(text)
        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        table.setItem(row, column, item)

    def _update_telemetry_tables(self, telemetry: list[RaceTelemetry]) -> None:
        self._telemetry_history.append(telemetry.copy())
        if telemetry:
            current_lap = max(record.current_lap for record in telemetry)
            self._lap_counter.setText(
                f"Lap: {current_lap} / {self._controller.track.total_laps}"
            )
        self._race_info_table.setRowCount(len(telemetry))
        self._vehicle_table.setRowCount(len(telemetry))

        for row, record in enumerate(telemetry):
            self._set_table_item(self._race_info_table, row, 0, str(record.position))
            self._set_table_item(self._race_info_table, row, 1, record.driver_name)
            self._set_table_item(self._race_info_table, row, 2, f"{record.gap_to_leader_m:.1f} m")
            self._set_table_item(self._race_info_table, row, 3, str(record.current_lap))
            self._set_table_item(self._race_info_table, row, 4, record.race_status)

            self._set_table_item(self._vehicle_table, row, 0, record.driver_name)
            self._set_table_item(self._vehicle_table, row, 1, record.current_checkpoint_name)
            self._set_table_item(self._vehicle_table, row, 2, f"{record.current_speed_kmh:.1f} km/h")
            self._set_table_item(self._vehicle_table, row, 3, str(record.tyre_condition))
            self._set_table_item(self._vehicle_table, row, 4, str(record.fuel_load))

    def end_race(self) -> None:
        # Stop the visual simulation timer.
        self._race_widget._timer.stop()

        # Mark remaining active cars as Did not finish.
        for car in self._controller.cars:
            if car.race_status == "Active":
                car.race_status = "DNF"

        # Get final race data after stopping.
        telemetry = self._controller.get_telemetry()

        # Update live tables one final time.
        self._update_telemetry_tables(telemetry)

        # Build results screen using final telemetry.
        self._create_results_screen(telemetry)

        # Switch the stacked widget to show the results screen instead of the live race.
        self._race_stack.setCurrentIndex(1)

        self._end_race_button.setEnabled(False)

    def _create_results_screen(self, telemetry_history):
        layout = QVBoxLayout(self._results_widget)

        title = QLabel("Race Results")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        table = QTableWidget(
            0,
            self._controller.track.total_laps + 2
        )

        headers = ["Driver"]

        for lap in range(1, self._controller.track.total_laps + 1):
            headers.append(f"Lap {lap}")

        headers.extend(["Final Position", "Status"])

        table.setHorizontalHeaderLabels(headers)

        # Prevent scrollbars from appearing by fitting the entire results table on screen.
        table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        # Make columns compact enough to display all laps.
        header = table.horizontalHeader()
        assert header is not None # Ensure the header is available
        header.setSectionResizeMode(QHeaderView.ResizeMode.Fixed)

        # Set sensible widths.
        table.setColumnWidth(0, 150)  # Driver name

        for column in range(1, len(headers)):
            table.setColumnWidth(column, 80)  # Lap times, final position, and status

        final = self._controller.get_telemetry()

        for record in final:
            row = table.rowCount()
            table.insertRow(row)

            table.setItem(
                row,
                0,
                QTableWidgetItem(record.driver_name)
            )

            # Fill lap columns with completed lap times.
            for lap in range(1, self._controller.track.total_laps + 1):

                if lap <= len(record.lap_times):
                    lap_time = record.lap_times[lap - 1]

                    table.setItem(
                        row,
                        lap,
                        QTableWidgetItem(f"{lap_time:.2f}s")
                    )
                else:
                    table.setItem(
                        row,
                        lap,
                        QTableWidgetItem("-")
                    )

            table.setItem(
                row,
                len(headers)-2,
                QTableWidgetItem(str(record.position))
            )

            table.setItem(
                row,
                len(headers)-1,
                QTableWidgetItem(record.race_status)
            )

        layout.addWidget(table)

        self._results_table = table            


def main() -> int:
    # QApplication is the root Qt application object required by every PyQt6 GUI.
    app = QApplication(sys.argv)

    # Load the track JSON so the GUI and simulation use the same track definition.
    track_path = Path(__file__).resolve().parents[1] / "data" / "track.json"
    track = load_track_definition(track_path)

    # Create the main race window and display it.
    window = RaceWindow(track)
    window.resize(1920, 1080)
    window.show()

    # Hand control to the Qt event loop and return the exit code to the shell.
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())