from __future__ import annotations #annotations is used to indicate the expected types of variables and function return values, which can help with code readability and debugging.

from dataclasses import dataclass #dataclass is a decorator that automatically generates special methods for classes, such as __init__ and __repr__, based on the class attributes.
from pathlib import Path #Path is a class from the pathlib module that provides an object-oriented interface for working with file system paths.
import json #json is a module that provides functions for working with JSON data, such as parsing and generating JSON strings.
from typing import Any #Any is a type hint that indicates that a variable can be of any type, which can be useful when the type of a variable can vary.


@dataclass(frozen=True) #The @dataclass decorator is used to create a data class, which is a class that is primarily used to store data. The frozen=True parameter makes the instances of the class immutable, meaning that their attributes cannot be modified after they are created.
class TrackCheckpoint:
	id: int
	name: str
	position: float


@dataclass(frozen=True)
class TrackSegment:
	id: int
	name: str
	type: str
	length_km: float
	grip_modifier: float = 0.0
	angle_degrees: float | None = None


@dataclass(frozen=True)
class TrackDefinition:
	id: int
	name: str
	location: str
	type: str
	total_length_km: float
	total_laps: int
	track_width_m: float
	surface_grip: float
	has_pit_lane: bool
	pit_lane_length_km: float
	start_finish_position: float
	checkpoints: list[TrackCheckpoint]
	segments: list[TrackSegment]
	comment: str = ""
	# Optional explicit ellipse geometry (legacy) and layout geometry
	ellipse: dict[str, Any] | None = None
	# Layout defines a 2-straight + 2-turn shape in pixels. Example:
	# {"center_x": 550, "center_y": 400, "straight_length_px": 800, "turn_radius_px": 200}
	layout: dict[str, Any] | None = None


def _parse_checkpoint(data: dict[str, Any]) -> TrackCheckpoint: #This function takes a dictionary as input and returns an instance of the TrackCheckpoint class. The dictionary is expected to have keys "id", "name", and "position", which correspond to the attributes of the TrackCheckpoint class. The function converts the values from the dictionary to the appropriate types (int, str, float) and creates a new TrackCheckpoint instance with those values.
	return TrackCheckpoint(
		id=int(data["id"]),
		name=str(data["name"]),
		position=float(data["position"]),
	)


def _parse_segment(data: dict[str, Any]) -> TrackSegment: #This function takes a dictionary as input and returns an instance of the TrackSegment class. The dictionary is expected to have keys "id", "name", "type", "length_km", and optionally "grip_modifier" and "angle_degrees". The function converts the values from the dictionary to the appropriate types (int, str, float) and creates a new TrackSegment instance with those values. If "grip_modifier" is not provided in the dictionary, it defaults to 0.0. If "angle_degrees" is not provided, it defaults to None.
	return TrackSegment(
		id=int(data["id"]),
		name=str(data["name"]),
		type=str(data["type"]),
		length_km=float(data["length_km"]),
		grip_modifier=float(data.get("grip_modifier", 0.0)),
		angle_degrees=(float(data["angle_degrees"]) if "angle_degrees" in data else None),
	)


def load_track_definition(path: str | Path) -> TrackDefinition: #This function takes a file path as input, reads the JSON data from the file, and returns an instance of the TrackDefinition class. The JSON data is expected to have keys that correspond to the attributes of the TrackDefinition class, including "id", "name", "location", "type", "total_length_km", "total_laps", "track_width_m", "surface_grip", "has_pit_lane", "pit_lane_length_km", "start_finish_position", "checkpoints", and "segments". The function uses the _parse_checkpoint and _parse_segment helper functions to convert the checkpoint and segment data from the JSON into instances of the TrackCheckpoint and TrackSegment classes, respectively. If a "comment" key is present in the JSON, it is included in the TrackDefinition instance; otherwise, it defaults to an empty string.
	payload = json.loads(Path(path).read_text(encoding="utf-8"))
	return TrackDefinition(
		id=int(payload["id"]),
		name=str(payload["name"]),
		location=str(payload["location"]),
		type=str(payload["type"]),
		total_length_km=float(payload["total_length_km"]),
		total_laps=int(payload["total_laps"]),
		track_width_m=float(payload["track_width_m"]),
		surface_grip=float(payload["surface_grip"]),
		has_pit_lane=bool(payload["has_pit_lane"]),
		pit_lane_length_km=float(payload["pit_lane_length_km"]),
		start_finish_position=float(payload["start_finish_position"]),
		checkpoints=[_parse_checkpoint(item) for item in payload.get("checkpoints", [])],
		segments=[_parse_segment(item) for item in payload.get("segments", [])],
		comment=str(payload.get("comment", "")),
		ellipse=payload.get("ellipse", None),
		layout=payload.get("layout", None),
	)