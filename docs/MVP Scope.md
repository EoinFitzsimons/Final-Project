# MVP Scope

What do I need to be in the project for it to be suitable for an undergrad final project? It is a racing simulation. I want a GUI to display the simulations as cars racing on a track.

## Database

In terms of entities that would exist, I have: [List developer vs user]

* Car(ID, Driver, Colour)
* Driver(ID, Age, Name, Skills, Stats)
* Track(ID, Name, Location, #Turns, Length, Other Characteristics)
* RaceResult(Track, Drivers, DriverPositions, #Laps, Time)

I want the drivers to be agents capable of making decisions based on the parameters around them, and internal to them.

The AI cars/driver should share all parameters available

## GUI

In terms of screens for the UI

Main Menu

* User sees the drivers
* There is information on what the attributes mean

Race

* The cars are on track driving around
* There is telemetry on the side. It contains driver positions, gaps through sectors(points where time is logged so it's not continuous)
* Race Progress is shown, as well as options to end the race or pause.

Results

* A results screen showing the order of the race.
