DROP TABLE census.c2000_tracts CASCADE;

SET search_path TO census,crime,public;

CREATE SEQUENCE census.c2000_tracts_seq;

CREATE TABLE census.c2000_tracts (
  id      INTEGER NOT NULL DEFAULT nextval('c2000_tracts_seq'),
  tract   BIGINT NOT NULL, 
  pop     FLOAT 
);

SELECT AddGeometryColumn('census','c2000_tracts','geo',3435,'POLYGON',2);

ALTER SEQUENCE census.c2000_tracts_seq 
  OWNED BY census.c2000_tracts.id;
ALTER TABLE ONLY census.c2000_tracts
  ADD CONSTRAINT c2000_tracts_pkey PRIMARY KEY (id);
ALTER TABLE ONLY census.c2000_tracts
  ADD CONSTRAINT c2000_tracts_unique UNIQUE(id);

\copy census.c2000_tracts (tract,pop,geo) FROM '/mnt/data1/CPD/census2000_tract_population.csv' CSV 

CREATE INDEX c2000_tract_geoidx ON census.c2000_tracts USING gist(geo); 
