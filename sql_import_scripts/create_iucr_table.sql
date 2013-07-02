DROP TABLE crime.iucr;

CREATE SEQUENCE crime.iucr_seq;

CREATE TABLE crime.iucr (
  id      INTEGER NOT NULL DEFAULT nextval('iucr_seq'),
  iucr    VARCHAR NOT NULL,
  pdesc   VARCHAR NOT NULL,
  sdesc   VARCHAR NOT NULL,
  indexcrime VARCHAR NOT NULL
);

ALTER SEQUENCE crime.iucr_seq 
  OWNED BY crime.iucr.id;
ALTER TABLE ONLY crime.iucr
  ADD CONSTRAINT iucr_pkey PRIMARY KEY (id);
ALTER TABLE ONLY crime.iucr
  ADD CONSTRAINT iucr_unique UNIQUE(id);

\copy crime.iucr (iucr,pdesc,sdesc,indexcrime) FROM '/mnt/data1/CPD/iucr.csv' CSV HEADER

create view indexcrimes as (select c.* from crimes c join iucr i on c.iucr=i.iucr where i.indexcrime='I');

create view violentcrimes as (select * from indexcrimes where ptype='ROBBERY' or ptype='BATTERY' or ptype='ASSAULT' or ptype='HOMICIDE' or ptype='CRIM SEXUAL ASSAULT');

/*
create table violentcrimes_censustracts as (select c.*, t.tract, t.pop from violentcrimes c join census.c2010_tracts t on st_contains(t.geo,c.geo));

create view foo as (select c.count, t.geo, t.pop from (select tract, count(*) from violentcrimes_censustracts where year=2012 and (extract(hour from ts) > 18 or extract(hour from ts) < 5) group by tract) c join census.c2010_tracts t on c.tract=t.tract);
*/
