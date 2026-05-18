FUNCTION CreateCar()

    CREATE Car

    Car.ID = Start from 0 then +1 for each new car

    Car.DriverID = Randomly assign existing Driver.ID

    Car.BaseTopSpeed = 350 km/h
    Car.BaseAcceleration = 2 seconds (0-100 km/h)
    Car.BaseHandling = 100

    Car.CurrentSpeed = 0 km/h

    Car.TyreCondition = 100
    Car.FuelLoad = 100

    Car.CurrentLap = 0
    Car.CurrentPosition = Starting Grid Position

    Car.CurrentCheckpoint = 0

    Car.RaceStatus = Active

    RETURN Car

END FUNCTION
