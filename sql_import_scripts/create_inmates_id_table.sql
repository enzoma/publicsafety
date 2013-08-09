DROP TABLE IF EXISTS jail.inmates_id CASCADE;

SET search_path TO jail,public;

CREATE SEQUENCE jail.inmates_id_seq;

CREATE TABLE jail.inmates_id (
  tableid      INTEGER NOT NULL DEFAULT nextval('inmates_id_seq'),
  inmate_name  VARCHAR,
  birth_date   TIMESTAMP,
  booking_date TIMESTAMP,
  address1     VARCHAR,
  address2     VARCHAR,
  state        VARCHAR,
  country      VARCHAR,
  release_date TIMESTAMP,
  clean_charge_code  VARCHAR,
  cluster_charge_code VARCHAR,
  charge_desc  VARCHAR,
  days_of_stay FLOAT,
  age_in_years_at_arrest FLOAT,
  id           INTEGER
);

ALTER SEQUENCE jail.inmates_id_seq
  OWNED BY jail.inmates_id.tableid;
ALTER TABLE ONLY jail.inmates_id
  ADD CONSTRAINT jail_inmates_id_pkey PRIMARY KEY (tableid);
ALTER TABLE ONLY jail.inmates_id
  ADD CONSTRAINT jail_inmates_id_unique UNIQUE(tableid);

\copy jail.inmates_id (inmate_name, birth_date, booking_date, address1, address2, state, country, release_date, clean_charge_code, cluster_charge_code, charge_desc, days_of_stay, age_in_years_at_arrest, id) FROM '/mnt/data1/CPD/jail/cleancrime_nolinenum.csv' CSV HEADER

