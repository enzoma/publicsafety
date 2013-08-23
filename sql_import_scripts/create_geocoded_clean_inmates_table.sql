DROP TABLE IF EXISTS jail.geocoded_clean_inmates CASCADE;

SET search_path TO jail,public;

CREATE SEQUENCE jail.geocoded_clean_inmates_seq;

CREATE TABLE jail.geocoded_clean_inmates (
  tableid         INTEGER NOT NULL DEFAULT nextval('geocoded_clean_inmates_seq'),
  id              INTEGER,
  inmate_name     VARCHAR,
  name_birth      VARCHAR,
  birth_date      TIMESTAMP,
  booking_date    TIMESTAMP,
  address1        VARCHAR,
  city            VARCHAR,
  state           VARCHAR,
  release_date    TIMESTAMP,
  charge_code     VARCHAR,
  charge_desc     VARCHAR,
  current_bond    FLOAT,
  latitude        FLOAT,
  longitude       FLOAT,
  days_of_stay    INTEGER
);

SELECT AddGeometryColumn('jail','geocoded_clean_inmates','geo',3435,'POINT',2);

ALTER SEQUENCE jail.geocoded_clean_inmates_seq
  OWNED BY jail.geocoded_clean_inmates.tableid;
ALTER TABLE ONLY jail.geocoded_clean_inmates
  ADD CONSTRAINT jail_geo_clean_pkey PRIMARY KEY (tableid);
ALTER TABLE ONLY jail.geocoded_clean_inmates
  ADD CONSTRAINT jail_geo_clean_unique UNIQUE(tableid);
CREATE INDEX "jail_geocoded_clean_tableid" ON "jail.geocoded_clean_inmates" USING GIST("geo")

\copy jail.geocoded_clean_inmates (id, inmate_name, name_birth, birth_date, booking_date, address1, city, state, release_date, charge_code, charge_desc, current_bond, latitude, longitude, days_of_stay,geo) FROM '/mnt/data1/CPD/geocoded_cleaned.csv' CSV HEADER;

