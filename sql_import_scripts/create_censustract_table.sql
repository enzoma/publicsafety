DROP SCHEMA census CASCADE;

CREATE SCHEMA census;

SET search_path TO census,crime,public;

CREATE SEQUENCE census.c2010_tracts_seq;

CREATE TABLE census.c2010_tracts (
  id      INTEGER NOT NULL DEFAULT nextval('c2010_tracts_seq'),
  tract   BIGINT NOT NULL, 
  pop     FLOAT NOT NULL
);

SELECT AddGeometryColumn('census','c2010_tracts','geo',3435,'POLYGON',2);

ALTER SEQUENCE census.c2010_tracts_seq 
  OWNED BY census.c2010_tracts.id;
ALTER TABLE ONLY census.c2010_tracts
  ADD CONSTRAINT c2010_tracts_pkey PRIMARY KEY (id);
ALTER TABLE ONLY census.c2010_tracts
  ADD CONSTRAINT c2010_tracts_unique UNIQUE(id);

\copy census.c2010_tracts (tract,pop,geo) FROM '/mnt/data1/CPD/census2010_tract_population.csv' CSV 

CREATE INDEX c2010_tract_geoidx ON census.c2010_tracts USING gist(geo); 
