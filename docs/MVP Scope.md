# MVP Scope

What do I need to be in the project for it to be suitable for an undergrad final project? It is a racing simulation. I want a GUI to display the simulations as cars racing on a track.

## Database

In terms of entities that would exist, I have: [List developer vs user]

* Car(ID, Driver, Colour)
* Driver(ID, Age, Name, Skills, Stats)
* Track(ID, Name, Location, #Turns, Length, Other Characteristics)
* RaceResult(Track, Drivers, DriverPositions, #Laps, Time)

I want the drivers to be agents capable of making decisions based on the parameters around them, and internal to them.

I want the user to be in control of one driver, and be able to dictate how hard they push, when they make pitstops, how hard they battle. 

The AI cars/driver and user controlled should share all parameters available

## GUI

In terms of screens for the UI

Main Menu

* User selects a driver
* There are instructions on what the user can do

Race

* The cars are on track driving around
* There is telemetry on the side. It contains driver positions, gaps through sectors(points where time is logged so it's not continuous)
* There are strategy buttons, pit stop, push normal conserve.

Results

* A results screen showing the order of the race.
