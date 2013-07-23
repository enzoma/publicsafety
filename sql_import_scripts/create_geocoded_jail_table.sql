SET search_path TO jail,public;
DROP TABLE jail.inmates_geocoded CASCADE;

CREATE SEQUENCE jail.jail_geo_seq;

CREATE TABLE jail.inmates_geocoded (
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
  current_bond   FLOAT,
  latitude       FLOAT,
  longitude      FLOAT,
  days_of_stay   INTEGER
);

SELECT AddGeometryColumn('jail','inmates_geocoded','geo',3435,'POINT',2);

ALTER SEQUENCE jail.jail_geo_seq 
  OWNED BY jail.inmates_geocoded.id;
ALTER TABLE ONLY jail.inmates_geocoded
  ADD CONSTRAINT jail_geo_pkey PRIMARY KEY (id);
ALTER TABLE ONLY jail.inmates_geocoded
  ADD CONSTRAINT jail_geo_unique UNIQUE(id);
CREATE INDEX "jail_inmates_geo_id" ON "jail.inmates_geocoded" USING GIST("geo")

\copy jail.inmates_geocoded (inmate_name, birth_date, booking_date, address1, address2, city, state, country, release_date, charge_code, charge_desc, current_bond, latitude, longitude) FROM '/mnt/data1/CPD/jail/Geocoded.csv' CSV HEADER;

UPDATE jail.inmates_geocoded SET days_of_stay=extract(day FROM release_date-booking_date) WHERE release_date is not null AND booking_date is not null;
UPDATE jail.inmates_geocoded SET birth_date = birth_date - interval '100 years' WHERE extract(year FROM birth_date) > 2013;
UPDATE jail.inmates_geocoded SET inmate_name=trim(both from inmate_name);
UPDATE jail.inmates_geocoded SET geo=ST_Transform(ST_SetSRID(ST_Point("longitude", "latitude"), 4326),3435);
