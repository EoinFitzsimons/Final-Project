'''
BEGIN Race Telemetry Update - race_controller.py

    FOR EACH active car

        Calculate current race position
        Calculate gap to leader

        Record telemetry

            Colour
            Driver Name

            Position
            Current Lap
            Lap Time

            Current Checkpoint
            Gap to Leader

            Current Speed

            Behaviour Mode
            Tyre Condition
            Fuel Load

            Race Status

    END FOR

    Order telemetry by race position

    Populate Race Information table

        Position
        Driver Name
        Gap to Leader
        Current Lap
        Race Status

    Populate Vehicle Telemetry table

        Driver Name
        Current Checkpoint
        Current Speed
        Tyre Condition
        Fuel Load

    Display telemetry within the Race GUI

END Race Telemetry Update


BEGIN Race GUI Update - race.py

    Wait for timer event

    Advance race simulation

    Request latest telemetry from Race Controller

    IF telemetry is available THEN

        FOR EACH driver telemetry record

            Update driver position
            Update lap number
            Update lap time

            Update current checkpoint

            Update current speed
            Update gap to leader

            Update tyre condition
            Update fuel load

            Update race status

            Calculate screen position

        END FOR

        Refresh race leaderboard

        Refresh Race Information table

        Refresh Vehicle Telemetry table

        Redraw race map

            Draw track
            Draw checkpoints
            Draw cars
            Draw driver labels

    END IF

    IF race has finished THEN

        Stop timer

        Request race results

        Open Results Screen

    END IF

END Race GUI Update
'''