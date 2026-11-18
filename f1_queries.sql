DROP DATABASE IF EXISTS f1_compare;
CREATE DATABASE f1_compare;
USE f1_compare;

CREATE TABLE drivers (
  driver_number INT PRIMARY KEY,
  acronym       VARCHAR(5),
  full_name     VARCHAR(60),
  team_name     VARCHAR(40)
);

CREATE TABLE laps (
  driver_number INT,
  lap_number    INT,
  lap_time      DECIMAL(7,3),
  sector1       DECIMAL(6,3),
  sector2       DECIMAL(6,3),
  sector3       DECIMAL(6,3),
  top_speed     INT,
  is_pit_out    BOOLEAN,
  PRIMARY KEY (driver_number, lap_number)
);

-- clean laps only: no lap 1, no pit-out laps, no slow in/safety laps
CREATE VIEW v_laps AS
SELECT d.full_name, d.acronym, d.team_name, l.*
FROM laps l JOIN drivers d USING (driver_number)
WHERE l.lap_time IS NOT NULL
  AND l.lap_number > 1
  AND l.is_pit_out = 0
  AND l.lap_time < 92;
  
SELECT acronym, MIN(lap_time) AS best_lap, MAX(top_speed) AS vmax
FROM f1_compare.v_laps
GROUP BY acronym
ORDER BY best_lap;
