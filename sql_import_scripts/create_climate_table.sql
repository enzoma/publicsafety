DROP TABLE weather.climate CASCADE;

SET search_path TO weather,public;

CREATE SEQUENCE weather.climate_seq;

CREATE TABLE weather.climate (
  id       INTEGER NOT NULL DEFAULT nextval('climate_seq'),
  ts       TIMESTAMP NOT NULL, 
  tmin     FLOAT,
  tmax     FLOAT,
  tmin_std FLOAT,
  tmax_std FLOAT
);

ALTER SEQUENCE weather.climate_seq 
  OWNED BY weather.climate.id;
ALTER TABLE ONLY weather.climate
  ADD CONSTRAINT climate_pkey PRIMARY KEY (id);
ALTER TABLE ONLY weather.climate
  ADD CONSTRAINT climate_unique UNIQUE(id);

\copy weather.climate (ts, tmin, tmax, precip, snow, wind) FROM '/mnt/data1/CPD/ord_climate_parsed.csv' CSV HEADER
