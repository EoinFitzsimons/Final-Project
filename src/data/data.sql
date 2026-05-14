CREATE TABLE drivers (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    archetype TEXT NOT NULL,
    age INTEGER,
    speed INTEGER,
    handling INTEGER,
    aggression INTEGER,
    consistency INTEGER
);


CREATE TABLE cars (
    id INTEGER PRIMARY KEY,
    driver_id INTEGER,
    top_speed INTEGER,
    tyre_condition REAL,
    fuel_load REAL,
    current_lap INTEGER,
    current_checkpoint INTEGER,
    FOREIGN KEY(driver_id) REFERENCES drivers(id)
);


CREATE TABLE tracks (
    id INTEGER PRIMARY KEY,
    name TEXT,
    total_laps INTEGER,
    total_length INTEGER,
    number_of_turns INTEGER,
    number_of_straights INTEGER,
    surface_grip REAL
);