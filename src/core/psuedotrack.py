'''
FUNCTION CreateTrack()
    
    CREATE Track

    Track.ID = Start from 0 then +1 for each new track
    Track.Name = Random Name
    Track.Location = Random Location

    Track.TotalLength = Random FROM (1-5) km
    Track.TotalLaps = Random FROM (10-50)  

    Track.NumberOfTurns = Random FROM (5-20)
    Track.NumberOfStraights = Random FROM (5-20)

    Track.TrackWidth = Random FROM (10-20) m

    Track.StartFinishLinePosition = Random Position on main straight

    Track.HasPitLane = Random Boolean
    Track.PitLaneLength = Random FROM (1-5) km
    Track.PitEntryPosition = Random Position on start main straight
    Track.PitExitPosition = Random Position on  end main straight

    Track.SurfaceGrip = Random FROM (0-100)

    Track.Checkpoints[]
    Track.Segments[]

    RETURN Track
END FUNCTION

FUNCTION GenerateCheckpoints(Track)
    For eacg turn and straight in Track
        CREATE Checkpoint
        Checkpoint.ID = Unique ID
        Checkpoint.Position = Centre of the track segment
        Checkpoint.Type = "Turn" or "Straight"
        Add Checkpoint to Track.Checkpoints[]
    END FOR
END FUNCTION

#Example of a generated track in JSON format{
  "id": 0,
  "name": "Oval Test Track",
  "location": "Test Location",
  "type": "oval",
  "total_length_km": 5.0,
  "total_laps": 20,
  "track_width_m": 14,
  "surface_grip": 100,
  "has_pit_lane": false,
  "pit_lane_length_km": 0.0,
  "start_finish_position": 0,
  "checkpoints": [
    {
      "id": 1,
      "name": "Start Finish",
      "position": 0
    },
    {
      "id": 2,
      "name": "Sector 1",
      "position": 0.25
    },
    {
      "id": 3,
      "name": "Sector 2",
      "position": 0.5
    },
    {
      "id": 4,
      "name": "Sector 3",
      "position": 0.75
    }
  ],
  "segments": [
    {
      "id": 1,
      "name": "Main Straight",
      "type": "straight",
      "length_km": 1.25,
      "grip_modifier": 0
    },
    {
      "id": 2,
      "name": "Turn 1",
      "type": "corner",
      "angle_degrees": 180,
      "length_km": 1.25,
      "grip_modifier": -10
    },
    {
      "id": 3,
      "name": "Back Straight",
      "type": "straight",
      "length_km": 1.25,
      "grip_modifier": 0
    },
    {
      "id": 4,
      "name": "Turn 2",
      "type": "corner",
      "angle_degrees": 180,
      "length_km": 1.25,
      "grip_modifier": -10
    }
  ],
  "comment": "Oval track. Position refers to the percentage progress around the track."
}
'''