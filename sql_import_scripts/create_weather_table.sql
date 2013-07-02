DROP SCHEMA weather CASCADE;

CREATE SCHEMA weather;

SET search_path TO weather,public;

CREATE SEQUENCE weather.weather_seq;

CREATE TABLE weather.wx (
  id      INTEGER NOT NULL DEFAULT nextval('weather_seq'),
  ts      TIMESTAMP NOT NULL, 
  tmin    FLOAT,
  tmax    FLOAT,
  precip  FLOAT,
  snow    FLOAT,
  wind    FLOAT
);

ALTER SEQUENCE weather.weather_seq 
  OWNED BY weather.wx.id;
ALTER TABLE ONLY weather.wx
  ADD CONSTRAINT weather_pkey PRIMARY KEY (id);
ALTER TABLE ONLY weather.wx
  ADD CONSTRAINT weather_unique UNIQUE(id);

\copy weather.wx (ts, tmin, tmax, precip, snow, wind) FROM '/mnt/data1/CPD/ord_weather_parsed.csv' CSV HEADER
