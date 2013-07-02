DROP SCHEMA crime CASCADE;

CREATE SCHEMA crime;

SET search_path TO crime,public;

CREATE SEQUENCE crime.crime_seq;

CREATE TABLE crime.crimes (
  id      INTEGER NOT NULL DEFAULT nextval('crime_seq'),
  crimeid VARCHAR NOT NULL,
  caseno  VARCHAR,
  ts      TIMESTAMP NOT NULL, 
  block   VARCHAR NOT NULL,
  iucr    VARCHAR NOT NULL,
  ptype   VARCHAR NOT NULL,
  descr   VARCHAR NOT NULL,
  locdescr VARCHAR,
  arrest   BOOLEAN NOT NULL,
  domestic BOOLEAN NOT NULL,
  beat     INTEGER NOT NULL,
  district INTEGER,
  ward     INTEGER,
  commarea INTEGER,
  fbicode  VARCHAR NOT NULL,
  x        FLOAT,
  y        FLOAT,
  year     INTEGER,
  updated  TIMESTAMP NOT NULL,
  latitude FLOAT,
  longitude FLOAT,
  locstr   VARCHAR
);

SELECT AddGeometryColumn('crime','crimes','geo',3435,'POINT',2);

ALTER SEQUENCE crime.crime_seq 
  OWNED BY crime.crimes.id;
ALTER TABLE ONLY crime.crimes
  ADD CONSTRAINT crime_pkey PRIMARY KEY (id);
ALTER TABLE ONLY crime.crimes
  ADD CONSTRAINT crime_unique UNIQUE(id);

\copy crime.crimes (crimeid, caseno, ts, block, iucr, ptype, descr, locdescr, arrest, domestic, beat, district, ward, commarea, fbicode, x, y, year, updated, latitude, longitude, locstr) FROM '/mnt/data1/CPD/crimes_2001-2013.csv' CSV HEADER

UPDATE crime.crimes SET geo = ST_Transform(ST_SetSRID(ST_Point("longitude","latitude"),4326),3435);

CREATE INDEX crime_geoidx ON crime.crimes USING gist(geo); 

UPDATE crime.crimes SET iucr='0'||iucr WHERE iucr LIKE '___';
