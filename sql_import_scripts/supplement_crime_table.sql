CREATE TABLE crime.foo AS (
  SELECT c.*, i.indexcrime='I' isindex FROM 
  crime.crimes c LEFT JOIN crime.iucr i ON c.iucr=i.iucr );
DROP TABLE crime.crimes;
ALTER TABLE crime.foo RENAME TO crimes;
  
ALTER TABLE crime.crimes ADD COLUMN isviolent BOOLEAN;
UPDATE crime.crimes SET isviolent=False;
UPDATE crime.crimes SET isviolent=True 
  WHERE ptype IN ('ROBBERY', 'BATTERY', 'HOMICIDE', 'CRIM SEXUAL ASSAULT');

CREATE TABLE crime.foo AS (
  SELECT c.*, b.beat_num current_beat FROM
  crime.crimes c LEFT JOIN crime.cpdbeats b ON ST_Contains(b.geom, c.geo));
DROP TABLE crime.crimes;
ALTER TABLE crime.foo RENAME TO crimes;

