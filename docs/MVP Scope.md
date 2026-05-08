
# MVP Scope

A deterministic motorsport management simulation where the user controls the strategy of a single driver rather than directly driving the car themselves. The simulation is based on timing gaps between competitors rather than physical spatial awareness on the track. Drivers make decisions based on factors such as tyre wear, grip, race position, sector gaps, and number of laps remaining.

The project is agent based, with AI drivers operating under the same information and limitations as the user controlled driver. Behaviour is controlled through predefined strategy states such as push, normal and conserve. These influence things such as tyre wear rate and performance over the race.

The simulation is displayed through a 2d birds’ eye GUI representation of a race track. The visualisation is a representation of the simulation state rather than a physics simulation or collision system.

## Database

### Core Entities

* Car(ID, DriverID, Colour)
* Driver(ID, Name, Age, Skill, Aggression, Consistency)
* Track(ID, Name, Location, Length, NumberOfTurns)
* RaceResult(ID, TrackID, DriverID, Position, TotalTime, LapsCompleted)

The database exists to:

* Store driver, car and track data
* Store race results
* Allow repeatable race simulations with different configurations
* Provide data to the simulation engine and GUI

## Simulation Scope

### Included in MVP

* Deterministic simulation loop
* AI driver behaviour states
* Push / Normal / Conserve modes
* Tyre wear affecting grip and performance
* Sector timing and race gaps
* Lap counting and race finishing
* Pit stop decisions
* Race results and finishing order
* 2d race visualisation
* Telemetry display
* User controlled strategy inputs
* Multiple AI controlled competitors

### Explicitly Out of Scope

* Realistic physics simulation
* Collision systems
* Full spatial awareness between cars
* Suspension, aerodynamics or engine simulation
* Multiplayer
* Career mode
* Financial systems
* Team staffing systems
* Contract systems
* Persistent world simulation
* Real time weather systems

## GUI

### Main Menu

* User selects a driver
* User selects track/race configuration
* Instructions/help screen

### Race Screen

* Cars displayed moving around a 2d track
* Telemetry panel showing:
  * Driver positions
  * Sector gaps
  * Current strategy mode
  * Tyre condition
  * Lap count
* User strategy controls:
  * Push
  * Normal
  * Conserve
  * Pit stop request

### Results Screen

* Finishing positions
* Total race times
* Sector/lap statistics
* Tyre and strategy summary

## MVP Goal

The goal of the MVP is to demonstrate:

* Deterministic agent based race simulation
* Strategy driven race outcomes
* A functioning GUI connected to the simulation engine
* Repeatable simulation behaviour under fixed seeds
* Expandable architecture for future development beyond undergraduate project scope
