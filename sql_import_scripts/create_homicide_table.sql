DROP TABLE crime.homicides CASCADE;

SET search_path TO crime,public;

CREATE SEQUENCE crime.homicides_seq;

CREATE TABLE crime.homicides (
  id      INTEGER NOT NULL DEFAULT nextval('homicides_seq'),
  story_url VARCHAR,
  neighborhood  VARCHAR,
  homname      VARCHAR, 
  gender   VARCHAR,
  age    INTEGER,
  address   VARCHAR, 
  charges   VARCHAR,
  race      VARCHAR,
  location   VARCHAR,
  time     VARCHAR, 
  homdate     VARCHAR,
  rd       VARCHAR,
  cause    VARCHAR
);


ALTER SEQUENCE crime.homicides_seq 
  OWNED BY crime.homicides.id;
ALTER TABLE ONLY crime.homicides
  ADD CONSTRAINT homicide_pkey PRIMARY KEY (id);
ALTER TABLE ONLY crime.homicides
  ADD CONSTRAINT homicide_unique UNIQUE(id);

\copy crime.homicides (address, homdate, time, location, neighborhood, age, gender, race, homname, cause, story_url, rd, charges) FROM '/home/pmeinshausen/Homicides_2009-2013.csv' CSV HEADER



