-- INITIAL HEADER TO DROP OLD SHEMA AND CREATE 311 SCHEMA -- 
DROP SCHEMA threeoneone CASCADE;

CREATE SCHEMA threeoneone;

SET search_path TO threeoneone,public;

-- CREATE GRAFFITI TABLE ---
CREATE TABLE threeoneone.graffiti(
  id INTEGER NOT NULL,
  casedate DATE NOT NULL,
  status VARCHAR NOT NULL, 
  findate DATE, 
  serviceno VARCHAR NOT NULL,
  requesttype VARCHAR NOT NULL,
  surface VARCHAR,
  location VARCHAR,
  address VARCHAR,
  zipcode INTEGER,
  x FLOAT,
  y FLOAT,
  ward INTEGER,
  district INTEGER,
  comm_area INTEGER,
  latitude FLOAT,
  longitude FLOAT,
  locstr VARCHAR
);

SELECT AddGeometryColumn('threeoneone','graffiti','geo',3435,'POINT',2);

ALTER TABLE ONLY threeoneone.graffiti
  ADD CONSTRAINT graffiti_pkey PRIMARY KEY (id);
ALTER TABLE ONLY threeoneone.graffiti
  ADD CONSTRAINT graffiti_unique UNIQUE(id);

\copy threeoneone.graffiti (id, casedate, status, findate, serviceno, requesttype, surface, location, address, zipcode, x, y, ward, district, comm_area, latitude, longitude, locstr) FROM '/mnt/data1/CPD/311_Graffiti.csv' CSV HEADER

UPDATE threeoneone.graffiti SET geo = ST_Transform(ST_SetSRID(ST_Point("longitude","latitude"),4326),3435);

CREATE INDEX graffiti_geoidx ON threeoneone.graffiti USING gist(geo); 

-- CREATE BUILDINGS TABLE ---
CREATE TABLE threeoneone.buildings(
  id INTEGER NOT NULL,
  requesttype VARCHAR,
  requestno VARCHAR,
  servicedate DATE,
  loconlot VARCHAR,
  dangerous VARCHAR,
  status VARCHAR,
  entryptifopen VARCHAR,
  vacantorocc VARCHAR,
  vacbcfire BOOLEAN,
  pplusingbuilding BOOLEAN,
  addressno VARCHAR,
  addressdir VARCHAR,
  addressname VARCHAR,
  addresssuffix VARCHAR,
  zipcode INTEGER,
  x FLOAT,
  y FLOAT,
  latitude FLOAT,
  longitude FLOAT,
  locstr VARCHAR
);

SELECT AddGeometryColumn('threeoneone','buildings','geo',3435,'POINT',2);

ALTER TABLE ONLY threeoneone.buildings 
  ADD CONSTRAINT buildings_pkey PRIMARY KEY (id);
ALTER TABLE ONLY threeoneone.buildings
  ADD CONSTRAINT buildings_unique UNIQUE(id);

\copy threeoneone.buildings (id, requesttype, requestno, servicedate, loconlot, dangerous, status, entryptifopen, vacantorocc, vacbcfire, pplusingbuilding, addressno, addressdir, addressname, addresssuffix, zipcode, x, y, latitude, longitude, locstr) FROM '/mnt/data1/CPD/311_Buildings.csv' CSV HEADER

UPDATE threeoneone.buildings SET geo = ST_Transform(ST_SetSRID(ST_Point("longitude","latitude"),4326),3435);

CREATE INDEX buildings_geoidx ON threeoneone.buildings USING gist(geo); 

-- CREATE LIGHTS TABLE ---
CREATE TABLE threeoneone.lights(
  id INTEGER NOT NULL,
  casedate DATE NOT NULL,
  status VARCHAR NOT NULL, 
  findate DATE, 
  serviceno VARCHAR NOT NULL,
  requesttype VARCHAR NOT NULL,
  address VARCHAR,
  zipcode INTEGER,
  x FLOAT,
  y FLOAT,
  ward INTEGER,
  district INTEGER,
  comm_area INTEGER,
  latitude FLOAT,
  longitude FLOAT,
  locstr VARCHAR
);

SELECT AddGeometryColumn('threeoneone','lights','geo',3435,'POINT',2);

ALTER TABLE ONLY threeoneone.lights
  ADD CONSTRAINT lights_pkey PRIMARY KEY (id);
ALTER TABLE ONLY threeoneone.lights
  ADD CONSTRAINT lights_unique UNIQUE(id);

\copy threeoneone.lights (id, casedate, status, findate, serviceno, requesttype, address, zipcode, x, y, ward, district, comm_area, latitude, longitude, locstr) FROM '/mnt/data1/CPD/311_Lights.csv' CSV HEADER

UPDATE threeoneone.lights SET geo = ST_Transform(ST_SetSRID(ST_Point("longitude","latitude"),4326),3435);

CREATE INDEX lights_geoidx ON threeoneone.lights USING gist(geo); 