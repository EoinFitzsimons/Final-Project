from __future__ import annotations #annotations is used to indicate the expected types of variables and function return values, which can help with code readability and debugging.

from math import cos, sin, pi #cos and sin are functions from the math module that calculate the cosine and sine of an angle, respectively. The pi constant represents the mathematical constant π, which is approximately equal to 3.14159. In this code, these functions and constant are used to calculate the positions of checkpoints on the racetrack layout based on their normalised position along the track's perimeter.
from typing import Tuple #Tuple is a type hint that indicates that a variable is expected to be a tuple, which is an ordered collection of elements. In this code, Tuple[QPainterPath, QPainterPath, QPointF, float, float, float] indicates that the function build_layout_paths returns a tuple containing two QPainterPath objects, one QPointF object, and three float values. This can help with code readability and debugging by providing information about the expected return types of the function. The items of the tuple cannot be modified after creation.

from PyQt6.QtCore import QPointF, QRectF #QPointF is a class from the PyQt6 library that represents a point in 2D space with floating-point precision. QRectF is a class that represents a rectangle defined by its top-left corner and its width and height, also with floating-point precision. In this code, these classes are used to define the geometry of the racetrack layout and to calculate the positions of checkpoints on the track.
from PyQt6.QtGui import QPainterPath #QPainterPath is a class from the PyQt6 library that represents a path that can be drawn using a QPainter. It can consist of lines, curves, and other shapes. In this code, QPainterPath is used to define the outer and inner paths of the racetrack layout, which are then used to draw the track on the screen.

from src.models.track import TrackDefinition #This line imports the TrackDefinition class from the src.models.track module. The TrackDefinition class is a data class that represents the definition of a racetrack, including its name, location, type, length, laps, width, surface grip, pit lane information, checkpoints, segments, and optional layout geometry. This class is used in the functions defined in this file to build the layout paths and calculate checkpoint positions based on the track definition.


def build_layout_paths(track: TrackDefinition, canvas_width: float, canvas_height: float) -> Tuple[QPainterPath, QPainterPath, QPointF, float, float, float]: #This function takes a TrackDefinition object and the dimensions of the canvas as input and returns a tuple containing two QPainterPath objects (outer_path and inner_path), a QPointF object (center), and three float values (half_straight, turn_radius, track_width_px). The function builds the layout paths for the racetrack based on the provided track definition and layout parameters. It calculates the center point of the track, the length of the straight sections, the radius of the turns, and the width of the track in pixels. The outer_path represents the outer boundary of the track, while the inner_path represents the inner boundary.
#The backup values for those not set in the definition are based on canvas size, but will not be used as every json definition will have these set. It is still good practice to have a backup.
    layout = track.layout or {}
    cx = float(layout.get("center_x", canvas_width / 2.0)) #The cx variable is calculated by retrieving the "center_x" value from the track's layout dictionary. If the "center_x" key is not present in the layout, it defaults to half of the canvas width (canvas_width / 2.0). This means that if the track definition does not specify a center_x value, the center of the track will be positioned at the horizontal midpoint of the canvas.
    cy = float(layout.get("center_y", canvas_height / 2.0))#The same but for cy.
    straight_px = float(layout.get("straight_length_px", max(canvas_width * 0.5, 200.0)))
    turn_r = float(layout.get("turn_radius_px", max(canvas_height * 0.2, 80.0)))
    track_width_px = float(layout.get("track_width_px", max(track.track_width_m * 6.0, min(canvas_width, canvas_height) * 0.06)))
    
	#Half straight is used for layout and checkpoint calculations, but the full straight length is used for path building. The track is built around the center point, so half straight is added/subtracted from the center x coordinate to get the start/end of straights and turns.
    half_straight = straight_px / 2.0
    center = QPointF(cx, cy)
    half_w = track_width_px / 2.0

    # Outer/inner radii for turns are based on turn radius + track width, but the inner radius is not allowed to go below 1 pixel to avoid rendering issues with very narrow tracks or large turn radii.
    router = turn_r + half_w
    rinner = max(turn_r - half_w, 1.0)

    # Build outer path, starting at the right-most point of the top outer straight, then going left, around the left turn, right along the bottom straight, and around the right turn back to the start. The inner path is built in the same way but with the inner radius instead of the outer radius.
    outer = QPainterPath()
    # start at right-most point of top outer straight
    outer.moveTo(cx + half_straight, cy - router)
    outer.lineTo(cx - half_straight, cy - router)
    # left outer semicircle (top to bottom)
    rect_left = QRectF((cx - half_straight) - router, cy - router, 2 * router, 2 * router)
    outer.arcTo(rect_left, 90.0, 180.0)
    outer.lineTo(cx + half_straight, cy + router)
    # right outer semicircle (bottom to top)
    rect_right = QRectF((cx + half_straight) - router, cy - router, 2 * router, 2 * router)
    outer.arcTo(rect_right, 270.0, 180.0)
    outer.closeSubpath()

    # Build inner path, same as outer but with inner radius instead of outer radius
    inner = QPainterPath()
    inner.moveTo(cx + half_straight, cy - rinner)
    inner.lineTo(cx - half_straight, cy - rinner)
    rect_left_i = QRectF((cx - half_straight) - rinner, cy - rinner, 2 * rinner, 2 * rinner)
    inner.arcTo(rect_left_i, 90.0, 180.0)
    inner.lineTo(cx + half_straight, cy + rinner)
    rect_right_i = QRectF((cx + half_straight) - rinner, cy - rinner, 2 * rinner, 2 * rinner)
    inner.arcTo(rect_right_i, 270.0, 180.0)
    inner.closeSubpath()

    return outer, inner, center, half_straight, turn_r, track_width_px


def checkpoint_point_on_layout(center: QPointF, half_straight: float, turn_r: float, position: float) -> QPointF: #This function takes the center point of the track, the length of the half straight section, the radius of the turns, and a normalised position along the track's perimeter as input and returns a QPointF object representing the position of a checkpoint on the track layout. The function places quarter checkpoints at stable visual landmarks on the oval so the same sector stays in the same place even when the widget size changes.

    position = position % 1.0
    # Nudge the quarter checkpoints slightly away from the exact corners so the labels do not stack on the start/finish marker.
    if abs(position - 0.25) < 1e-9:
        position = 0.24
    elif abs(position - 0.75) < 1e-9:
        position = 1

    cx = center.x()
    cy = center.y()

    if position < 0.25:
        # Top straight: from right to left.
        frac = position / 0.25
        x = cx + half_straight - (2.0 * half_straight) * frac
        y = cy - turn_r
        return QPointF(x, y)

    if position < 0.5:
        # Left semicircle: top -> bottom.
        frac = (position - 0.25) / 0.25
        angle = pi / 2.0 + frac * pi
        center_left_x = cx - half_straight
        center_left_y = cy
        x = center_left_x + cos(angle) * turn_r
        y = center_left_y + sin(angle) * turn_r
        return QPointF(x, y)

    if position < 0.75:
        # Bottom straight: left -> right.
        frac = (position - 0.5) / 0.25
        x = cx - half_straight + (2.0 * half_straight) * frac
        y = cy + turn_r
        return QPointF(x, y)

    # Right semicircle: bottom -> top.
    frac = (position - 0.75) / 0.25
    angle = 3.0 * pi / 2.0 + frac * pi
    center_right_x = cx + half_straight
    center_right_y = cy
    x = center_right_x + cos(angle) * turn_r
    y = center_right_y + sin(angle) * turn_r
    return QPointF(x, y)
