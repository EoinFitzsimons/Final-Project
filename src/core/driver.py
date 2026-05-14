FUNCTION GenerateDriver()

    CREATE Driver

    Driver.ID = Start from 0 then +1 for each new driver
    Driver.Name = Random Name

    Driver.Archtype = Random FROM
    (
        Veteran Defender,
        Wild Rookie,
        Calculated Racer,
        Speed Demon,
        Street Fighter,
        Seasoned Veteran,
        Future Champion,
        Ol Reliable,
        Pay Driver,
        Reigning Champion
    )

    IF Driver.Archtype = "Veteran Defender" THEN

        Driver.Age = Random FROM (36-50)

        Driver.Stats =
        (
            Speed: Random FROM (0-33),
            Handling: Random FROM (67-100),
            Aggression: Random FROM (0-33),
            Consistency: Random FROM (67-100)
        )

    ELSE IF Driver.Archtype = "Wild Rookie" THEN

        Driver.Age = Random FROM (16-24)

        Driver.Stats =
        (
            Speed: Random FROM (67-100),
            Handling: Random FROM (67-100),
            Aggression: Random FROM (67-100),
            Consistency: Random FROM (0-33)
        )

    ELSE IF Driver.Archtype = "Calculated Racer" THEN

        Driver.Age = Random FROM (25-35)

        Driver.Stats =
        (
            Speed: Random FROM (34-66),
            Handling: Random FROM (67-100),
            Aggression: Random FROM (0-33),
            Consistency: Random FROM (67-100)
        )

    ELSE IF Driver.Archtype = "Speed Demon" THEN

        Driver.Age = Random FROM (25-35)

        Driver.Stats =
        (
            Speed: Random FROM (67-100),
            Handling: Random FROM (34-66),
            Aggression: Random FROM (34-66),
            Consistency: Random FROM (0-33)
        )

    ELSE IF Driver.Archtype = "Street Fighter" THEN

        Driver.Age = Random FROM (25-35)

        Driver.Stats =
        (
            Speed: Random FROM (34-66),
            Handling: Random FROM (0-33),
            Aggression: Random FROM (67-100),
            Consistency: Random FROM (34-66)
        )

    ELSE IF Driver.Archtype = "Seasoned Veteran" THEN

        Driver.Age = Random FROM (36-50)

        Driver.Stats =
        (
            Speed: Random FROM (34-66),
            Handling: Random FROM (67-100),
            Aggression: Random FROM (0-33),
            Consistency: Random FROM (67-100)
        )

    ELSE IF Driver.Archtype = "Future Champion" THEN

        Driver.Age = Random FROM (16-24)

        Driver.Stats =
        (
            Speed: Random FROM (67-100),
            Handling: Random FROM (67-100),
            Aggression: Random FROM (34-66),
            Consistency: Random FROM (34-66)
        )

    ELSE IF Driver.Archtype = "Ol Reliable" THEN

        Driver.Age = Random FROM (36-50)

        Driver.Stats =
        (
            Speed: Random FROM (0-33),
            Handling: Random FROM (34-66),
            Aggression: Random FROM (0-33),
            Consistency: Random FROM (34-66)
        )

    ELSE IF Driver.Archtype = "Pay Driver" THEN

        Driver.Age = Random FROM (36-50)

        Driver.Stats =
        (
            Speed: Random FROM (0-33),
            Handling: Random FROM (0-33),
            Aggression: Random FROM (0-33),
            Consistency: Random FROM (0-33)
        )

    ELSE IF Driver.Archtype = "Reigning Champion" THEN

        Driver.Age = Random FROM (25-35)

        Driver.Stats =
        (
            Speed: Random FROM (67-100),
            Handling: Random FROM (67-100),
            Aggression: Random FROM (67-100),
            Consistency: Random FROM (67-100)
        )

    END IF

    RETURN Driver

END FUNCTION