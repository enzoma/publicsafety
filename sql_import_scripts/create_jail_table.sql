DROP SCHEMA jail CASCADE;

CREATE SCHEMA jail;

SET search_path TO jail,public;

CREATE SEQUENCE jail.jail_seq;

CREATE TABLE jail.inmates (
  id             INTEGER NOT NULL DEFAULT nextval('jail_seq'),
  inmate_name    VARCHAR,
  birth_date     TIMESTAMP, 
  booking_date   TIMESTAMP,
  address1       VARCHAR,
  address2       VARCHAR,
  city           VARCHAR,
  state          VARCHAR,
  country        VARCHAR,
  release_date   TIMESTAMP,
  charge_code    VARCHAR,
  charge_desc    VARCHAR,
  current_bond   FLOAT
);

ALTER SEQUENCE jail.jail_seq 
  OWNED BY jail.inmates.id;
ALTER TABLE ONLY jail.inmates
  ADD CONSTRAINT jail_pkey PRIMARY KEY (id);
ALTER TABLE ONLY jail.inmates
  ADD CONSTRAINT jail_unique UNIQUE(id);

\copy jail.inmates (inmate_name, birth_date, booking_date, address1, address2, city, state, country, release_date, charge_code, charge_desc, current_bond) FROM '/mnt/data1/CPD/jail/JailData1.csv' CSV HEADER

ALTER TABLE jail.inmates ADD COLUMN days_of_stay INTEGER;
UPDATE TABLE jail.inmates SET days_of_stay=extract(day FROM release_date-booking_date) WHERE release_date is not null AND booking_date is not null;
UPDATE jail.inmates SET birth_date = birth_date - interval '100 years' WHERE extract(year FROM birth_date) > 2013;
