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
