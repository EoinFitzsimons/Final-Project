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