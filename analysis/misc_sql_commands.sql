/*  Connect to Database from the instance
psql --host dssgpg --user tplagge tplagge
*/ 

-- Adding a length_of_stay (in days) column to db
alter table jail.inmates add column days_of_stay integer;
update jail.inmates set days_of_stay=extract(day from release_date-booking_date) where release_date is not null and booking_date is not null;

-- Determining the age at arrest
alter table jail.inmates add column age_in_days_at_arrest integer;
update jail.inmates set age_in_days_at_arrest = extract(day from booking_date-birth_date) where booking_date is not null and birth_date is not null;

-- Convert days to age in years -- 
alter table jail.inmates add column age_in_years_at_arrest float;
update jail.inmates set age_in_years_at_arrest = (cast(age_in_days_at_arrest as float))/365;

-- Adding a unique_id to members of the db
create table jail.individuals (inmate_name varchar, birth_date timestamp, id serial);
insert into jail.individuals (select inmate_name, birth_date from jail.inmates group by inmate_name, birth_date);

create view jail.inmates_with_uniqueid as select j.*, k.id inmate_id from jail.inmates j join jail.individuals k on j.inmate_name=k.inmate_name and j.birth_date=k.birth_date;

alter table jail.inmates add column individuals_id integer;
alter table jail.individuals
add primary key (id);
ALTER TABLE jail.inmates ADD CONSTRAINT individuals_fk FOREIGN KEY (unique_id) references jail.individuals (id);

update jail.inmates 
set individuals_id = individuals.id
from individuals WHERE
(inmates.inmate_name=individuals.inmate_name AND inmates.birth_date=individuals.birth_date);  

-- Adding an arrest_count column for each member in the database
CREATE table distinct_inmate_counts_table AS SELECT trim(both from inmate_name) as trim_inmate_name, birth_date, COUNT(*) FROM jail.inmates GROUP BY trim(both from inmate_name), birth_date, inmate_name;

alter table jail.inmates add column arrest_count integer;

update jail.inmates 
set arrest_count = count from jail.distinct_inmate_counts_table where
(inmates.inmate_name=distinct_inmate_counts_table.trim_inmate_name AND
inmates.birth_date=distinct_inmate_counts_table.birth_date);

/* Useful Command: Deleting a column
ALTER TABLE table_name
DROP COLUMN column_name */

